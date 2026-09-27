"""
Analytics API endpoints for Sentiment and Issue Category deep-dives.
"""

from fastapi import APIRouter, HTTPException, status
from backend.app.models.schemas import SentimentAnalyticsResponse, IssueAnalyticsResponse
from backend.app.services.analytics_service import get_sentiment_analytics, get_issue_analytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/sentiment", response_model=SentimentAnalyticsResponse, summary="Get Sentiment Deep-Dive Analytics")
def read_sentiment_analytics():
    """
    Returns granular sentiment statistics, monthly volumes, and issue category correlations.
    """
    try:
        return get_sentiment_analytics()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compute sentiment analytics: {str(e)}"
        )


@router.get("/issues", response_model=IssueAnalyticsResponse, summary="Get Issue Category Analytics")
def read_issue_analytics():
    """
    Returns issue category breakdowns, frequency rankings, dissatisfaction hotspots, and trends.
    """
    try:
        return get_issue_analytics()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compute issue analytics: {str(e)}"
        )
