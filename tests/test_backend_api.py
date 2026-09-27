"""
Comprehensive API test suite for FastAPI backend endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.database import init_db

# Initialize test client and database
init_db()
client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["sentiment_model"] is True
    assert data["issue_model"] is True
    assert data["database_connected"] is True
    assert data["total_records"] > 0


def test_predict_feedback_valid():
    payload = {"text": "I was charged twice on my credit card for the same transaction."}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert "sentiment_confidence" in data
    assert "issue_category" in data
    assert "issue_confidence" in data
    assert "attention_level" in data
    assert "explanation" in data
    assert "recommended_action" in data
    assert data["sentiment"] in ["Positive", "Negative", "Neutral"]
    assert data["issue_category"] == "Payment Issue"
    assert 0.0 <= data["sentiment_confidence"] <= 1.0
    assert 0.0 <= data["issue_confidence"] <= 1.0
    assert data["attention_level"] in ["High", "Medium", "Low"]


def test_predict_feedback_validation():
    # Empty string should fail validation
    res1 = client.post("/api/predict", json={"text": ""})
    assert res1.status_code in [400, 422]

    # Too short text
    res2 = client.post("/api/predict", json={"text": "hi"})
    assert res2.status_code in [400, 422]


def test_get_dashboard_metrics():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total_feedback"] > 0
    assert data["positive_feedback"] + data["negative_feedback"] + data["neutral_feedback"] == data["total_feedback"]
    assert len(data["sentiment_distribution"]) == 3
    assert len(data["issue_distribution"]) > 0
    assert len(data["monthly_feedback"]) > 0
    assert len(data["sentiment_issue_matrix"]) > 0


def test_get_feedback_paginated():
    response = client.get("/api/feedback?page=1&limit=15")
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 15
    assert data["total"] > 0
    assert len(data["data"]) == 15


def test_get_feedback_filtering():
    response = client.get("/api/feedback?sentiment=Positive&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) > 0
    for item in data["data"]:
        assert item["sentiment"] == "Positive"


def test_get_feedback_search():
    response = client.get("/api/feedback?search=broken&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) > 0
    for item in data["data"]:
        assert "broken" in item["feedback_text"].lower() or "broken" in item["feedback_id"].lower()


def test_get_feedback_by_id():
    # Test existing feedback ID
    res1 = client.get("/api/feedback/FB-00001")
    assert res1.status_code == 200
    item = res1.json()
    assert item["feedback_id"] == "FB-00001"

    # Test non-existent ID
    res2 = client.get("/api/feedback/FB-99999999")
    assert res2.status_code == 404


def test_get_sentiment_analytics():
    response = client.get("/api/analytics/sentiment")
    assert response.status_code == 200
    data = response.json()
    assert "positive_percentage" in data
    assert "negative_percentage" in data
    assert "neutral_percentage" in data
    assert len(data["sentiment_distribution"]) == 3
    assert len(data["monthly_sentiment_trend"]) > 0
    assert "highest_negative_category" in data


def test_get_issue_analytics():
    response = client.get("/api/analytics/issues")
    assert response.status_code == 200
    data = response.json()
    assert len(data["issue_distribution"]) > 0
    assert len(data["category_statistics"]) > 0
    assert "most_reported_issue" in data
    assert "highest_negative_issue" in data


def test_get_business_insights():
    response = client.get("/api/insights")
    assert response.status_code == 200
    insights = response.json()
    assert isinstance(insights, list)
    assert len(insights) >= 3
    for ins in insights:
        assert "title" in ins
        assert "description" in ins
        assert "metric" in ins
        assert "action" in ins
