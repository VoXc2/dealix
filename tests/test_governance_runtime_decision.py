"""Runtime governance mapping tests."""

from __future__ import annotations

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.governance_os.policy_check import PolicyCheckResult, PolicyVerdict
from auto_client_acquisition.governance_os.runtime_decision import (
    governance_decision_from_passport_ai_gate,
    governance_decision_from_policy_check,
)


def test_policy_block_maps_to_block() -> None:
    r = PolicyCheckResult(False, PolicyVerdict.BLOCK, ("issue",))
    assert governance_decision_from_policy_check(r) == GovernanceDecision.BLOCK


def test_policy_allow_maps_to_allow() -> None:
    r = PolicyCheckResult(True, PolicyVerdict.ALLOW, ())
    assert governance_decision_from_policy_check(r) == GovernanceDecision.ALLOW


def test_passport_pii_external_maps_to_require_approval() -> None:
    assert (
        governance_decision_from_passport_ai_gate(
            False,
            ("pii_external_use_requires_approval_workflow",),
        )
        == GovernanceDecision.REQUIRE_APPROVAL
    )


def test_passport_multiple_errors_block() -> None:
    assert (
        governance_decision_from_passport_ai_gate(
            False,
            ("pii_external_use_requires_approval_workflow", "source_id_required"),
        )
        == GovernanceDecision.BLOCK
    )
