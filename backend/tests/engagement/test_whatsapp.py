"""
Tests for WhatsAppAgent — 24h session window, send, receive, webhook.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest

from app.engagement.base import (
    AgentContext,
    ChannelType,
    DeliveryReceipt,
    DeliveryStatus,
)
from app.engagement.channels.whatsapp import _build_twiml


# ─────────────────────────────────────────────────────────────
# TwiML builder
# ─────────────────────────────────────────────────────────────

def test_build_twiml_basic():
    """TwiML should be valid XML with the message."""
    twiml = _build_twiml("مرحبا")
    assert '<?xml version="1.0"' in twiml
    assert "<Response>" in twiml
    assert "<Message>مرحبا</Message>" in twiml


def test_build_twiml_escapes_xml():
    """TwiML builder escapes XML special characters."""
    twiml = _build_twiml("Hello & <World>")
    assert "&amp;" in twiml
    assert "&lt;" in twiml
    assert "&gt;" in twiml


# ─────────────────────────────────────────────────────────────
# receive() — payload parsing
# ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_receive_parses_twilio_form(wa_agent):
    """receive() correctly parses a Twilio inbound form payload."""
    payload = {
        "From": "whatsapp:+966512345678",
        "Body": "أريد معرفة الأسعار",
        "MessageSid": "SM_test_123",
        "ProfileName": "Ahmed",
        "NumMedia": "0",
    }

    incoming = await wa_agent.receive(payload)

    assert incoming.channel == ChannelType.WHATSAPP
    assert incoming.from_address == "+966512345678"  # prefix stripped
    assert incoming.body == "أريد معرفة الأسعار"
    assert incoming.provider_message_id == "SM_test_123"
    assert incoming.profile_name == "Ahmed"


@pytest.mark.asyncio
async def test_receive_sets_session_window(wa_agent):
    """receive() creates/updates a conversation with 24h session window."""
    payload = {
        "From": "whatsapp:+966512345678",
        "Body": "مرحبا",
        "MessageSid": "SM_001",
        "NumMedia": "0",
    }

    await wa_agent.receive(payload)

    conv = await wa_agent.memory.get_conversation(
        channel="whatsapp", address="+966512345678"
    )
    assert conv is not None
    assert conv["session_active"] == 1
    assert conv["session_expires"] is not None


# ─────────────────────────────────────────────────────────────
# 24-hour session window
# ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_in_session_window_after_user_message(wa_agent):
    """After a user message, the session window should be open."""
    phone = "+966511111111"

    # Simulate a user message (sets session window)
    payload = {"From": f"whatsapp:{phone}", "Body": "hi", "NumMedia": "0"}
    await wa_agent.receive(payload)

    in_window = await wa_agent._in_session_window(phone)
    assert in_window is True


@pytest.mark.asyncio
async def test_not_in_session_window_new_lead(wa_agent):
    """A lead with no conversation history has no session window."""
    phone = "+966599999999"
    in_window = await wa_agent._in_session_window(phone)
    assert in_window is False


@pytest.mark.asyncio
async def test_session_window_expires(wa_agent):
    """After the session expiry time, the window is closed."""
    from datetime import datetime, timedelta, timezone

    phone = "+966522222222"
    # Set an expired session
    past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    await wa_agent.memory.upsert_conversation(
        channel="whatsapp",
        address=phone,
        session_active=True,
        session_expires=past,
    )

    in_window = await wa_agent._in_session_window(phone)
    assert in_window is False


# ─────────────────────────────────────────────────────────────
# send_freeform (dry run — no Twilio creds)
# ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_send_freeform_dry_run(wa_agent):
    """Without Twilio credentials, send_freeform returns DRY RUN receipt."""
    receipt = await wa_agent.send_freeform("+966512345678", "مرحبا")
    assert receipt.status == DeliveryStatus.SENT
    assert receipt.provider_message_id == "dry_run"


# ─────────────────────────────────────────────────────────────
# handle_inbound_webhook
# ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_handle_inbound_webhook_returns_twiml(wa_agent):
    """handle_inbound_webhook returns valid TwiML XML."""
    # Mock LLM reply so we don't need real API keys
    wa_agent.llm.chat = AsyncMock(return_value="شكراً لتواصلك!")

    payload = {
        "From": "whatsapp:+966512345678",
        "Body": "مرحبا",
        "MessageSid": "SM_webhook_test",
        "ProfileName": "Ahmed",
        "NumMedia": "0",
    }

    twiml = await wa_agent.handle_inbound_webhook(payload)

    assert "<?xml" in twiml
    assert "<Message>" in twiml
    assert "شكراً" in twiml


@pytest.mark.asyncio
async def test_handle_inbound_webhook_persists_messages(wa_agent):
    """handle_inbound_webhook saves both inbound and outbound messages."""
    wa_agent.llm.chat = AsyncMock(return_value="أهلاً وسهلاً")
    # Use a unique phone number to avoid cross-test history pollution
    phone = "+966577777777"

    payload = {
        "From": f"whatsapp:{phone}",
        "Body": "كيف يعمل Dealix؟",
        "NumMedia": "0",
    }

    await wa_agent.handle_inbound_webhook(payload)

    history = await wa_agent.memory.get_history(
        channel="whatsapp", address=phone
    )
    assert len(history) >= 2
    # The last two messages should be inbound + outbound
    last_user = next(m for m in reversed(history) if m["role"] == "user")
    last_asst = next(m for m in reversed(history) if m["role"] == "assistant")
    assert last_user["content"] == "كيف يعمل Dealix؟"
    assert last_asst["content"] == "أهلاً وسهلاً"
