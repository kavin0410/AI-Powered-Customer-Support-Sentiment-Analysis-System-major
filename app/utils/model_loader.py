"""
Model loading and inference caching utility for Streamlit app.
"""

import os
import sys
from typing import Dict, Any, Tuple
import joblib
import streamlit as st

# Ensure project root is accessible
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.predictor import load_sentiment_model, load_issue_model, _extract_prediction_and_confidence


MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
SENTIMENT_MODEL_PATH = os.path.join(MODELS_DIR, "sentiment_pipeline.pkl")
ISSUE_MODEL_PATH = os.path.join(MODELS_DIR, "issue_pipeline.pkl")


@st.cache_resource(show_spinner="Loading trained machine learning models...")
def load_all_models() -> Tuple[Any, Any]:
    """
    Loads and caches both sentiment and issue classification pipelines.
    Throws descriptive human-friendly errors if files are absent or unreadable.
    """
    if not os.path.exists(SENTIMENT_MODEL_PATH):
        raise FileNotFoundError(
            f"Sentiment model pipeline not found at '{SENTIMENT_MODEL_PATH}'. "
            "Please ensure the Phase 1 training pipeline was run and generated the file."
        )

    if not os.path.exists(ISSUE_MODEL_PATH):
        raise FileNotFoundError(
            f"Issue classification model pipeline not found at '{ISSUE_MODEL_PATH}'. "
            "Please ensure the Phase 1 training pipeline was run and generated the file."
        )

    try:
        sentiment_pipeline = joblib.load(SENTIMENT_MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Failed to deserialize sentiment model from '{SENTIMENT_MODEL_PATH}': {str(e)}")

    try:
        issue_pipeline = joblib.load(ISSUE_MODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Failed to deserialize issue classification model from '{ISSUE_MODEL_PATH}': {str(e)}")

    return sentiment_pipeline, issue_pipeline


def predict_input(text: str) -> Dict[str, Any]:
    """
    Executes prediction using cached models and returns calibrated probabilities.
    """
    sentiment_model, issue_model = load_all_models()
    
    sent_res = _extract_prediction_and_confidence(sentiment_model, text)
    issue_res = _extract_prediction_and_confidence(issue_model, text)

    return {
        "sentiment": sent_res["class"],
        "sentiment_confidence": sent_res["confidence"],
        "sentiment_probabilities": sent_res["probabilities"],
        "issue_category": issue_res["class"],
        "issue_confidence": issue_res["confidence"],
        "issue_probabilities": issue_res["probabilities"]
    }
