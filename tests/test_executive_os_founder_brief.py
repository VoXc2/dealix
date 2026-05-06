"""Executive OS weekly pack."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_executive_os_weekly_pack_200() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/executive-os/weekly-pack")
    assert r.status_code == 200
    body = r.json()
    assert "week_label" in body
    assert "guardrails" in body
