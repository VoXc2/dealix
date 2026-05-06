"""Partnership OS — no white-label in API response."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_partnership_rules() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/partnership-os/status")
    assert r.status_code == 200
    rules = r.json()["rules"]
    assert rules["no_white_label_before_3_paid_pilots"] is True
