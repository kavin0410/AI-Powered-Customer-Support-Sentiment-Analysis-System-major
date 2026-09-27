# Python 3.11 Slim base image
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/ \
    && apt-get clean

# Copy and install Python dependencies
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download NLTK data required by preprocessing
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

# Copy backend code, models, and baseline data
COPY backend/ backend/
COPY models/ models/
COPY data/ data/
COPY src/ src/

# Initialize SQLite database and seed baseline records
RUN python -m backend.scripts.import_data

# Expose port
EXPOSE 8000

# Health check probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Start Uvicorn ASGI server
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
