"""System 28 — the Assurance Contract Engine.

Every agent action is governed by an assurance contract that declares what the
agent may see / propose / execute and which preconditions must hold before
execution. No contract = fail-closed DENY (`no_unbounded_agents`). An
irreversible contract must carry a rollback plan (`no_unverified_outcomes`).
External or irreversible actions escalate to approval rather than auto-execute.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.assurance_contract_os.schemas import (
    AssuranceContract,
    ContractCheckResult,
    ContractDecision,
)
from auto_client_acquisition.control_plane_os.ledger import ControlEventType, emit

_MODULE = "assurance_contract_os"


class ContractError(ValueError):
    """Raised when a contract is invalid — never swallowed."""


class ContractEngine:
    """Registers assurance contracts and evaluates actions against them."""

    def __init__(self) -> None:
        # keyed by (agent_id, action_type)
        self._contracts: dict[tuple[str, str], AssuranceContract] = {}

    def register_contract(self, contract: AssuranceContract) -> AssuranceContract:
        """Register a contract. Irreversible contracts must carry a rollback plan."""
        if contract.is_irreversible and not (contract.rollback_plan or "").strip():
            raise ContractError(
                f"irreversible contract for {contract.agent_id}/{contract.action_type} "
                "requires a rollback_plan"
            )
        self._contracts[(contract.agent_id, contract.action_type)] = contract
        emit(
            event_type=ControlEventType.CONTRACT_REGISTERED,
            source_module=_MODULE,
            subject_type="assurance_contract",
            subject_id=contract.contract_id,
            payload={
                "agent_id": contract.agent_id,
                "action_type": contract.action_type,
                "contract_type": str(contract.contract_type),
            },
        )
        return contract

    def get_contract(
        self, agent_id: str, action_type: str
    ) -> AssuranceContract | None:
        return self._contracts.get((agent_id, action_type))

    def list_contracts(
        self, *, agent_id: str | None = None
    ) -> list[AssuranceContract]:
        contracts = list(self._contracts.values())
        if agent_id:
            contracts = [c for c in contracts if c.agent_id == agent_id]
        return contracts

    def evaluate(
        self,
        *,
        agent_id: str,
        action_type: str,
        context: dict[str, Any] | None = None,
    ) -> ContractCheckResult:
        """Evaluate an action against its contract. Fails closed if none exists."""
        context = context or {}
        contract = self.get_contract(agent_id, action_type)

        if contract is None:
            result = ContractCheckResult(
                contract_id=None,
                agent_id=agent_id,
                action_type=action_type,
                passed=False,
                decision=ContractDecision.DENY,
                reason="no assurance contract registered for this action — fail closed",
            )
            self._record(result, ControlEventType.CONTRACT_FAILED)
            return result

        failed = [
            check
            for check in contract.precondition_checks
            if not context.get(check)
        ]
        if failed:
            result = ContractCheckResult(
                contract_id=contract.contract_id,
                agent_id=agent_id,
                action_type=action_type,
                passed=False,
                decision=ContractDecision.DENY,
                failed_checks=failed,
                reason=f"precondition checks failed: {', '.join(failed)}",
            )
            self._record(result, ControlEventType.CONTRACT_FAILED)
            return result

        if contract.is_external or contract.is_irreversible:
            result = ContractCheckResult(
                contract_id=contract.contract_id,
                agent_id=agent_id,
                action_type=action_type,
                passed=True,
                decision=ContractDecision.ESCALATE,
                reason="external/irreversible action requires approval before execution",
            )
            self._record(result, ControlEventType.CONTRACT_EVALUATED)
            return result

        result = ContractCheckResult(
            contract_id=contract.contract_id,
            agent_id=agent_id,
            action_type=action_type,
            passed=True,
            decision=ContractDecision.ALLOW,
            reason="all preconditions satisfied",
        )
        self._record(result, ControlEventType.CONTRACT_EVALUATED)
        return result

    def _record(
        self, result: ContractCheckResult, event_type: ControlEventType
    ) -> None:
        emit(
            event_type=event_type,
            source_module=_MODULE,
            subject_type="assurance_contract",
            subject_id=result.contract_id or "none",
            decision=str(result.decision),
            payload={
                "agent_id": result.agent_id,
                "action_type": result.action_type,
                "passed": result.passed,
                "failed_checks": result.failed_checks,
            },
        )


_ENGINE: ContractEngine | None = None


def get_contract_engine() -> ContractEngine:
    """Return the process-scoped contract engine singleton."""
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = ContractEngine()
    return _ENGINE


def reset_contract_engine() -> None:
    """Test helper: drop the cached engine."""
    global _ENGINE
    _ENGINE = None


__all__ = [
    "ContractEngine",
    "ContractError",
    "get_contract_engine",
    "reset_contract_engine",
]
