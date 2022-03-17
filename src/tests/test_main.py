from fastapi.testclient import TestClient
import json

from main import app
client = TestClient(app)


def test_read_main():
    response = client.get("/")  
    assert response.status_code == 200
    assert "message" in response.json()

