"""
Backend test suite: Detailed sentiment, issue analytics, and business insights.
"""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_get_sentiment_analytics():
    response = client.get("/api/analytics/sentiment")
    assert response.status_code == 200
    data = response.json()
    assert "positive_percentage" in data
    assert "negative_percentage" in data
    assert "neutral_percentage" in data
    assert "sentiment_distribution" in data
    assert "monthly_sentiment_trend" in data
    assert "sentiment_by_issue" in data


def test_get_issue_analytics():
    response = client.get("/api/analytics/issues")
    assert response.status_code == 200
    data = response.json()
    assert "issue_distribution" in data
    assert "issue_percentages" in data
    assert "issue_trend" in data
    assert "sentiment_by_issue" in data
    assert "category_statistics" in data


def test_get_business_insights():
    response = client.get("/api/insights")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for item in data:
        assert "title" in item
        assert "description" in item
        assert "type" in item
