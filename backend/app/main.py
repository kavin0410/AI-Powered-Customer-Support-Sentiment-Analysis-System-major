"""
FastAPI application entrypoint and route orchestrator.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import PROJECT_NAME, VERSION, DESCRIPTION, CORS_ORIGINS
from backend.app.core.database import init_db, get_db_connection
from backend.app.utils.model_loader import get_models
from backend.app.models.schemas import HealthResponse

from backend.app.api.prediction import router as prediction_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.feedback import router as feedback_router
from backend.app.api.analytics import router as analytics_router
from backend.app.api.insights import router as insights_router

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("backend.app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to initialize SQLite database and pre-load ML pipelines.
    """
    logger.info("Initializing SQLite database...")
    init_db()

    logger.info("Pre-loading ML pipelines...")
    try:
        get_models()
        logger.info("ML models successfully pre-loaded and ready for inference.")
    except Exception as e:
        logger.error("Model loading error occurred during startup: %s", str(e))

    yield
    logger.info("Cleaning up server resources upon shutdown.")


app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Centralized error handler for Pydantic validation errors (HTTP 422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        loc = " -> ".join([str(l) for l in err.get("loc", []) if l != "body"])
        msg = err.get("msg", "Invalid input value")
        errors.append(f"{loc}: {msg}" if loc else msg)
    
    error_msg = "; ".join(errors) if errors else "Validation failed for request parameters."
    logger.warning("Validation error on %s %s: %s", request.method, request.url.path, error_msg)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_msg}
    )

# Centralized generic exception handler preventing stack trace leakage (HTTP 500)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    logger.error("Unhandled internal exception on %s %s: %s", request.method, request.url.path, str(exc), exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please try again later or contact support."}
    )

# CORS Middleware for React frontend (Vite port 5173 and others)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(prediction_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(feedback_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
app.include_router(insights_router, prefix="/api")


@app.get("/api/health", response_model=HealthResponse, tags=["Health"], summary="System Health Check")
def health_check():
    """
    Validates database connectivity and ML pipeline availability.
    """
    sent_loaded = False
    issue_loaded = False
    db_connected = False
    total_records = 0

    try:
        sent_m, issue_m = get_models()
        sent_loaded = sent_m is not None
        issue_loaded = issue_m is not None
    except Exception as e:
        logger.warning("Health check model inspection: %s", str(e))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM feedback")
        total_records = cursor.fetchone()[0]
        conn.close()
        db_connected = True
    except Exception as e:
        logger.error("Health check database inspection failure: %s", str(e))

    return HealthResponse(
        status="healthy" if (sent_loaded and issue_loaded and db_connected) else "degraded",
        service="AI Customer Support API",
        sentiment_model=sent_loaded,
        issue_model=issue_loaded,
        database_connected=db_connected,
        total_records=total_records
    )


@app.get("/", tags=["Root"])
def root_info():
    return {
        "message": "AI-Powered Customer Support & Sentiment Analysis API is running.",
        "documentation": "/docs",
        "health": "/api/health"
    }
