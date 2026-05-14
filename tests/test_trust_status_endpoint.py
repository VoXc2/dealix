"""Tests for /api/v1/trust/status — shape, ETag, and Shields.io compatibility."""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.trust_status import REPORT_PATH, router as trust_status_router


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(trust_status_router)
    return TestClient(app)


def test_trust_status_returns_200_and_shields_io_shape():
    r = _client().get("/api/v1/trust/status")
    assert r.status_code == 200
    body = r.json()
    # Shields.io endpoint contract:
    assert body["schemaVersion"] == 1
    assert isinstance(body["label"], str)
    assert isinstance(body["message"], str)
    assert isinstance(body["color"], str)
    # Dealix-specific extensions:
    assert "score" in body
    assert "ceo_complete" in body


def test_trust_status_emits_etag_header():
    r = _client().get("/api/v1/trust/status")
    assert "etag" in {k.lower() for k in r.headers.keys()}


def test_trust_status_label_is_doctrine():
    body = _client().get("/api/v1/trust/status").json()
    assert "doctrine" in body["label"].lower()


def test_trust_status_resilient_to_missing_report(tmp_path, monkeypatch):
    """If verifier-report.json is missing, endpoint must NOT 500."""
    missing = tmp_path / "absent.json"
    monkeypatch.setattr("api.routers.trust_status.REPORT_PATH", missing)
    r = _client().get("/api/v1/trust/status")
    assert r.status_code == 200
    body = r.json()
    assert body["schemaVersion"] == 1
