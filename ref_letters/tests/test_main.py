from fastapi.testclient import TestClient # Import TestClient.
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import json

# from ..database import Base
from ..main import app

client = TestClient(app) # TestClient created passing the FastAPI application.

"""
Functions created with name that starts with test_ (pytest convention).
TestClient object is used the same way as with requests.
Simple assert statements written that check (pytest).
"""
def test_read_main():
    response = client.get("/ping")
    assert response.status_code == 200
    assert {'ping': 'pong!'} in response.json()