"""Assurance contract registry and policy evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone

from auto_client_acquisition.control_plane_os.tenant_context import resolve_tenant_id


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class AssuranceContract:
    contract_id: str
    tenant_id: str
    action_type: str
    status: str = "active"
    external_action: bool = False
    irreversible_action: bool = False
    rollback_plan_required: bool = False
    created_at: datetime = field(default_factory=_now)


@dataclass(frozen=True, slots=True)
class ContractDecision:
    decision: str
    reason: str
    approval_required: bool
    rollback_plan_required: bool = False


class InMemoryAssuranceContractRepository:
    def __init__(self) -> None:
        self._contracts: dict[str, dict[str, AssuranceContract]] = {}

    def register_contract(self, contract: AssuranceContract) -> AssuranceContract:
        tid = resolve_tenant_id(contract.tenant_id)
        self._contracts.setdefault(tid, {})[contract.action_type] = replace(contract, tenant_id=tid)
        return self._contracts[tid][contract.action_type]

    def get_contract(self, *, tenant_id: str | None, action_type: str) -> AssuranceContract | None:
        tid = resolve_tenant_id(tenant_id)
        return self._contracts.get(tid, {}).get(action_type)

    def evaluate_action(
        self,
        *,
        tenant_id: str | None,
        action_type: str,
        external_action: bool,
        irreversible_action: bool,
        rollback_plan: str | None,
    ) -> ContractDecision:
        contract = self.get_contract(tenant_id=tenant_id, action_type=action_type)
        if contract is None:
            return ContractDecision(
                decision="deny",
                reason="no assurance contract registered",
                approval_required=True,
                rollback_plan_required=False,
            )
        if contract.status != "active":
            return ContractDecision(
                decision="deny",
                reason="assurance contract is not active",
                approval_required=True,
                rollback_plan_required=False,
            )
        requires_rollback = contract.rollback_plan_required or irreversible_action or contract.irreversible_action
        if requires_rollback and not (rollback_plan or "").strip():
            return ContractDecision(
                decision="deny",
                reason="irreversible action requires rollback plan",
                approval_required=True,
                rollback_plan_required=True,
            )
        should_escalate = contract.external_action or external_action or irreversible_action
        if should_escalate:
            return ContractDecision(
                decision="escalate",
                reason="external or irreversible action requires approval",
                approval_required=True,
                rollback_plan_required=requires_rollback,
            )
        return ContractDecision(
            decision="allow",
            reason="assurance contract satisfied",
            approval_required=False,
            rollback_plan_required=requires_rollback,
        )


__all__ = ["AssuranceContract", "ContractDecision", "InMemoryAssuranceContractRepository"]
