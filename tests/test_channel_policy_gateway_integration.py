"""Phase 8 — Channel Policy Gateway tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.channel_policy_gateway import check_channel_policy


def test_whatsapp_internal_brief_allowed() -> None:
    d = check_channel_policy(channel="whatsapp", action_kind="internal_brief")
    assert d.allowed is True
    assert d.action_mode == "internal_only"


def test_whatsapp_cold_blocked() -> None:
    d = check_channel_policy(
        channel="whatsapp", action_kind="send_live", is_cold=True,
    )
    assert d.allowed is False
    assert d.action_mode == "blocked"
    assert "cold_whatsapp" in d.missing_conditions


def test_whatsapp_blast_blocked() -> None:
    d = check_channel_policy(
        channel="whatsapp", action_kind="send_live", is_blast=True,
    )
    assert d.allowed is False


def test_whatsapp_purchased_list_blocked() -> None:
    d = check_channel_policy(
        channel="whatsapp", action_kind="send_live", is_purchased_list=True,
    )
    assert d.allowed is False


def test_whatsapp_missing_conditions_blocks() -> None:
    d = check_channel_policy(channel="whatsapp", action_kind="send_live")
    assert d.allowed is False
    assert "consent_record_exists" in d.missing_conditions
    assert "approved_template_or_24h_window" in d.missing_conditions
    assert "live_gate_true" in d.missing_conditions
    assert "human_approved" in d.missing_conditions


def test_whatsapp_all_conditions_met_approved_manual() -> None:
    d = check_channel_policy(
        channel="whatsapp", action_kind="send_live",
        consent_record_exists=True, approved_template_or_24h_window=True,
        live_gate_true=True, human_approved=True,
    )
    assert d.allowed is True
    assert d.action_mode == "approved_manual"


def test_email_draft_allowed() -> None:
    d = check_channel_policy(channel="email", action_kind="draft")
    assert d.allowed is True
    assert d.action_mode == "draft_only"


def test_email_live_send_blocked_by_default() -> None:
    d = check_channel_policy(channel="email", action_kind="send_live")
    assert d.allowed is False


def test_email_live_send_with_gate_and_approval_allowed() -> None:
    d = check_channel_policy(
        channel="email", action_kind="send_live",
        live_gate_true=True, human_approved=True,
    )
    assert d.allowed is True


def test_linkedin_draft_allowed() -> None:
    d = check_channel_policy(channel="linkedin", action_kind="draft")
    assert d.allowed is True
    assert d.action_mode == "draft_only"


def test_linkedin_automation_blocked() -> None:
    d = check_channel_policy(channel="linkedin", action_kind="automate")
    assert d.allowed is False
    assert d.action_mode == "blocked"
    assert "NO_LINKEDIN_AUTO" in d.reason_en


def test_linkedin_scraping_blocked() -> None:
    d = check_channel_policy(channel="linkedin", action_kind="scrape")
    assert d.allowed is False
    assert "NO_SCRAPING" in d.reason_en


def test_linkedin_manual_outreach_allowed() -> None:
    d = check_channel_policy(channel="linkedin", action_kind="manual_outreach")
    assert d.allowed is True


def test_calls_script_allowed() -> None:
    d = check_channel_policy(channel="calls", action_kind="draft")
    assert d.allowed is True


def test_calls_live_dial_blocked_by_default() -> None:
    d = check_channel_policy(channel="calls", action_kind="send_live")
    assert d.allowed is False


def test_calls_live_dial_with_all_permissions_allowed() -> None:
    d = check_channel_policy(
        channel="calls", action_kind="send_live",
        customer_permission=True, live_gate_true=True, human_approved=True,
    )
    assert d.allowed is True


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/channel-policy/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "channel_policy_gateway"
    gates = body["hard_gates"]
    assert gates["no_linkedin_auto"] is True
    assert gates["no_cold_whatsapp"] is True
    assert gates["no_scraping"] is True


@pytest.mark.asyncio
async def test_check_endpoint_blocks_cold_whatsapp() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/channel-policy/check", json={
            "channel": "whatsapp",
            "action_kind": "send_live",
            "is_cold": True,
        })
    assert r.status_code == 200
    assert r.json()["decision"]["allowed"] is False


@pytest.mark.asyncio
async def test_check_endpoint_blocks_linkedin_automate() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/channel-policy/check", json={
            "channel": "linkedin",
            "action_kind": "automate",
        })
    assert r.status_code == 200
    decision = r.json()["decision"]
    assert decision["allowed"] is False
    assert decision["action_mode"] == "blocked"


@pytest.mark.asyncio
async def test_check_endpoint_invalid_channel_422() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/channel-policy/check", json={
            "channel": "smoke_signal",
            "action_kind": "draft",
        })
    assert r.status_code == 422
