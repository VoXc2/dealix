"""Assurance contracts enterprise rules tests."""

from __future__ import annotations

from auto_client_acquisition.assurance_contract_os.repositories import (
    AssuranceContract,
    InMemoryAssuranceContractRepository,
)


def test_no_contract_denies_action() -> None:
    repo = InMemoryAssuranceContractRepository()
    decision = repo.evaluate_action(
        tenant_id="tenant-a",
        action_type="whatsapp.send_message",
        external_action=True,
        irreversible_action=False,
        rollback_plan=None,
    )
    assert decision.decision == "deny"
    assert "no assurance contract" in decision.reason


def test_external_action_escalates_and_irreversible_requires_rollback_plan() -> None:
    repo = InMemoryAssuranceContractRepository()
    repo.register_contract(
        AssuranceContract(
            contract_id="ctr-1",
            tenant_id="tenant-a",
            action_type="whatsapp.send_message",
            external_action=True,
            rollback_plan_required=True,
        )
    )

    denied = repo.evaluate_action(
        tenant_id="tenant-a",
        action_type="whatsapp.send_message",
        external_action=True,
        irreversible_action=True,
        rollback_plan=None,
    )
    assert denied.decision == "deny"
    assert denied.rollback_plan_required

    escalated = repo.evaluate_action(
        tenant_id="tenant-a",
        action_type="whatsapp.send_message",
        external_action=True,
        irreversible_action=True,
        rollback_plan="draft rollback strategy",
    )
    assert escalated.decision == "escalate"
    assert escalated.approval_required
