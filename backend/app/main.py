"""
FastAPI application entrypoint and route orchestrator.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, status
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to initialize SQLite database and pre-load ML pipelines.
    """
    print("[STARTUP] Initializing SQLite database...")
    init_db()

    print("[STARTUP] Pre-loading ML pipelines...")
    try:
        get_models()
        print("[STARTUP] ML models successfully pre-loaded and ready for inference.")
    except Exception as e:
        print(f"[STARTUP ERROR] Model loading error: {str(e)}")

    yield
    print("[SHUTDOWN] Cleaning up server resources...")


app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description=DESCRIPTION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware for React frontend (Vite port 5173 and others)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS + ["*"],  # Allows local frontend seamlessly
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
    except Exception:
        pass

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM feedback")
        total_records = cursor.fetchone()[0]
        conn.close()
        db_connected = True
    except Exception:
        pass

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
