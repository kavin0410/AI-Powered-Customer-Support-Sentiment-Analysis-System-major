"""
Dashboard API endpoint.
"""

from fastapi import APIRouter, HTTPException, status
from backend.app.models.schemas import DashboardResponse
from backend.app.services.analytics_service import get_dashboard_data

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse, summary="Get Executive Dashboard Analytics")
def get_dashboard():
    """
    Returns aggregated real-time metrics, distributions, monthly trends, and cross-tabulation matrix.
    All figures are derived dynamically from the SQLite database.
    """
    try:
        return get_dashboard_data()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to compute dashboard metrics: {str(e)}"
        )
