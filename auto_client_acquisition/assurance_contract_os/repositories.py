"""Assurance contract repository + evaluation rules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.assurance_contract_os.schemas import AssuranceContract
from auto_client_acquisition.control_plane_os.tenant_context import ensure_tenant_id


@dataclass(frozen=True, slots=True)
class ContractEvaluation:
    decision: str
    reason: str
    contract_id: str = ""


class AssuranceContractRepository:
    """Tenant-scoped assurance contracts, deny-by-default."""

    def __init__(self) -> None:
        self._contracts: dict[tuple[str, str, str], AssuranceContract] = {}

    def register(self, contract: AssuranceContract) -> AssuranceContract:
        key = (contract.tenant_id, contract.agent_id, contract.action_type)
        self._contracts[key] = contract
        return contract

    def evaluate(
        self,
        *,
        tenant_id: str,
        agent_id: str,
        action_type: str,
        context: dict[str, Any] | None = None,
    ) -> ContractEvaluation:
        tenant = ensure_tenant_id(tenant_id)
        key = (tenant, agent_id, action_type)
        contract = self._contracts.get(key)
        if contract is None:
            return ContractEvaluation(decision="deny", reason="no_contract")

        context = context or {}
        for check in contract.precondition_checks:
            if not bool(context.get(check, False)):
                return ContractEvaluation(
                    decision="deny",
                    reason=f"failed_precondition:{check}",
                    contract_id=contract.contract_id,
                )

        if contract.is_irreversible and not contract.rollback_plan.strip():
            return ContractEvaluation(
                decision="deny",
                reason="irreversible_action_requires_rollback_plan",
                contract_id=contract.contract_id,
            )

        if contract.is_external or contract.is_irreversible:
            return ContractEvaluation(
                decision="escalate",
                reason="external_or_irreversible_requires_human_approval",
                contract_id=contract.contract_id,
            )

        return ContractEvaluation(
            decision="allow",
            reason="contract_checks_passed",
            contract_id=contract.contract_id,
        )

    def clear_for_test(self) -> None:
        self._contracts.clear()


__all__ = ["AssuranceContractRepository", "ContractEvaluation"]
