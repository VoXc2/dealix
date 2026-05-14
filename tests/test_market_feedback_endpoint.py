"""Tests for /api/v1/public/market-feedback — shape, honeypot, consent."""
from __future__ import annotations

import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

import api.routers.market_feedback as mf_mod
from api.routers.market_feedback import router as mf_router


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(mf_router)
    return TestClient(app)


def test_post_valid_feedback_returns_id(tmp_path, monkeypatch):
    monkeypatch.setattr(mf_mod, "LOG_PATH", tmp_path / "fb.jsonl")
    r = _client().post(
        "/api/v1/public/market-feedback",
        json={
            "signal_type": "objection",
            "message": "Pricing seems steep for a sprint.",
            "consent": True,
            "sector": "professional_services",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["feedback_id"]
    # Entry written.
    saved = (tmp_path / "fb.jsonl").read_text().strip()
    row = json.loads(saved)
    assert row["signal_type"] == "objection"
    # Stored message has emails redacted; this one had none, so passes through.
    assert "Pricing seems steep" in row["message_redacted"]


def test_post_strips_emails_from_message(tmp_path, monkeypatch):
    monkeypatch.setattr(mf_mod, "LOG_PATH", tmp_path / "fb.jsonl")
    r = _client().post(
        "/api/v1/public/market-feedback",
        json={
            "signal_type": "request",
            "message": "Please email me at someone@example.com.",
            "consent": True,
        },
    )
    assert r.status_code == 200
    row = json.loads((tmp_path / "fb.jsonl").read_text().strip())
    assert "someone@example.com" not in row["message_redacted"]
    assert "[email]" in row["message_redacted"]


def test_honeypot_silently_drops(tmp_path, monkeypatch):
    monkeypatch.setattr(mf_mod, "LOG_PATH", tmp_path / "fb.jsonl")
    r = _client().post(
        "/api/v1/public/market-feedback",
        json={
            "signal_type": "objection",
            "message": "should not be saved",
            "consent": True,
            "website": "https://spammer.example.com",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["feedback_id"] == "honeypot"
    # No file written.
    assert not (tmp_path / "fb.jsonl").exists()


def test_consent_required(tmp_path, monkeypatch):
    monkeypatch.setattr(mf_mod, "LOG_PATH", tmp_path / "fb.jsonl")
    r = _client().post(
        "/api/v1/public/market-feedback",
        json={"signal_type": "objection", "message": "x", "consent": False},
    )
    assert r.status_code == 422


def test_invalid_signal_type_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(mf_mod, "LOG_PATH", tmp_path / "fb.jsonl")
    r = _client().post(
        "/api/v1/public/market-feedback",
        json={"signal_type": "rant", "message": "x", "consent": True},
    )
    assert r.status_code == 422


def test_empty_message_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(mf_mod, "LOG_PATH", tmp_path / "fb.jsonl")
    r = _client().post(
        "/api/v1/public/market-feedback",
        json={"signal_type": "objection", "message": "", "consent": True},
    )
    assert r.status_code == 422


def test_message_too_long_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(mf_mod, "LOG_PATH", tmp_path / "fb.jsonl")
    r = _client().post(
        "/api/v1/public/market-feedback",
        json={"signal_type": "objection", "message": "x" * 5000, "consent": True},
    )
    assert r.status_code == 422


def test_summary_endpoint_returns_zero_when_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(mf_mod, "LOG_PATH", tmp_path / "absent.jsonl")
    body = _client().get("/api/v1/public/market-feedback/summary").json()
    assert body["total"] == 0
    assert body["by_signal_type"] == {}
    assert body["recent_anonymized"] == []


def test_summary_endpoint_aggregates(tmp_path, monkeypatch):
    from datetime import datetime, timezone
    log = tmp_path / "fb.jsonl"
    rows = [
        {"feedback_id": "1", "received_at": datetime.now(timezone.utc).isoformat(),
         "signal_type": "objection", "message_redacted": "A", "sector": "logistics"},
        {"feedback_id": "2", "received_at": datetime.now(timezone.utc).isoformat(),
         "signal_type": "praise", "message_redacted": "B", "sector": "fintech"},
        {"feedback_id": "3", "received_at": datetime.now(timezone.utc).isoformat(),
         "signal_type": "objection", "message_redacted": "C", "sector": "logistics"},
    ]
    log.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    monkeypatch.setattr(mf_mod, "LOG_PATH", log)
    body = _client().get("/api/v1/public/market-feedback/summary").json()
    assert body["total"] == 3
    assert body["by_signal_type"]["objection"] == 2
    assert body["by_signal_type"]["praise"] == 1
    assert body["by_sector"]["logistics"] == 2
