"""Observability v12 mode delegates."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_obs_v12_status() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/observability-v12/status")
    assert r.status_code == 200
    assert "trace_fields_recommended" in r.json()
