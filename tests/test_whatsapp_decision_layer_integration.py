"""Phase 7 — WhatsApp Decision Layer tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.whatsapp_decision_bot import (
    SUPPORTED_COMMANDS,
    build_brief,
    parse_command,
    preview_action,
)
from auto_client_acquisition.whatsapp_decision_bot.policy import (
    can_ever_live_send,
    is_unsafe_command,
)


def test_can_ever_live_send_always_false() -> None:
    """Constitutional: this layer NEVER does live customer outbound."""
    assert can_ever_live_send() is False


def test_supported_commands_include_arabic() -> None:
    assert "وش الوضع اليوم؟" in SUPPORTED_COMMANDS
    assert "وش أهم 3 قرارات؟" in SUPPORTED_COMMANDS
    assert "اعتمد الرد" in SUPPORTED_COMMANDS


def test_parse_command_today_status() -> None:
    r = parse_command(text="وش الوضع اليوم؟")
    assert r.intent == "today_status"
    assert r.action_mode == "preview_only"


def test_parse_command_top_3_decisions() -> None:
    r = parse_command(text="وش أهم 3 قرارات؟")
    assert r.intent == "top_3_decisions"
    assert r.action_mode == "preview_only"


def test_parse_command_overdue_deals() -> None:
    r = parse_command(text="وش الصفقات المتأخرة؟")
    assert r.intent == "overdue_deals"


def test_parse_command_open_support() -> None:
    r = parse_command(text="وش الدعم المفتوح؟")
    assert r.intent == "open_support"


def test_parse_command_draft_reply() -> None:
    r = parse_command(text="جهز رد للعميل")
    assert r.intent == "draft_reply"
    assert r.action_mode == "draft_only"


def test_parse_command_approve_reply_requires_approval() -> None:
    r = parse_command(text="اعتمد الرد")
    assert r.intent == "approve_reply"
    assert r.action_mode == "approval_required"
    # CRITICAL: must NEVER be approved_execute or live_send
    assert r.action_mode != "approved_execute"


def test_parse_command_blocks_unsafe_broadcast() -> None:
    """The exact unsafe pattern the prompt requires us to block."""
    r = parse_command(text="أرسل واتساب لكل الأرقام")
    assert r.intent == "blocked_unsafe"
    assert r.action_mode == "blocked"
    # Reason must be Saudi Arabic
    assert "Dealix لا يدعم" in r.output_ar


def test_parse_command_blocks_cold_whatsapp() -> None:
    r = parse_command(text="send cold whatsapp to all leads")
    assert r.action_mode == "blocked"


def test_parse_command_blocks_purchased_list() -> None:
    r = parse_command(text="استخدم القائمة المشتراة")
    assert r.action_mode == "blocked"


def test_parse_command_unknown_returns_unknown() -> None:
    r = parse_command(text="random text")
    assert r.intent == "unknown"
    assert r.action_mode == "preview_only"


def test_is_unsafe_command_detects_broadcast() -> None:
    is_unsafe, _ = is_unsafe_command("أرسل واتساب للجميع")
    assert is_unsafe


def test_preview_action_never_lives() -> None:
    p = preview_action(
        action_kind="send_whatsapp",
        text_to_send="مرحبا",
        target_handle="acme",
    )
    assert p.would_send_live is False
    assert p.requires_human_approval is True


def test_preview_action_unsafe_blocked() -> None:
    p = preview_action(
        action_kind="send_whatsapp",
        text_to_send="أرسل واتساب لكل الأرقام",
    )
    assert len(p.blocked_reasons) >= 1


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/whatsapp-decision/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "whatsapp_decision_bot"
    assert body["supports_customer_outbound"] is False
    assert body["hard_gates"]["no_live_send"] is True
    assert body["hard_gates"]["no_customer_outbound"] is True


@pytest.mark.asyncio
async def test_brief_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/whatsapp-decision/brief", json={"customer_handle": "wd-test-1"})
    assert r.status_code == 200
    body = r.json()
    assert "brief_ar" in body
    assert body["hard_gates"]["no_live_send"] is True


@pytest.mark.asyncio
async def test_command_endpoint_today_status() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/whatsapp-decision/command", json={"text": "وش الوضع اليوم؟"})
    assert r.status_code == 200
    cmd = r.json()["command"]
    assert cmd["intent"] == "today_status"


@pytest.mark.asyncio
async def test_command_endpoint_blocks_unsafe() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/whatsapp-decision/command", json={
            "text": "أرسل واتساب لكل الأرقام",
        })
    assert r.status_code == 200
    cmd = r.json()["command"]
    assert cmd["action_mode"] == "blocked"


@pytest.mark.asyncio
async def test_approval_preview_returns_no_live_send() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/whatsapp-decision/approval-preview", json={
            "action_kind": "send_whatsapp",
            "text_to_send": "مرحبا",
            "target_handle": "acme",
        })
    assert r.status_code == 200
    body = r.json()
    assert body["would_send_live_now"] is False
    assert body["preview"]["would_send_live"] is False
