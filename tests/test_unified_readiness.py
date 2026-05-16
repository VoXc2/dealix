"""Unified readiness API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_unified_readiness_get() -> None:
    resp = client.get("/api/v1/readiness/unified")
    assert resp.status_code == 200
    body = resp.json()
    assert "verdict" in body
    assert "go" in body
    assert "blockers" in body


def test_go_no_go_alias() -> None:
    resp = client.get("/api/v1/readiness/go-no-go")
    assert resp.status_code == 200
    assert "go_no_go" in resp.json()
