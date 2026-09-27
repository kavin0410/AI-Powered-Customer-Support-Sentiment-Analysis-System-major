"""
Business Insights API endpoint.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from backend.app.models.schemas import InsightItem
from backend.app.services.insight_service import generate_business_insights

router = APIRouter(prefix="/insights", tags=["Business Insights"])


@router.get("", response_model=List[InsightItem], summary="Get Automated Business Insights")
def read_business_insights():
    """
    Returns automated factual operational observations and strategic business actions
    dynamically computed from current feedback data.
    """
    try:
        return generate_business_insights()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate business insights: {str(e)}"
        )
