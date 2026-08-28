"""Commercial-state regression tests for the canonical Operating Company Contract."""

from __future__ import annotations

from auto_client_acquisition.orchestrator.operating_company_contract import (
    CANONICAL_COMMERCIAL_CHAIN,
    DEFAULT_OPERATING_COMPANY_CONTRACT,
)


def test_canonical_commercial_chain_matches_current_authority():
    assert CANONICAL_COMMERCIAL_CHAIN == (
        "real_interaction",
        "verified_relationship",
        "qualified_problem",
        "free_mini_diagnostic",
        "qualified_discovery",
        "customer_specific_quote",
        "pilot_decision",
        "pilot_payment_verified",
        "pilot_delivery",
        "proof_review",
        "expansion_or_stop",
    )


def test_research_cannot_jump_to_verified_relationship_or_paid_pilot():
    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_state_transition(
        src="research_signal", dst="verified_relationship"
    )
    assert ok is False
    assert "transition_not_allowed" in (reason or "")

    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_state_transition(
        src="research_signal", dst="pilot_payment_verified"
    )
    assert ok is False
    assert "transition_not_allowed" in (reason or "")


def test_relationship_requires_real_interaction_evidence():
    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="relationship_verified",
        history=(),
        payload={"interaction_evidence_ref": "event://big5/interaction/1"},
    )
    assert ok is False
    assert "missing_prior=interaction_captured" in (reason or "")

    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="relationship_verified",
        history=("interaction_captured",),
        payload={},
    )
    assert ok is False
    assert "missing_field=interaction_evidence_ref" in (reason or "")

    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="relationship_verified",
        history=("interaction_captured",),
        payload={"interaction_evidence_ref": "event://big5/interaction/1"},
    )
    assert ok is True
    assert reason is None


def test_free_diagnostic_starts_after_qualified_problem_not_payment():
    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="diagnostic_started",
        history=("problem_qualified",),
        payload={},
    )
    assert ok is True
    assert reason is None

    blocked, blocked_reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="diagnostic_started",
        history=("interaction_captured", "relationship_verified"),
        payload={},
    )
    assert blocked is False
    assert "missing_any_prior" in (blocked_reason or "")


def test_legacy_paid_diagnostic_history_remains_compatible():
    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="diagnostic_started",
        history=("invoice_paid",),
        payload={},
    )
    assert ok is True
    assert reason is None


def test_quote_requires_completed_diagnostic_and_discovery_evidence():
    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="discovery_completed",
        history=("diagnostic_completed",),
        payload={"discovery_notes_ref": "evidence://discovery/1"},
    )
    assert ok is True
    assert reason is None

    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="customer_specific_quote_prepared",
        history=("discovery_completed",),
        payload={"scope_evidence_ref": "evidence://scope/1"},
    )
    assert ok is True
    assert reason is None

    blocked, blocked_reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="customer_specific_quote_prepared",
        history=("diagnostic_completed",),
        payload={"scope_evidence_ref": "evidence://scope/1"},
    )
    assert blocked is False
    assert "missing_prior=discovery_completed" in (blocked_reason or "")


def test_paid_pilot_delivery_requires_verified_payment_evidence():
    blocked, blocked_reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="pilot_delivery_started",
        history=("pilot_decision_approved",),
        payload={"payment_proof_ref": "bank://proof/1"},
    )
    assert blocked is False
    assert "missing_prior=pilot_payment_verified" in (blocked_reason or "")

    blocked, blocked_reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="pilot_delivery_started",
        history=("pilot_payment_verified",),
        payload={},
    )
    assert blocked is False
    assert "missing_field=payment_proof_ref" in (blocked_reason or "")

    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="pilot_delivery_started",
        history=("pilot_payment_verified",),
        payload={"payment_proof_ref": "bank://proof/1"},
    )
    assert ok is True
    assert reason is None


def test_closed_won_cannot_be_promoted_without_payment_proof():
    blocked, blocked_reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="closed_won",
        history=("final_proof_pack_ready",),
        payload={},
    )
    assert blocked is False
    assert "closed_won_requires_verified_payment_evidence" in (blocked_reason or "")

    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="closed_won",
        history=("pilot_payment_verified",),
        payload={"payment_proof_ref": "bank://proof/1"},
    )
    assert ok is True
    assert reason is None


def test_quote_send_and_pilot_delivery_remain_governed():
    quote_needs_approval, quote_reason = (
        DEFAULT_OPERATING_COMPANY_CONTRACT.requires_approval_for_action(
            action_id="send_customer_specific_quote"
        )
    )
    assert quote_needs_approval is True
    assert "commercial_commitment" in (quote_reason or "")

    delivery_needs_approval, delivery_reason = (
        DEFAULT_OPERATING_COMPANY_CONTRACT.requires_approval_for_action(
            action_id="start_pilot_delivery",
            context={"payment_proof": False},
        )
    )
    assert delivery_needs_approval is True
    assert "payment_proof" in (delivery_reason or "")

    delivery_needs_approval, delivery_reason = (
        DEFAULT_OPERATING_COMPANY_CONTRACT.requires_approval_for_action(
            action_id="start_pilot_delivery",
            context={"payment_proof": True},
        )
    )
    assert delivery_needs_approval is False
    assert delivery_reason is None
