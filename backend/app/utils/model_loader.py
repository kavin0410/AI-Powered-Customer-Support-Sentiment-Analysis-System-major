"""
Model loading and cached singleton management for FastAPI backend.
"""

import os
import sys
from typing import Tuple, Any, Dict
import joblib
import numpy as np

# Ensure root directory is on sys.path for unpickling custom transformers
from backend.app.core.config import BASE_DIR, SENTIMENT_MODEL_PATH, ISSUE_MODEL_PATH
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

_SENTIMENT_PIPELINE = None
_ISSUE_PIPELINE = None


def get_models() -> Tuple[Any, Any]:
    """
    Returns the loaded sentiment and issue classification pipelines.
    Loads once as a singleton.
    """
    global _SENTIMENT_PIPELINE, _ISSUE_PIPELINE

    if _SENTIMENT_PIPELINE is None:
        if not os.path.exists(SENTIMENT_MODEL_PATH):
            raise FileNotFoundError(f"Sentiment pipeline not found at '{SENTIMENT_MODEL_PATH}'")
        _SENTIMENT_PIPELINE = joblib.load(SENTIMENT_MODEL_PATH)
        print(f"[MODEL LOADER] Loaded sentiment model from {SENTIMENT_MODEL_PATH}")

    if _ISSUE_PIPELINE is None:
        if not os.path.exists(ISSUE_MODEL_PATH):
            raise FileNotFoundError(f"Issue pipeline not found at '{ISSUE_MODEL_PATH}'")
        _ISSUE_PIPELINE = joblib.load(ISSUE_MODEL_PATH)
        print(f"[MODEL LOADER] Loaded issue model from {ISSUE_MODEL_PATH}")

    return _SENTIMENT_PIPELINE, _ISSUE_PIPELINE


def extract_prediction(pipeline, text: str) -> Dict[str, Any]:
    """
    Extracts predicted class and real calibrated probability distribution from an sklearn pipeline.
    """
    if hasattr(pipeline, "predict_proba"):
        probs = pipeline.predict_proba([text])[0]
        classes = pipeline.classes_
        top_idx = int(np.argmax(probs))
        predicted_class = str(classes[top_idx])
        confidence = float(probs[top_idx])
        prob_dict = {str(c): round(float(p), 4) for c, p in zip(classes, probs)}
    elif hasattr(pipeline, "decision_function"):
        dec = pipeline.decision_function([text])[0]
        exp_dec = np.exp(dec - np.max(dec))
        probs = exp_dec / np.sum(exp_dec)
        classes = pipeline.classes_
        top_idx = int(np.argmax(probs))
        predicted_class = str(classes[top_idx])
        confidence = float(probs[top_idx])
        prob_dict = {str(c): round(float(p), 4) for c, p in zip(classes, probs)}
    else:
        pred = pipeline.predict([text])[0]
        predicted_class = str(pred)
        confidence = 1.0
        prob_dict = {predicted_class: 1.0}

    return {
        "class": predicted_class,
        "confidence": round(confidence, 4),
        "probabilities": prob_dict
    }
