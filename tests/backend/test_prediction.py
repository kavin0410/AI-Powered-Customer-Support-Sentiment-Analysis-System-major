"""
Backend test suite: Machine learning prediction endpoints and validation.
"""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_predict_feedback_valid():
    payload = {"text": "The delivery was delayed by three days and the item was defective."}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] in ["Positive", "Negative", "Neutral"]
    assert 0.0 <= data["sentiment_confidence"] <= 1.0
    assert data["issue_category"] in [
        "Product Issue", "Delivery Issue", "Payment Issue",
        "Technical Issue", "Service Issue", "General Feedback"
    ]
    assert 0.0 <= data["issue_confidence"] <= 1.0
    assert data["attention_level"] in ["High", "Medium", "Low"]
    assert "sentiment_probabilities" in data
    assert "issue_probabilities" in data


def test_predict_feedback_empty_validation():
    # Empty string should fail validation
    resp1 = client.post("/api/predict", json={"text": ""})
    assert resp1.status_code in [400, 422]

    # Pure whitespace string should fail validation
    resp2 = client.post("/api/predict", json={"text": "   \n\t  "})
    assert resp2.status_code in [400, 422]

    # Excessively short input
    resp3 = client.post("/api/predict", json={"text": "a"})
    assert resp3.status_code == 422


def test_predict_feedback_excessive_length():
    huge_text = "word " * 1500
    response = client.post("/api/predict", json={"text": huge_text})
    assert response.status_code == 422
