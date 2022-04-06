from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

from ..database import Base
from ..main import app
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
'''
# Integration Test 1 - Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
'''
