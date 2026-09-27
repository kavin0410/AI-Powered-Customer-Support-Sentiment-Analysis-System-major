"""
Backend test suite: System health check and model availability.
"""

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check_status():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert data["service"] == "AI Customer Support API"
    assert "sentiment_model" in data
    assert "issue_model" in data
    assert "database_connected" in data
    assert data["total_records"] > 0


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "documentation" in data
    assert data["documentation"] == "/docs"
