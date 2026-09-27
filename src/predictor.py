"""
Unified Inference Engine for Customer Support & Sentiment Analysis.

Exposes:
- `predict_sentiment(text)`
- `predict_issue(text)`
- `predict_feedback(text)`

Loads serialized scikit-learn Pipelines and generates real, calibrated class
probabilities and predictions. Handles empty and invalid inputs robustly.
"""

import os
from typing import Dict, Any, Optional
import joblib
import numpy as np

# Default paths relative to project root
DEFAULT_MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
DEFAULT_SENTIMENT_PATH = os.path.join(DEFAULT_MODELS_DIR, "sentiment_pipeline.pkl")
DEFAULT_ISSUE_PATH = os.path.join(DEFAULT_MODELS_DIR, "issue_pipeline.pkl")

# Global cached pipelines
_SENTIMENT_PIPELINE = None
_ISSUE_PIPELINE = None


def load_sentiment_model(model_path: Optional[str] = None):
    """Loads and caches the sentiment analysis pipeline."""
    global _SENTIMENT_PIPELINE
    if _SENTIMENT_PIPELINE is None or model_path is not None:
        target_path = model_path or DEFAULT_SENTIMENT_PATH
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"Sentiment model pipeline not found at: {target_path}")
        _SENTIMENT_PIPELINE = joblib.load(target_path)
    return _SENTIMENT_PIPELINE


def load_issue_model(model_path: Optional[str] = None):
    """Loads and caches the issue classification pipeline."""
    global _ISSUE_PIPELINE
    if _ISSUE_PIPELINE is None or model_path is not None:
        target_path = model_path or DEFAULT_ISSUE_PATH
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"Issue model pipeline not found at: {target_path}")
        _ISSUE_PIPELINE = joblib.load(target_path)
    return _ISSUE_PIPELINE


def _extract_prediction_and_confidence(pipeline, text: str) -> Dict[str, Any]:
    """
    Extracts predicted class and real calibrated probability confidence from a pipeline.
    """
    # Predict probabilities if supported
    if hasattr(pipeline, "predict_proba"):
        probs = pipeline.predict_proba([text])[0]
        classes = pipeline.classes_
        top_idx = int(np.argmax(probs))
        predicted_class = str(classes[top_idx])
        confidence = float(probs[top_idx])
        prob_dict = {str(c): round(float(p), 4) for c, p in zip(classes, probs)}
    elif hasattr(pipeline, "decision_function"):
        # For non-calibrated margin estimators (SVM), apply softmax to decision values
        dec = pipeline.decision_function([text])[0]
        # Softmax transformation
        exp_dec = np.exp(dec - np.max(dec))
        probs = exp_dec / np.sum(exp_dec)
        classes = pipeline.classes_
        top_idx = int(np.argmax(probs))
        predicted_class = str(classes[top_idx])
        confidence = float(probs[top_idx])
        prob_dict = {str(c): round(float(p), 4) for c, p in zip(classes, probs)}
    else:
        # Fallback to direct prediction
        pred = pipeline.predict([text])[0]
        predicted_class = str(pred)
        confidence = 1.0
        prob_dict = {predicted_class: 1.0}

    return {
        "class": predicted_class,
        "confidence": round(confidence, 4),
        "probabilities": prob_dict
    }


def validate_input_text(text: Any) -> str:
    """Validates and sanitizes text input, raising ValueError on empty or invalid types."""
    if text is None:
        raise ValueError("Input text cannot be None.")
    if not isinstance(text, str):
        raise TypeError(f"Expected string input, received {type(text).__name__}.")
    stripped = text.strip()
    if len(stripped) == 0:
        raise ValueError("Input text cannot be empty or pure whitespace.")
    return stripped


def predict_sentiment(text: str, model_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Predict sentiment class and confidence for a given feedback string.
    
    Returns:
        dict: {"sentiment": str, "confidence": float, "probabilities": dict}
    """
    cleaned_input = validate_input_text(text)
    pipeline = load_sentiment_model(model_path)
    res = _extract_prediction_and_confidence(pipeline, cleaned_input)
    return {
        "sentiment": res["class"],
        "confidence": res["confidence"],
        "probabilities": res["probabilities"]
    }


def predict_issue(text: str, model_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Predict issue category and confidence for a given feedback string.
    
    Returns:
        dict: {"issue_category": str, "confidence": float, "probabilities": dict}
    """
    cleaned_input = validate_input_text(text)
    pipeline = load_issue_model(model_path)
    res = _extract_prediction_and_confidence(pipeline, cleaned_input)
    return {
        "issue_category": res["class"],
        "confidence": res["confidence"],
        "probabilities": res["probabilities"]
    }


def predict_feedback(text: str) -> Dict[str, Any]:
    """
    Combined prediction engine analyzing both sentiment and customer issue category.
    
    Returns:
        dict matching the required interface:
        {
            "sentiment": "...",
            "sentiment_confidence": 0.94,
            "issue_category": "...",
            "issue_confidence": 0.88,
            "all_sentiment_probabilities": {...},
            "all_issue_probabilities": {...}
        }
    """
    cleaned_input = validate_input_text(text)
    sent_res = predict_sentiment(cleaned_input)
    issue_res = predict_issue(cleaned_input)

    return {
        "sentiment": sent_res["sentiment"],
        "sentiment_confidence": sent_res["confidence"],
        "issue_category": issue_res["issue_category"],
        "issue_confidence": issue_res["confidence"],
        "all_sentiment_probabilities": sent_res["probabilities"],
        "all_issue_probabilities": issue_res["probabilities"]
    }


if __name__ == "__main__":
    test_samples = [
        "The package arrived broken, completely smashed during transit. Horrible courier service.",
        "I was charged twice on my credit card for the same order! Please refund my money immediately.",
        "Your live agent Sarah was so helpful and solved my issue within minutes. Truly wonderful support!",
        "The mobile app keeps crashing whenever I try to navigate to the checkout page.",
        "I would suggest adding more color options to your catalog in the upcoming spring season."
    ]

    print("Running sample predictions through predictor engine:\n")
    for sample in test_samples:
        result = predict_feedback(sample)
        print(f"Feedback: \"{sample}\"")
        print(f" -> Sentiment:      {result['sentiment']} (Confidence: {result['sentiment_confidence']:.2%})")
        print(f" -> Issue Category: {result['issue_category']} (Confidence: {result['issue_confidence']:.2%})\n")
