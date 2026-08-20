from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_heath_check_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok","database":"connected"}

def test_read_root_navigation():
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert data["documentation"] == "/docs"

def test_add_fact_payload_validation():
    response = client.post("/add-fact",json={})
    assert response.status_code == 422