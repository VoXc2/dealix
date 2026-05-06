"""Customer success OS status — read-only."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_cs_os_status() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/customer-success/customer-success-os/status")
    assert r.status_code == 200
    assert r.json()["guardrails"]["db_optional_degraded"] is True
