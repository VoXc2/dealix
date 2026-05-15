"""Tests for System 28 — assurance_contract_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.assurance_contract_os import (
    AssuranceContract,
    ContractType,
    get_contract_engine,
    reset_contract_engine,
)
from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_contract_engine()


def test_no_contract_fails_closed() -> None:
    # no_unbounded_agents — an action with no contract is denied
    result = get_contract_engine().evaluate(agent_id="a1", action_type="send")
    assert result.passed is False
    assert result.decision == "deny"


def test_failed_precondition_denies() -> None:
    engine = get_contract_engine()
    engine.register_contract(
        AssuranceContract(
            contract_type=ContractType.EXECUTION,
            agent_id="a1",
            action_type="draft",
            precondition_checks=["consent"],
        )
    )
    result = engine.evaluate(agent_id="a1", action_type="draft", context={})
    assert result.decision == "deny"
    assert "consent" in result.failed_checks


def test_satisfied_internal_action_allowed() -> None:
    engine = get_contract_engine()
    engine.register_contract(
        AssuranceContract(
            contract_type=ContractType.EXECUTION,
            agent_id="a1",
            action_type="draft",
            precondition_checks=["consent"],
        )
    )
    result = engine.evaluate(
        agent_id="a1", action_type="draft", context={"consent": True}
    )
    assert result.decision == "allow"


def test_external_action_escalates() -> None:
    engine = get_contract_engine()
    engine.register_contract(
        AssuranceContract(
            contract_type=ContractType.EXECUTION,
            agent_id="a1",
            action_type="send",
            is_external=True,
        )
    )
    result = engine.evaluate(agent_id="a1", action_type="send", context={})
    assert result.decision == "escalate"
