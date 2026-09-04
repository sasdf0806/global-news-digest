from datetime import UTC, datetime

from app.db import Base, get_db
from app.main import app
from app.models import Event
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool


def _client_with_events() -> TestClient:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        now = datetime.now(UTC)
        db.add_all(
            [
                Event(
                    title="Climate summit reaches agreement",
                    fact_summary="Delegates signed a new climate agreement.",
                    category="world",
                    region="global",
                    importance_score=0.95,
                    status="published",
                    last_updated_at=now,
                ),
                Event(
                    title="Draft internal policy update",
                    category="world",
                    region="global",
                    importance_score=1.0,
                    status="draft",
                    last_updated_at=now,
                ),
                Event(
                    title="Central bank holds rates",
                    fact_summary="Rates remain unchanged.",
                    category="economy",
                    region="europe",
                    importance_score=0.75,
                    status="published",
                    last_updated_at=now,
                ),
            ]
        )
        db.commit()

    def override_db():
        with Session(engine) as db:
            yield db

    app.dependency_overrides[get_db] = override_db
    return TestClient(app)


def test_events_returns_published_ranked_events_and_request_id() -> None:
    client = _client_with_events()
    try:
        response = client.get("/api/events", headers={"X-Request-ID": "req_test"})
        assert response.status_code == 200
        assert response.headers["X-Request-ID"] == "req_test"
        body = response.json()
        assert body["success"] is True
        assert body["request_id"] == "req_test"
        assert [item["title"] for item in body["data"]] == [
            "Climate summit reaches agreement",
            "Central bank holds rates",
        ]
    finally:
        app.dependency_overrides.clear()


def test_events_filters_keyword_and_paginates() -> None:
    client = _client_with_events()
    try:
        response = client.get("/api/events?keyword=agreement&limit=1&offset=0")
        assert response.status_code == 200
        assert [item["title"] for item in response.json()["data"]] == [
            "Climate summit reaches agreement"
        ]
    finally:
        app.dependency_overrides.clear()


def test_events_rejects_invalid_pagination() -> None:
    client = _client_with_events()
    try:
        assert client.get("/api/events?limit=0").status_code == 422
        assert client.get("/api/events?offset=-1").status_code == 422
    finally:
        app.dependency_overrides.clear()
