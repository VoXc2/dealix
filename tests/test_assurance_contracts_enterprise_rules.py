"""Enterprise contract rules: deny-by-default, escalate on external risk."""

from __future__ import annotations

from auto_client_acquisition.assurance_contract_os import (
    AssuranceContract,
    AssuranceContractRepository,
)


def test_no_contract_denies_action() -> None:
    repo = AssuranceContractRepository()
    result = repo.evaluate(
        tenant_id="tenant-a",
        agent_id="sales_agent",
        action_type="whatsapp.send_message",
    )
    assert result.decision == "deny"
    assert result.reason == "no_contract"


def test_failed_precondition_denies_action() -> None:
    repo = AssuranceContractRepository()
    repo.register(
        AssuranceContract(
            tenant_id="tenant-a",
            agent_id="sales_agent",
            action_type="crm.update_deal",
            precondition_checks=["has_decision_passport"],
        ),
    )
    result = repo.evaluate(
        tenant_id="tenant-a",
        agent_id="sales_agent",
        action_type="crm.update_deal",
        context={"has_decision_passport": False},
    )
    assert result.decision == "deny"
    assert "failed_precondition" in result.reason


def test_external_action_escalates_even_when_checks_pass() -> None:
    repo = AssuranceContractRepository()
    repo.register(
        AssuranceContract(
            tenant_id="tenant-a",
            agent_id="sales_agent",
            action_type="whatsapp.send_message",
            precondition_checks=["has_decision_passport"],
            is_external=True,
        ),
    )
    result = repo.evaluate(
        tenant_id="tenant-a",
        agent_id="sales_agent",
        action_type="whatsapp.send_message",
        context={"has_decision_passport": True},
    )
    assert result.decision == "escalate"


def test_irreversible_contract_requires_rollback_plan() -> None:
    repo = AssuranceContractRepository()
    repo.register(
        AssuranceContract(
            tenant_id="tenant-a",
            agent_id="ops_agent",
            action_type="delete_customer_data",
            is_irreversible=True,
            rollback_plan="",
        ),
    )
    result = repo.evaluate(
        tenant_id="tenant-a",
        agent_id="ops_agent",
        action_type="delete_customer_data",
    )
    assert result.decision == "deny"
    assert result.reason == "irreversible_action_requires_rollback_plan"
