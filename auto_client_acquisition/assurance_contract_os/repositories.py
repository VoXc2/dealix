"""Assurance contract repository and evaluator."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from auto_client_acquisition.assurance_contract_os.schemas import AssuranceContract


@dataclass(slots=True)
class ContractDecision:
    decision: str
    reason: str
    approval_required: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class InMemoryAssuranceContractRepository:
    def __init__(self) -> None:
        self._contracts: dict[tuple[str, str, str], AssuranceContract] = {}

    def register_contract(self, contract: AssuranceContract) -> AssuranceContract:
        key = (contract.tenant_id, contract.agent_id, contract.action_type)
        self._contracts[key] = contract
        return contract

    def find_contract(self, *, tenant_id: str, agent_id: str, action_type: str) -> AssuranceContract | None:
        return self._contracts.get((tenant_id, agent_id, action_type))

    def evaluate_action(
        self,
        *,
        tenant_id: str,
        agent_id: str,
        action_type: str,
        check_results: dict[str, bool] | None = None,
    ) -> ContractDecision:
        contract = self.find_contract(tenant_id=tenant_id, agent_id=agent_id, action_type=action_type)
        if contract is None:
            return ContractDecision(decision="deny", reason="no_contract")
        checks = check_results or {}
        failed_checks = [name for name in contract.precondition_checks if not checks.get(name, False)]
        if failed_checks:
            return ContractDecision(
                decision="deny",
                reason=f"failed_precondition:{','.join(failed_checks)}",
            )
        if contract.is_irreversible and not contract.rollback_plan.strip():
            return ContractDecision(
                decision="deny",
                reason="irreversible_action_requires_rollback_plan",
            )
        if contract.is_external:
            return ContractDecision(
                decision="escalate",
                reason="external_action_requires_approval",
                approval_required=True,
            )
        return ContractDecision(decision="allow", reason="contract_allows_action")
