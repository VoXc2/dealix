"""Self-improvement weekly learning — insufficient_data when no snapshot."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_weekly_learning_degraded_or_ok() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/self-improvement-os/weekly-learning")
    assert r.status_code == 200
    assert r.json()["status"] in {"insufficient_data", "ok"}
