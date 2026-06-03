"""Transactional email allowlist + revoke guard.

These tests do NOT actually send email — they verify the gating logic.
The Gmail OAuth path is exercised separately and not in this unit test.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.email.transactional import (
    ALLOWED_KINDS,
    render_diagnostic_intake_confirmation,
    render_proof_pack_delivered,
    render_proposal_sent,
    send_transactional,
)


@pytest.mark.asyncio
async def test_disallowed_kind_is_blocked(monkeypatch):
    # Force gmail to look unconfigured so we don't try to send.
    monkeypatch.setenv("GMAIL_SENDER_EMAIL", "")
    result = await send_transactional(
        kind="cold_outreach_blast",  # NOT in whitelist
        to_email="test@example.com",
        subject="hi",
        body_plain="hi",
    )
    assert result.delivered is False
    assert result.reason_code == "blocked_kind"


@pytest.mark.asyncio
async def test_missing_recipient_is_blocked(monkeypatch):
    monkeypatch.setenv("GMAIL_SENDER_EMAIL", "")
    result = await send_transactional(
        kind="diagnostic_intake_confirmation",
        to_email="",
        subject="hi",
        body_plain="hi",
    )
    assert result.delivered is False
    assert result.reason_code == "no_recipient"


def test_whitelist_only_contains_expected_kinds():
    assert "diagnostic_intake_confirmation" in ALLOWED_KINDS
    assert "proposal_sent" in ALLOWED_KINDS
    assert "proof_pack_delivered" in ALLOWED_KINDS
    assert "monthly_value_report" in ALLOWED_KINDS
    # NEVER allow cold outreach
    assert "cold_outreach" not in ALLOWED_KINDS
    assert "marketing_blast" not in ALLOWED_KINDS


def test_diagnostic_confirmation_is_bilingual():
    subject, body = render_diagnostic_intake_confirmation(
        customer_name="أحمد", sector="b2b_services"
    )
    assert "Dealix" in subject
    assert "Diagnostic" in subject
    # Bilingual body
    assert "السلام عليكم" in body
    assert "Hello" in body
    # No external send promises
    assert "scraping" not in body.lower() or "do NOT" in body or "لن" in body
    assert "غير مضمونة" in body or "no guaranteed" in body.lower()


def test_proposal_sent_includes_engagement_id_and_price():
    subject, body = render_proposal_sent(
        customer_name="Alwaha",
        engagement_id="eng_777",
        price_sar=499,
        payment_link="https://moyasar.example/pay/xyz",
    )
    assert "eng_777" in subject
    assert "499" in body
    assert "moyasar" in body


def test_proof_pack_delivered_carries_tier():
    subject, body = render_proof_pack_delivered(
        customer_name="Alwaha",
        engagement_id="eng_001",
        proof_score=82.5,
        tier="sales_support",
    )
    assert "82.5" in body
    assert "sales_support" in body
    assert "14" in body  # 14-section reference
