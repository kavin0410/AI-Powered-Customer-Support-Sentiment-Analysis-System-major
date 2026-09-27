"""
Unit tests for model serialization, loading, and pipeline integrity.
"""

import os
import pytest
import joblib
from sklearn.pipeline import Pipeline
from src.preprocessing import VALID_SENTIMENTS, VALID_CATEGORIES


MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
SENTIMENT_MODEL_PATH = os.path.join(MODELS_DIR, "sentiment_pipeline.pkl")
ISSUE_MODEL_PATH = os.path.join(MODELS_DIR, "issue_pipeline.pkl")


def test_sentiment_model_file_exists():
    assert os.path.exists(SENTIMENT_MODEL_PATH), "sentiment_pipeline.pkl is missing from models/"


def test_issue_model_file_exists():
    assert os.path.exists(ISSUE_MODEL_PATH), "issue_pipeline.pkl is missing from models/"


def test_sentiment_pipeline_structure():
    model = joblib.load(SENTIMENT_MODEL_PATH)
    assert isinstance(model, Pipeline), "Sentiment model should be an sklearn Pipeline"
    assert "preprocessor" in model.named_steps
    assert "vectorizer" in model.named_steps
    assert "classifier" in model.named_steps
    
    # Check classes
    classes = set(model.classes_)
    assert classes == VALID_SENTIMENTS, f"Expected {VALID_SENTIMENTS}, got {classes}"


def test_issue_pipeline_structure():
    model = joblib.load(ISSUE_MODEL_PATH)
    assert isinstance(model, Pipeline), "Issue model should be an sklearn Pipeline"
    assert "preprocessor" in model.named_steps
    assert "vectorizer" in model.named_steps
    assert "classifier" in model.named_steps
    
    # Check classes
    classes = set(model.classes_)
    assert classes == VALID_CATEGORIES, f"Expected {VALID_CATEGORIES}, got {classes}"


def test_model_predict_proba_available():
    sent_model = joblib.load(SENTIMENT_MODEL_PATH)
    issue_model = joblib.load(ISSUE_MODEL_PATH)

    sample = ["The courier delayed my package for two weeks."]
    sent_proba = sent_model.predict_proba(sample)
    issue_proba = issue_model.predict_proba(sample)

    assert sent_proba.shape == (1, len(VALID_SENTIMENTS))
    assert issue_proba.shape == (1, len(VALID_CATEGORIES))
    assert abs(sent_proba[0].sum() - 1.0) < 1e-4
    assert abs(issue_proba[0].sum() - 1.0) < 1e-4
