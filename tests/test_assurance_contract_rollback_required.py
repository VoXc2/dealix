"""Non-negotiable: an irreversible contract must carry a rollback plan.

Guards `no_unverified_outcomes`.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.assurance_contract_os import (
    AssuranceContract,
    ContractError,
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


def test_irreversible_contract_without_rollback_plan_rejected() -> None:
    with pytest.raises(ContractError):
        get_contract_engine().register_contract(
            AssuranceContract(
                contract_type=ContractType.EXECUTION,
                agent_id="a1",
                action_type="delete_account",
                is_irreversible=True,
            )
        )


def test_irreversible_contract_with_rollback_plan_accepted() -> None:
    contract = get_contract_engine().register_contract(
        AssuranceContract(
            contract_type=ContractType.EXECUTION,
            agent_id="a1",
            action_type="delete_account",
            is_irreversible=True,
            rollback_plan="restore from soft-delete within 30 days",
        )
    )
    assert contract.rollback_plan
