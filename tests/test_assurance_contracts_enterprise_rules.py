"""Assurance contract non-negotiable behavior."""

from __future__ import annotations

from auto_client_acquisition.assurance_contract_os.repositories import InMemoryAssuranceContractRepository
from auto_client_acquisition.assurance_contract_os.schemas import AssuranceContract


def test_no_contract_means_deny() -> None:
    repo = InMemoryAssuranceContractRepository()
    decision = repo.evaluate_action(
        tenant_id="tenant_a",
        agent_id="sales_agent",
        action_type="whatsapp.send_message",
    )
    assert decision.decision == "deny"
    assert decision.reason == "no_contract"


def test_failed_precondition_means_deny() -> None:
    repo = InMemoryAssuranceContractRepository()
    repo.register_contract(
        AssuranceContract(
            contract_id="c1",
            tenant_id="tenant_a",
            contract_type="execution",
            agent_id="sales_agent",
            action_type="crm.update_deal",
            precondition_checks=["dq_passed"],
        )
    )
    decision = repo.evaluate_action(
        tenant_id="tenant_a",
        agent_id="sales_agent",
        action_type="crm.update_deal",
        check_results={"dq_passed": False},
    )
    assert decision.decision == "deny"
    assert "failed_precondition" in decision.reason


def test_external_action_escalates() -> None:
    repo = InMemoryAssuranceContractRepository()
    repo.register_contract(
        AssuranceContract(
            contract_id="c1",
            tenant_id="tenant_a",
            contract_type="execution",
            agent_id="sales_agent",
            action_type="whatsapp.send_message",
            is_external=True,
        )
    )
    decision = repo.evaluate_action(
        tenant_id="tenant_a",
        agent_id="sales_agent",
        action_type="whatsapp.send_message",
    )
    assert decision.decision == "escalate"
    assert decision.approval_required is True


def test_irreversible_action_requires_rollback_plan() -> None:
    repo = InMemoryAssuranceContractRepository()
    repo.register_contract(
        AssuranceContract(
            contract_id="c1",
            tenant_id="tenant_a",
            contract_type="execution",
            agent_id="sales_agent",
            action_type="delete_customer_data",
            is_irreversible=True,
            rollback_plan="",
        )
    )
    decision = repo.evaluate_action(
        tenant_id="tenant_a",
        agent_id="sales_agent",
        action_type="delete_customer_data",
    )
    assert decision.decision == "deny"
    assert "rollback_plan" in decision.reason
