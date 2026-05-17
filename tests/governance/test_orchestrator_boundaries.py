"""Governance boundary tests for the orchestrator policy layer (PR6)."""

from __future__ import annotations

from auto_client_acquisition.dealix_orchestrator.policy import (
    HIGH_RISK_ACTIONS,
    can_auto_send,
    claim_has_source,
    requires_approval,
    stage_transition_allowed,
)


# ─── High-risk action gate ───────────────────────────────────────


def test_high_risk_actions_cannot_auto_send():
    for action in HIGH_RISK_ACTIONS:
        assert requires_approval(action) is True
        allowed, reason = can_auto_send(action)
        assert allowed is False
        assert reason


def test_low_risk_action_can_auto_send():
    allowed, reason = can_auto_send("qualify_lead")
    assert allowed is True
    assert reason is None


# ─── Claim source gate ───────────────────────────────────────────


def test_sensitive_claim_without_source_is_rejected():
    ok, reason = claim_has_source("we guarantee a revenue increase", None)
    assert ok is False
    assert reason

    ok, _ = claim_has_source("our platform is PDPL compliant", "")
    assert ok is False


def test_sensitive_claim_with_source_passes():
    ok, reason = claim_has_source(
        "our platform is PDPL compliant", "docs/compliance/pdpl_audit.md"
    )
    assert ok is True
    assert reason is None


def test_neutral_claim_needs_no_source():
    ok, _ = claim_has_source("the diagnostic takes about a week", None)
    assert ok is True


# ─── Stage transition gate ───────────────────────────────────────


def test_forward_single_stage_transition_allowed():
    ok, _ = stage_transition_allowed("new_lead", "qualified_a")
    assert ok is True


def test_skipping_stages_is_blocked():
    ok, reason = stage_transition_allowed("new_lead", "invoice_sent")
    assert ok is False
    assert "skip" in reason


def test_backwards_transition_is_blocked():
    ok, reason = stage_transition_allowed("invoice_sent", "new_lead")
    assert ok is False
    assert "backwards" in reason


def test_drop_to_terminal_loss_is_allowed():
    ok, _ = stage_transition_allowed("meeting_booked", "closed_lost")
    assert ok is True
