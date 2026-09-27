"""
Prediction Service orchestrating inference over trained ML pipelines.
"""

from backend.app.models.schemas import PredictionResponse
from backend.app.utils.model_loader import get_models, extract_prediction
from backend.app.utils.validation import determine_attention_level


def predict_text(text: str) -> PredictionResponse:
    """
    Executes real inference on customer feedback text using Phase 1 trained pipelines.
    Generates genuine calibrated posterior class probabilities and business triage advice.
    """
    cleaned_text = text.strip()
    sentiment_model, issue_model = get_models()

    # Model inference
    sent_res = extract_prediction(sentiment_model, cleaned_text)
    issue_res = extract_prediction(issue_model, cleaned_text)

    # Business rule triage
    triage = determine_attention_level(
        sentiment=sent_res["class"],
        sentiment_conf=sent_res["confidence"],
        issue_category=issue_res["class"]
    )

    return PredictionResponse(
        text=cleaned_text,
        sentiment=sent_res["class"],
        sentiment_confidence=sent_res["confidence"],
        issue_category=issue_res["class"],
        issue_confidence=issue_res["confidence"],
        attention_level=triage["level"],
        explanation=triage["explanation"],
        recommended_action=triage["action"],
        sentiment_probabilities=sent_res["probabilities"],
        issue_probabilities=issue_res["probabilities"]
    )
