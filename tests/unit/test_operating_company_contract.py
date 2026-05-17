"""Tests for Dealix operating-company contract."""

from __future__ import annotations

from auto_client_acquisition.orchestrator.operating_company_contract import (
    DEFAULT_OPERATING_COMPANY_CONTRACT,
    GOVERNED_ACCELERATION_CHAIN,
)
from auto_client_acquisition.orchestrator.policies import (
    AutonomyMode,
    default_policy,
    requires_approval,
)


def test_contract_summary_shape():
    summary = DEFAULT_OPERATING_COMPANY_CONTRACT.to_summary()
    assert summary["factories_total"] == 7
    assert summary["loops_total"] == 9
    assert summary["states_total"] >= 10
    assert summary["event_types_total"] >= 20


def test_governed_chain_exact_match_required():
    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_chain(
        GOVERNED_ACCELERATION_CHAIN
    )
    assert ok is True
    assert reason is None

    bad_ok, bad_reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_chain(
        ("signal", "risk", "action")
    )
    assert bad_ok is False
    assert bad_reason == "chain_must_match_governed_acceleration"


def test_event_guard_blocks_message_send_without_approval():
    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="message_sent",
        history=("message_prepared",),
        payload={},
    )
    assert ok is False
    assert "message_send_requires_approval" in (reason or "")


def test_event_guard_requires_payment_proof_for_invoice_paid():
    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="invoice_paid",
        history=("invoice_sent",),
        payload={},
    )
    assert ok is False
    assert "payment_proof" in (reason or "")

    ok_after, reason_after = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_event(
        event_type="invoice_paid",
        history=("invoice_sent",),
        payload={"payment_proof_ref": "bank_slip_2026_05_17.png"},
    )
    assert ok_after is True
    assert reason_after is None


def test_state_transition_enforces_progression():
    ok, reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_state_transition(
        src="meeting_done", dst="scope_requested"
    )
    assert ok is True
    assert reason is None

    blocked_ok, blocked_reason = DEFAULT_OPERATING_COMPANY_CONTRACT.validate_state_transition(
        src="new_lead", dst="invoice_paid"
    )
    assert blocked_ok is False
    assert "transition_not_allowed" in (blocked_reason or "")


def test_policy_approval_matrix_blocks_scope_send_even_autopilot():
    policy = default_policy("c1")
    policy.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
    needs, reason = requires_approval(action_type="send_scope", policy=policy)
    assert needs is True
    assert "operating_contract" in (reason or "")


def test_policy_approval_matrix_allows_start_delivery_with_payment_proof():
    policy = default_policy("c1")
    policy.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
    needs, reason = requires_approval(
        action_type="start_delivery",
        policy=policy,
        risk_factors={"payment_proof": True},
    )
    assert needs is False
    assert reason is None


def test_policy_approval_matrix_blocks_start_delivery_without_payment_proof():
    policy = default_policy("c1")
    policy.autonomy_mode = AutonomyMode.FULL_AUTOPILOT
    needs, reason = requires_approval(
        action_type="start_delivery",
        policy=policy,
        risk_factors={"payment_proof": False},
    )
    assert needs is True
    assert "payment_proof" in (reason or "")
