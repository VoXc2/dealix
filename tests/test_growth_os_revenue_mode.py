"""Growth OS mode — delegates safely."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_growth_os_mode() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/growth-os/status")
    assert r.status_code == 200
    assert r.json()["guardrails"]["no_auto_publish"] is True
