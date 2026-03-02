import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base
from app.core.dependencies import get_db

# SQLite test DB (file-based so multiple connections work)
TEST_DB_URL = "sqlite:///./test_ticket_booking.db"

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    # fresh DB each run
    if os.path.exists("test_ticket_booking.db"):
        os.remove("test_ticket_booking.db")

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

    if os.path.exists("test_ticket_booking.db"):
        os.remove("test_ticket_booking.db")


@pytest.fixture(scope="function")
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# -------- Helper fixtures --------

def _register(client: TestClient, email: str, password: str, role: str):
    return client.post("/auth/register", json={"email": email, "password": password, "role": role})


def _login(client: TestClient, email: str, password: str) -> str:
    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    data = r.json()
    # supports either {"access_token": "..."} or {"token": "..."}
    token = data.get("access_token") or data.get("token")
    assert token, f"Token missing in response: {data}"
    return token


@pytest.fixture
def organizer_token(client):
    _register(client, "org@test.com", "abc123", "organizer")
    return _login(client, "org@test.com", "abc123")


@pytest.fixture
def customer_token(client):
    _register(client, "cust@test.com", "abc123", "customer")
    return _login(client, "cust@test.com", "abc123")


@pytest.fixture
def admin_token(client):
    _register(client, "admin@test.com", "abc123", "admin")
    return _login(client, "admin@test.com", "abc123")


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}