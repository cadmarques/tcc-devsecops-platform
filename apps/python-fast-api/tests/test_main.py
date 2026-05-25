from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"

def test_create_item():
    payload = {"name": "Laptop", "price": 1200.00}
    response = client.post("/api/v1/items", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"
    assert response.json()["id"] >= 1

def test_list_items():
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)