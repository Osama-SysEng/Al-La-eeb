import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login():
    response = client.post("/api/v1/auth/login", data={"username": "test@test.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register():
    response = client.post("/api/v1/auth/register", json={
        "email": "new@test.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "role": "player"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "new@test.com"

def test_health():
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
