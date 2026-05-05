"""Tests for customer_inbox_v10 — Chatwoot-inspired typed inbox."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.customer_inbox_v10 import (
    Channel,
    ConsentStatus,
    Conversation,
    MessageDirection,
    add_inbound,
    check_consent,
    compute_sla,
    escalate,
    route_to_channel,
    sla_table,
    start_conversation,
    suggest_reply,
)


# ════════════════════ schemas ════════════════════


def test_channel_enum_has_six_values():
    expected = {
        "website_chat",
        "inbound_whatsapp",
        "email",
        "manual_linkedin_note",
        "support_form",
        "outbound_blocked",
    }
    actual = {c.value for c in Channel}
    assert actual == expected


def test_consent_default_unknown_blocks_outbound():
    conv = start_conversation("lead_xyz", Channel.INBOUND_WHATSAPP)
    consent_value = (
        conv.consent_status.value
        if hasattr(conv.consent_status, "value")
        else conv.consent_status
    )
    assert consent_value == ConsentStatus.UNKNOWN.value
    out = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert out["action_mode"] == "blocked"


def test_message_direction_has_three_values():
    actual = {d.value for d in MessageDirection}
    assert actual == {"inbound", "draft_outbound", "blocked_outbound"}


# ════════════════════ conversation_model ════════════════════


def test_start_conversation_creates_with_unknown_consent():
    conv = start_conversation("lead_abc", Channel.WEBSITE_CHAT)
    consent_value = (
        conv.consent_status.value
        if hasattr(conv.consent_status, "value")
        else conv.consent_status
    )
    assert consent_value == ConsentStatus.UNKNOWN.value
    assert conv.customer_handle == "lead_abc"
    assert conv.messages == []


def test_add_inbound_redacts_phone_in_body():
    conv = start_conversation("lead_abc", Channel.INBOUND_WHATSAPP)
    conv = add_inbound(conv, "Hi please call me on +966501234567 ASAP")
    assert len(conv.messages) == 1
    body = conv.messages[0].body_redacted
    assert "+966501234567" not in body
    assert "REDACTED_PHONE" in body


def test_add_inbound_redacts_email_in_body():
    conv = start_conversation("lead_abc", Channel.EMAIL)
    conv = add_inbound(conv, "Reach me at sami.test@example.com tomorrow")
    body = conv.messages[0].body_redacted
    assert "sami.test@example.com" not in body


# ════════════════════ consent_status ════════════════════


def test_check_consent_unknown_returns_false():
    conv = start_conversation("lead_abc", Channel.WEBSITE_CHAT)
    assert check_consent(conv) is False


def test_check_consent_granted_returns_true():
    conv = start_conversation("lead_abc", Channel.WEBSITE_CHAT)
    conv.consent_status = ConsentStatus.GRANTED.value
    assert check_consent(conv) is True


def test_check_consent_blocked_returns_false():
    conv = start_conversation("lead_abc", Channel.WEBSITE_CHAT)
    conv.consent_status = ConsentStatus.BLOCKED.value
    assert check_consent(conv) is False


# ════════════════════ sla_policy ════════════════════


def test_compute_sla_inbound_whatsapp_target():
    conv = start_conversation("lead_abc", Channel.INBOUND_WHATSAPP)
    sla_hours_for_whatsapp_minutes = sla_table()[Channel.INBOUND_WHATSAPP.value]
    # 5 min < 1 hr → rounded up to 1 by sla_table.
    assert sla_hours_for_whatsapp_minutes == 1
    sla = compute_sla(conv)
    assert sla.target_hours == 1
    assert sla.action == "proceed"  # no inbound yet → elapsed=0


def test_compute_sla_breaches_when_inbound_old_for_whatsapp():
    conv = start_conversation("lead_abc", Channel.INBOUND_WHATSAPP)
    conv = add_inbound(conv, "hello")
    # Force last inbound to be 2 hours ago so SLA target (5 min) is breached.
    conv.messages[0].created_at = datetime.now(UTC) - timedelta(hours=2)
    sla = compute_sla(conv)
    assert sla.breached is True
    # 2hr / 5min target → way past 2x → alert_founder.
    assert sla.action == "alert_founder"


def test_sla_table_has_all_six_channels():
    table = sla_table()
    assert set(table.keys()) == {c.value for c in Channel}


# ════════════════════ routing_policy ════════════════════


def test_route_to_inbound_whatsapp_blocked_when_consent_unknown():
    conv = start_conversation("lead_abc", Channel.INBOUND_WHATSAPP)
    out = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert out["action_mode"] == "blocked"
    assert "no_cold_whatsapp" in out["blocked_reason"]


def test_route_to_inbound_whatsapp_allowed_when_consent_granted():
    conv = start_conversation("lead_abc", Channel.INBOUND_WHATSAPP)
    conv.consent_status = ConsentStatus.GRANTED.value
    out = route_to_channel(conv, Channel.INBOUND_WHATSAPP)
    assert out["action_mode"] == "draft_only"


def test_route_outbound_blocked_always_blocked():
    conv = start_conversation("lead_abc", Channel.WEBSITE_CHAT)
    conv.consent_status = ConsentStatus.GRANTED.value
    out = route_to_channel(conv, Channel.OUTBOUND_BLOCKED)
    assert out["action_mode"] == "blocked"


def test_route_email_returns_draft_only():
    conv = start_conversation("lead_abc", Channel.EMAIL)
    out = route_to_channel(conv, Channel.EMAIL)
    assert out["action_mode"] == "draft_only"


# ════════════════════ reply_suggestion ════════════════════


def test_suggest_reply_never_approved_execute():
    conv = start_conversation("lead_abc", Channel.WEBSITE_CHAT)
    sug = suggest_reply(conv)
    assert sug.action_mode in {"draft_only", "approval_required", "blocked"}
    assert sug.action_mode != "approved_execute"


def test_suggest_reply_blocked_when_consent_blocked():
    conv = start_conversation("lead_abc", Channel.WEBSITE_CHAT)
    conv.consent_status = ConsentStatus.BLOCKED.value
    sug = suggest_reply(conv)
    assert sug.action_mode == "blocked"
    assert sug.blocked_reason


def test_suggest_reply_returns_bilingual_text_when_granted():
    conv = start_conversation("lead_abc", Channel.WEBSITE_CHAT)
    conv.consent_status = ConsentStatus.GRANTED.value
    sug = suggest_reply(conv)
    assert sug.suggested_text_ar
    assert sug.suggested_text_en
    assert sug.action_mode == "draft_only"


# ════════════════════ escalation ════════════════════


def test_escalate_returns_approval_required():
    conv = start_conversation("lead_abc", Channel.EMAIL)
    out = escalate(conv, "customer asked for VP")
    assert out["action_mode"] == "approval_required"
    assert out["reason"] == "customer asked for VP"


# ════════════════════ API endpoint tests ════════════════════


@pytest.mark.asyncio
async def test_status_endpoint_advertises_guardrails():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/customer-inbox-v10/status")
    assert r.status_code == 200
    payload = r.json()
    assert payload["module"] == "customer_inbox_v10"
    assert payload["guardrails"]["no_cold_whatsapp"] is True
    assert payload["guardrails"]["no_auto_send_external"] is True
    assert payload["guardrails"]["manual_linkedin_only"] is True


@pytest.mark.asyncio
async def test_post_suggest_reply_returns_200():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Build a simple conversation payload.
        conv = Conversation(
            customer_handle="lead_xyz",
            channel=Channel.WEBSITE_CHAT,
            consent_status=ConsentStatus.GRANTED,
        )
        r = await client.post(
            "/api/v1/customer-inbox-v10/suggest-reply",
            json=conv.model_dump(mode="json"),
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["action_mode"] in {"draft_only", "approval_required", "blocked"}
    assert payload["suggested_text_ar"]


@pytest.mark.asyncio
async def test_post_conversation_start_returns_conversation():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-inbox-v10/conversation/start",
            json={"customer_handle": "lead_x1", "channel": "website_chat"},
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["customer_handle"] == "lead_x1"
    assert payload["channel"] == "website_chat"


@pytest.mark.asyncio
async def test_get_sla_policy_returns_table():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/customer-inbox-v10/sla-policy")
    assert r.status_code == 200
    payload = r.json()
    assert "channel_targets_hours" in payload
    assert "inbound_whatsapp" in payload["channel_targets_hours"]
