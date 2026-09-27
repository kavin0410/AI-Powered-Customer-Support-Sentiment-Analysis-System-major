"""
Backend test suite: Feedback exploration, search, filtering, and pagination.
"""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_get_feedback_paginated():
    response = client.get("/api/feedback?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total" in data
    assert data["page"] == 1
    assert data["limit"] == 10
    assert len(data["data"]) <= 10
    assert data["total"] > 0

    first = data["data"][0]
    assert "feedback_id" in first
    assert "feedback_text" in first
    assert "sentiment" in first
    assert "issue_category" in first


def test_get_feedback_filtering():
    # Filter by sentiment
    res_sent = client.get("/api/feedback?sentiment=Negative&page=1&limit=5")
    assert res_sent.status_code == 200
    for item in res_sent.json()["data"]:
        assert item["sentiment"] == "Negative"

    # Filter by issue category
    res_cat = client.get("/api/feedback?issue_category=Payment+Issue&page=1&limit=5")
    assert res_cat.status_code == 200
    for item in res_cat.json()["data"]:
        assert item["issue_category"] == "Payment Issue"


def test_get_feedback_search():
    response = client.get("/api/feedback?search=delivery&page=1&limit=5")
    assert response.status_code == 200
    assert "data" in response.json()


def test_get_feedback_by_id_success_and_404():
    # Get an existing feedback_id from page 1
    list_res = client.get("/api/feedback?page=1&limit=1")
    f_id = list_res.json()["data"][0]["feedback_id"]

    res = client.get(f"/api/feedback/{f_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["feedback_id"] == f_id
    assert "feedback_text" in data

    # Non-existent ID returns 404
    err_res = client.get("/api/feedback/NON_EXISTENT_ID_9999")
    assert err_res.status_code == 404
