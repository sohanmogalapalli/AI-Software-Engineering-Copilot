from starlette.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "llm_model" in data

def test_repository_status_endpoint():
    res = client.get("/api/repository/status")
    assert res.status_code == 200
    data = res.json()
    assert "indexed" in data
