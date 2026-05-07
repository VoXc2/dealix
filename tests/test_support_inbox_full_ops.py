"""Phase 7 — Support Inbox webhook + state store + SLA monitor."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_inbound_classifies_and_drafts_refund() -> None:
    """Refund is mandatory-escalate category."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/support-inbox/inbound", json={
            "message_text": "I want a refund please.",
            "customer_id": "support-test-1",
            "channel": "email",
        })
    assert r.status_code == 200
    body = r.json()
    assert body["classification"]["category"] == "refund"
    assert body["escalation"]["should_escalate"] is True
    # Draft must be approval_required (NO_LIVE_SEND)
    assert body["draft"]["action_mode"] in ("draft_only", "approval_required")
    assert body["hard_gates"]["no_live_send"] is True


@pytest.mark.asyncio
async def test_inbound_arabic_refund_classified() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/support-inbox/inbound", json={
            "message_text": "أبي استرجاع المبلغ من فضلك",
            "customer_id": "support-ar-1",
            "channel": "whatsapp",
        })
    assert r.status_code == 200
    body = r.json()
    assert body["classification"]["is_arabic"] is True
    assert body["escalation"]["should_escalate"] is True


@pytest.mark.asyncio
async def test_inbound_redacts_email_phone() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/support-inbox/inbound", json={
            "message_text": "Contact me at sami@example.com or +966500000000 about my order",
            "customer_id": "redaction-test",
            "channel": "email",
        })
    assert r.status_code == 200
    redacted = r.json()["ticket"]["message_text_redacted"]
    assert "sami@example.com" not in redacted
    assert "+966500000000" not in redacted
    assert "[EMAIL]" in redacted or "[PHONE]" in redacted


@pytest.mark.asyncio
async def test_list_tickets_filter_by_customer() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        await c.post("/api/v1/support-inbox/inbound", json={
            "message_text": "Question about Dealix pricing.",
            "customer_id": "filter-test-1",
            "channel": "email",
        })
        r = await c.get("/api/v1/support-inbox/tickets?customer_id=filter-test-1")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 1
    for t in body["tickets"]:
        assert t["customer_id"] == "filter-test-1"


@pytest.mark.asyncio
async def test_update_ticket_status() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        ing = await c.post("/api/v1/support-inbox/inbound", json={
            "message_text": "Can you help me onboard?",
            "customer_id": "status-test",
            "channel": "form",
        })
        tid = ing.json()["ticket"]["id"]
        r = await c.post(f"/api/v1/support-inbox/tickets/{tid}/status", json={
            "status": "in_progress",
        })
    assert r.status_code == 200
    assert r.json()["ticket"]["status"] == "in_progress"


@pytest.mark.asyncio
async def test_invalid_status_422() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/support-inbox/tickets/tkt_x/status", json={
            "status": "made_up_status",
        })
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_sla_breaches_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/support-inbox/sla-breaches")
    assert r.status_code == 200
    body = r.json()
    assert "count" in body
    assert "breached" in body
    assert body["hard_gates"]["no_live_send"] is True


def test_sla_monitor_finds_overdue() -> None:
    """Backdate a ticket's sla_due_at and confirm sla_monitor catches it."""
    from auto_client_acquisition.support_inbox.state_store import _INDEX
    from auto_client_acquisition.support_inbox.sla_monitor import (
        find_breached_tickets,
    )
    from auto_client_acquisition.support_os.ticket import create_ticket

    t = create_ticket(
        message_text_redacted="overdue test",
        customer_id="overdue-test-customer",
        channel="email",
        category="technical_issue",
        priority="p1",
    )
    # Backdate by 2 hours
    t.sla_due_at = datetime.now(timezone.utc) - timedelta(hours=2)
    _INDEX[t.id] = t
    breached = find_breached_tickets(customer_id="overdue-test-customer")
    assert any(b["ticket_id"] == t.id for b in breached)
    assert breached[0]["minutes_overdue"] >= 120
