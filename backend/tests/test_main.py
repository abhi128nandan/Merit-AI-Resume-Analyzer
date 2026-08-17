from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Welcome to AI Resume Analyzer API" in data["message"]
    assert data["api_v1"] == "/api/v1"


def test_health_check_root():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
