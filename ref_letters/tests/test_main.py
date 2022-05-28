from fastapi.testclient import TestClient # Import TestClient.
from ..main import app

client = TestClient(app) # TestClient created passing the FastAPI application.

"""
Functions created with name that starts with test_ (pytest convention).
TestClient object is used the same way as with requests.
Simple assert statements written that check (pytest).
"""
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"greetings": "Welcome to FastAPI Python"}

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {'ping': 'pong!'}