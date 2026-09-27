"""
Feedback querying and detail endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Query, HTTPException, status
from backend.app.models.schemas import FeedbackListResponse, FeedbackItem
from backend.app.services.feedback_service import get_feedback_list, get_feedback_by_id

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.get("", response_model=FeedbackListResponse, summary="Get Paginated Filtered Feedback")
def list_feedback(
    sentiment: Optional[str] = Query(None, description="Filter by sentiment: Positive, Negative, Neutral"),
    issue_category: Optional[str] = Query(None, description="Filter by issue category"),
    search: Optional[str] = Query(None, description="Keyword search against text and ID"),
    start_date: Optional[str] = Query(None, description="Start date ISO YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date ISO YYYY-MM-DD"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    limit: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    Returns a paginated list of feedback records matching provided criteria.
    """
    try:
        return get_feedback_list(
            sentiment=sentiment,
            issue_category=issue_category,
            search=search,
            start_date=start_date,
            end_date=end_date,
            page=page,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database query failure: {str(e)}"
        )


@router.get("/{feedback_id}", response_model=FeedbackItem, summary="Get Single Feedback Record")
def read_feedback_record(feedback_id: str):
    """
    Retrieves full feedback details for a specific feedback ID.
    """
    record = get_feedback_by_id(feedback_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feedback record '{feedback_id}' not found."
        )
    return record
