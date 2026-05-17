"""Tests for governed revenue factory policy decisions."""

from __future__ import annotations

from auto_client_acquisition.governance_os import (
    ACTION_POLICY,
    AutomationLevel,
    DecisionStatus,
    evaluate_governed_action,
    founder_approval_action_keys,
)


def test_level_1_action_allows_without_founder_approval() -> None:
    decision = evaluate_governed_action(action_key="lead_capture")
    assert decision.status == DecisionStatus.ALLOW
    assert decision.level == AutomationLevel.LEVEL_1_FULLY_AUTOMATED


def test_level_3_action_requires_founder_approval() -> None:
    decision = evaluate_governed_action(
        action_key="external_message_send",
        evidence_events={"message_draft_prepared"},
    )
    assert decision.status == DecisionStatus.NEEDS_FOUNDER_APPROVAL
    assert decision.reason == "founder_approval_required"


def test_level_3_action_allows_after_founder_approval() -> None:
    decision = evaluate_governed_action(
        action_key="external_message_send",
        evidence_events={"message_draft_prepared"},
        founder_approved=True,
    )
    assert decision.status == DecisionStatus.ALLOW


def test_missing_required_evidence_blocks_invoice_send() -> None:
    decision = evaluate_governed_action(action_key="invoice_send")
    assert decision.status == DecisionStatus.BLOCKED
    assert decision.reason == "missing_required_evidence"
    assert decision.missing_evidence == ("scope_approved",)


def test_unknown_action_is_blocked_as_drift() -> None:
    decision = evaluate_governed_action(action_key="totally_unknown_action")
    assert decision.status == DecisionStatus.BLOCKED
    assert decision.reason == "unknown_action_drift"


def test_founder_approval_key_set_matches_policy_level_3() -> None:
    expected = {
        key
        for key, policy in ACTION_POLICY.items()
        if policy.level == AutomationLevel.LEVEL_3_FOUNDER_APPROVAL
    }
    assert founder_approval_action_keys() == expected
    assert "invoice_send" in founder_approval_action_keys()

