from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

def test_read_rl_requests():
    response = client.get("/rl_requests")
    assert response.status_code == 200

def test_read_students():
    response = client.get("/students")
    assert response.status_code == 200

def test_read_teachers():
    response = client.get("/teachers")
    assert response.status_code == 200

def test_create_student():
    response = client.post(
        "/students/",
        headers={'Content-Type': 'application/json'},
        json={"name": "Test Student", "email": "student@test.com", "school_id": 22222},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Test Student",
        "email": "student@test.com",
        "school_id": 22222
    }

def test_create_teacher():
    response = client.post(
        "/teachers/",
        headers={'Content-Type': 'application/json'},
        json={"name": "Test Teacher", "email": "teacher@test.com", "degree": "Testing web apps"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Test Teacher",
        "email": "teacher@test.com",
        "degree": "Testing web apps"
    }


def test_post_rl_requests():
    response = client.post(
        "/rl_requests/",
        headers={'Content-Type': 'application/json'},
        json={"name": "Test RL Request", "description": "rl_requests@test.com", "student_id": 1, "teacher_id": 1},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Test RL Request",
        "description": "rl_requests@test.com",
        "student_id": 1,
        "teacher_id": 1
    }