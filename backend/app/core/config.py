"""
Configuration settings for the FastAPI backend.
"""

import os
from typing import List

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Database file location
DB_PATH = os.path.join(BASE_DIR, "backend", "customer_support.db")

# Phase 1 Artifact paths
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_feedback.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
SENTIMENT_MODEL_PATH = os.path.join(MODELS_DIR, "sentiment_pipeline.pkl")
ISSUE_MODEL_PATH = os.path.join(MODELS_DIR, "issue_pipeline.pkl")

# CORS Origins
CORS_ORIGINS: List[str] = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost:8000",
]

# API Metadata
PROJECT_NAME = "AI-Powered Customer Support & Sentiment Analysis System API"
VERSION = "2.0.0"
DESCRIPTION = "FastAPI backend providing real-time sentiment analysis, issue category classification, operational analytics, and business insights."
