"""Phase 9 — Radar Events tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.radar_events import (
    EVENT_TYPES,
    is_known_event_type,
    list_recent,
    record_event,
    summary_metrics,
)
from auto_client_acquisition.radar_events.event_store import _reset_buffer


def test_taxonomy_contains_required_event_types() -> None:
    required = [
        "lead_created", "lead_scored", "approval_requested", "approval_accepted",
        "support_ticket_created", "support_ticket_escalated",
        "service_session_started", "payment_intent_created", "payment_confirmed",
        "proof_event_created", "proof_pack_generated", "executive_pack_generated",
        "unsafe_action_blocked", "whatsapp_decision_requested",
        "customer_portal_opened", "customer_portal_degraded",
        "case_study_candidate_created",
    ]
    for r in required:
        assert r in EVENT_TYPES, f"missing event type: {r}"


def test_is_known_event_type() -> None:
    assert is_known_event_type("lead_created") is True
    assert is_known_event_type("totally_made_up") is False


def test_record_event_redacts_email() -> None:
    e = record_event(
        event_type="lead_created",
        customer_handle="rad-test-1",
        payload={"contact_email": "secret@private.sa", "note": "test"},
    )
    blob = str(e["payload"])
    # Original email must NOT appear; either [EMAIL] or asterisk-mask is OK
    assert "secret@private.sa" not in blob
    assert "[EMAIL]" in blob or "***" in blob


def test_record_event_redacts_phone() -> None:
    e = record_event(
        event_type="lead_scored",
        customer_handle="rad-test-2",
        payload={"contact_phone": "+966500000000"},
    )
    blob = str(e["payload"])
    assert "+966500000000" not in blob
    assert "[PHONE]" in blob or "***" in blob


def test_record_event_unknown_type_still_recorded_but_flagged() -> None:
    e = record_event(
        event_type="not_in_taxonomy_xyz",
        payload={"x": 1},
    )
    assert e["is_known_type"] is False


def test_summary_metrics_counts() -> None:
    _reset_buffer()
    record_event(event_type="lead_created", payload={})
    record_event(event_type="lead_created", payload={})
    record_event(event_type="approval_requested", payload={})
    s = summary_metrics()
    assert s["total_events"] == 3
    assert s["by_event_type"]["lead_created"] == 2
    assert s["by_event_type"]["approval_requested"] == 1


def test_unsafe_action_blocked_event_supported() -> None:
    e = record_event(event_type="unsafe_action_blocked", payload={"reason": "cold_whatsapp"})
    assert e["is_known_type"] is True


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/radar-events/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "radar_events"
    assert body["hard_gates"]["no_pii_in_event_payload"] is True


@pytest.mark.asyncio
async def test_taxonomy_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/radar-events/taxonomy")
    assert r.status_code == 200
    body = r.json()
    assert "lead_created" in body["event_types"]
    assert body["count"] >= 18


@pytest.mark.asyncio
async def test_record_endpoint_redacts() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/radar-events/record", json={
            "event_type": "lead_created",
            "customer_handle": "rad-http-test",
            "payload": {"email": "secret_user@private-domain.sa"},
        })
    assert r.status_code == 200
    blob = str(r.json()["event"]["payload"])
    # Real email must be stripped (any form of redaction is acceptable)
    assert "secret_user@private-domain.sa" not in blob


@pytest.mark.asyncio
async def test_record_endpoint_requires_event_type() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/radar-events/record", json={"payload": {}})
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_summary_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/radar-events/summary")
    assert r.status_code == 200
    body = r.json()
    assert "summary" in body
    assert "funnel_health" in body
