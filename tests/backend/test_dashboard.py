"""
Backend test suite: Executive dashboard aggregation KPIs and distribution series.
"""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_get_dashboard_metrics():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()

    assert data["total_feedback"] > 0
    assert data["positive_feedback"] >= 0
    assert data["negative_feedback"] >= 0
    assert data["neutral_feedback"] >= 0
    assert (
        data["positive_feedback"] + data["negative_feedback"] + data["neutral_feedback"]
        == data["total_feedback"]
    )
    assert data["most_common_issue"] != ""
    assert isinstance(data["sentiment_distribution"], list)
    assert len(data["sentiment_distribution"]) == 3
    assert isinstance(data["issue_distribution"], list)
    assert len(data["issue_distribution"]) == 6
    assert isinstance(data["monthly_feedback"], list)
    assert isinstance(data["sentiment_trend"], list)
