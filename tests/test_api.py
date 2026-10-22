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

def test_settings_endpoints():
    res = client.get("/api/settings")
    assert res.status_code == 200
    data = res.json()
    assert "recommended_models" in data
    assert len(data["recommended_models"]) > 0

    post_res = client.post("/api/settings", json={"provider": "gemini", "model": "gemini-2.0-flash"})
    assert post_res.status_code == 200
    assert post_res.json()["active_provider"] == "gemini"
