from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .. import cruds
from ..main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_post_items():

    # We grab another session to check
    # if the items are created
    db = override_get_db()
    client = TestClient(app)

    client.post("/rl_requests/", json={"title": "Example 1"})

    client.post("/rl_requests/", json={"title": "Example 2"})

    items = cruds.get_rl_requests(db)
    assert len(items) == 2
