"""Proof ledger — list endpoint returns structure (may be empty)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_proof_ledger_list_events() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/proof-ledger/events?limit=5")
    assert r.status_code == 200
    body = r.json()
    assert "count" in body
    assert "events" in body
