"""
Prediction API endpoint.
"""

from fastapi import APIRouter, HTTPException, status
from backend.app.models.schemas import PredictionRequest, PredictionResponse
from backend.app.services.prediction_service import predict_text

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("", response_model=PredictionResponse, summary="Predict Sentiment & Issue Category")
def predict_feedback(request: PredictionRequest):
    """
    Analyzes customer feedback text using Phase 1 trained ML pipelines.
    Returns:
    - Sentiment (Positive, Negative, Neutral) with calibrated confidence
    - Issue Category (6 classes) with calibrated confidence
    - Business-rule Attention Level triage (High, Medium, Low)
    - Full class probability distributions
    """
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback text cannot be empty or pure whitespace."
        )

    try:
        response = predict_text(request.text)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference engine failure: {str(e)}"
        )
