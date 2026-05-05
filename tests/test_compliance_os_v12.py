"""V12 Phase 6 — compliance_os_v12 action_policy + endpoint tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.compliance_os_v12 import evaluate_action


# ─────────────── Hard-blocked actions (regardless of consent) ────────


def test_cold_whatsapp_always_blocked() -> None:
    d = evaluate_action(action_type="cold_whatsapp", channel="whatsapp", consent_state="granted")
    assert d.verdict == "blocked"
    assert d.action_mode == "blocked"


def test_scrape_always_blocked() -> None:
    d = evaluate_action(action_type="scrape")
    assert d.verdict == "blocked"


def test_linkedin_automation_always_blocked() -> None:
    d = evaluate_action(action_type="linkedin_automation")
    assert d.verdict == "blocked"


def test_purchased_list_always_blocked() -> None:
    d = evaluate_action(action_type="purchased_list")
    assert d.verdict == "blocked"


def test_live_charge_blocked_by_default() -> None:
    d = evaluate_action(action_type="live_charge")
    assert d.verdict == "blocked"


# ─────────────── Always-escalate (data rights) ────────────


def test_delete_request_escalates() -> None:
    d = evaluate_action(action_type="delete_request")
    assert d.verdict == "needs_review"
    assert d.escalate_to_human is True
    assert d.action_mode == "approval_required"


def test_export_request_escalates() -> None:
    d = evaluate_action(action_type="export_request")
    assert d.verdict == "needs_review"
    assert d.escalate_to_human is True


def test_withdraw_consent_escalates() -> None:
    d = evaluate_action(action_type="withdraw_consent")
    assert d.escalate_to_human is True


# ─────────────── Internal allowed actions ────────────


def test_internal_note_allowed_as_draft() -> None:
    d = evaluate_action(action_type="internal_note", channel="internal")
    assert d.verdict == "allowed"
    assert d.action_mode == "draft_only"


def test_compose_diagnostic_allowed_as_draft() -> None:
    d = evaluate_action(action_type="compose_diagnostic")
    assert d.verdict == "allowed"


# ─────────────── Outbound + consent matrix ────────────


def test_send_message_warm_intro_allowed_as_draft() -> None:
    d = evaluate_action(
        action_type="send_message", channel="warm_intro", consent_state="not_yet_asked"
    )
    assert d.verdict == "allowed"
    assert d.action_mode == "draft_only"


def test_send_message_whatsapp_with_active_consent_allowed_as_draft() -> None:
    d = evaluate_action(
        action_type="send_message", channel="whatsapp", consent_state="granted"
    )
    assert d.verdict == "allowed"
    assert d.action_mode == "draft_only"


def test_send_message_whatsapp_withdrawn_consent_blocked() -> None:
    d = evaluate_action(
        action_type="send_message", channel="whatsapp", consent_state="withdrawn"
    )
    assert d.verdict == "blocked"
    assert d.escalate_to_human is True


def test_send_message_email_no_consent_needs_review() -> None:
    d = evaluate_action(
        action_type="send_message", channel="email", consent_state="not_yet_asked"
    )
    assert d.verdict == "needs_review"
    assert d.action_mode == "approval_required"


# ─────────────── Unknown action fail-safe ────────────


def test_unknown_action_fails_safe_to_review() -> None:
    d = evaluate_action(action_type="some_random_action_we_havent_thought_of")
    assert d.verdict == "needs_review"
    assert d.escalate_to_human is True


# ─────────────── Router endpoint ────────────


@pytest.mark.asyncio
async def test_action_check_endpoint_blocks_cold_whatsapp() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-data/action-check",
            json={
                "action_type": "cold_whatsapp",
                "channel": "whatsapp",
                "consent_state": "granted",
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body["verdict"] == "blocked"
    assert body["action_mode"] == "blocked"


@pytest.mark.asyncio
async def test_action_check_endpoint_warm_intro_allowed() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-data/action-check",
            json={
                "action_type": "send_message",
                "channel": "warm_intro",
                "consent_state": "not_yet_asked",
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body["verdict"] == "allowed"
    assert body["action_mode"] == "draft_only"


@pytest.mark.asyncio
async def test_action_check_returns_bilingual_reasons() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-data/action-check",
            json={"action_type": "delete_request"},
        )
    body = r.json()
    assert "PDPL" in body["reason_en"]
    assert "PDPL" in body["reason_ar"]
    assert body["escalate_to_human"] is True
