"""Trust dashboard API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_trust_dashboard() -> None:
    resp = client.get("/api/v1/trust/dashboard")
    assert resp.status_code == 200
    body = resp.json()
    assert body["approval_first"] is True
    assert body["cold_outreach_automation"] is False
