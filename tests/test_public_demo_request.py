"""
Tests for the public landing demo-request handler.

Pins the contract relied on by `landing/script.js`:
  - shape: { ok: True, calendly_url: "...", lead_id?: "..." }
  - status 200 on valid payload
  - 422 on missing required fields
  - 422 on missing consent
  - honeypot: silent ok with no LeadRecord persisted
  - LeadRecord persisted on valid submission (source='website')
  - idempotent on email within 30 days (no duplicate row)
  - PostHog failure does not block LeadRecord persistence
  - DB write failure does not block the response
"""

from __future__ import annotations

import importlib
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("APP_SECRET_KEY", "test-secret")
    db = tmp_path / "demo.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db}")
    # Reload settings + clear caches so each test gets a fresh engine
    importlib.reload(importlib.import_module("core.config.settings"))
    import db.session as _sess
    _sess._sessionmaker.cache_clear()
    _sess._engine.cache_clear()

    from api.main import create_app
    app = create_app()
    with TestClient(app) as c:
        yield c


VALID_BODY = {
    "name": "Test Lead",
    "company": "TestCo",
    "email": "test@example.sa",
    "phone": "+966500000000",
    "sector": "saas",
    "size": "11-50",
    "message": "hello",
    "consent": True,
}


def test_demo_request_returns_ok_and_calendly_url(client) -> None:
    r = client.post("/api/v1/public/demo-request", json=VALID_BODY)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True
    assert body["calendly_url"].startswith("https://"), body
    # lead_id is optional in the contract (DB write may skip on failure),
    # but in a healthy test env we expect it to be present.
    assert "lead_id" in body, "valid form should produce a lead_id when DB is healthy"


def test_demo_request_creates_lead_record(client) -> None:
    """LeadRecord must be persisted with source='website'."""
    from db.models import LeadRecord
    from db.session import async_session_factory

    r = client.post("/api/v1/public/demo-request", json=VALID_BODY)
    assert r.status_code == 200
    lead_id = r.json().get("lead_id")
    assert lead_id

    import asyncio
    async def _read():
        async with async_session_factory() as s:
            return (await s.execute(
                select(LeadRecord).where(LeadRecord.id == lead_id)
            )).scalars().first()
    rec = asyncio.run(_read())
    assert rec is not None
    assert rec.source == "website"
    assert rec.contact_email == "test@example.sa"
    assert rec.company_name == "TestCo"


def test_demo_request_idempotent_on_email_within_30d(client) -> None:
    """Submitting twice with the same email returns the SAME lead_id."""
    r1 = client.post("/api/v1/public/demo-request", json=VALID_BODY)
    r2 = client.post("/api/v1/public/demo-request", json={**VALID_BODY, "name": "Different"})
    assert r1.status_code == 200 and r2.status_code == 200
    lead1 = r1.json().get("lead_id")
    lead2 = r2.json().get("lead_id")
    assert lead1 and lead2
    assert lead1 == lead2, "duplicate email within 30d must reuse the same LeadRecord"


def test_demo_request_missing_required_fields(client) -> None:
    body = dict(VALID_BODY)
    body.pop("name")
    r = client.post("/api/v1/public/demo-request", json=body)
    assert r.status_code == 422
    assert r.json().get("detail") == "missing_required_fields"


def test_demo_request_consent_required(client) -> None:
    body = {**VALID_BODY, "consent": False}
    r = client.post("/api/v1/public/demo-request", json=body)
    assert r.status_code == 422
    assert r.json().get("detail") == "consent_required"


def test_demo_request_honeypot_silently_drops(client) -> None:
    """A filled `website` field = bot. Return ok but persist nothing."""
    from db.models import LeadRecord
    from db.session import async_session_factory

    body = {**VALID_BODY, "website": "http://spam.example"}
    r = client.post("/api/v1/public/demo-request", json=body)
    assert r.status_code == 200
    assert r.json()["ok"] is True
    # No lead_id should be returned because the path is silently dropped.
    assert "lead_id" not in r.json()

    import asyncio
    async def _count():
        async with async_session_factory() as s:
            rows = (await s.execute(
                select(LeadRecord).where(LeadRecord.contact_email == VALID_BODY["email"])
            )).scalars().all()
            return len(rows)
    assert asyncio.run(_count()) == 0, "honeypot must not persist a LeadRecord"


def test_demo_request_posthog_failure_does_not_block_lead_record(client) -> None:
    """If PostHog raises, the LeadRecord must still be created."""
    async def _bomb(*_a, **_kw):
        raise RuntimeError("posthog exploded")

    with patch("api.routers.public.capture_event", _bomb):
        r = client.post("/api/v1/public/demo-request", json=VALID_BODY)
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    # PostHog blew up but the LeadRecord write should still have happened.
    assert "lead_id" in body, "PostHog failure must not block DB persistence"


def test_demo_request_db_write_failure_does_not_block_response(client) -> None:
    """Even if the DB write itself raises, the visitor still gets the calendly URL."""
    async def _bomb(*_a, **_kw):
        raise RuntimeError("db hiccup")

    with patch("api.routers.public._record_inbound_lead", _bomb):
        r = client.post("/api/v1/public/demo-request", json=VALID_BODY)
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["calendly_url"].startswith("https://")
    # No lead_id when the wrapper itself raised.
    assert "lead_id" not in body
