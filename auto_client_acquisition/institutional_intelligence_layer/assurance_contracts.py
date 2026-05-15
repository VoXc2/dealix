"""Assurance and safety contracts (System 58)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssuranceContract:
    contract_id: str
    permission_scope: frozenset[str]
    execution_checks: tuple[str, ...]
    approval_checks: tuple[str, ...]
    rollback_checks: tuple[str, ...]
    evaluation_checks: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AssuranceRuntimeInput:
    action_scope: str
    checks_passed: frozenset[str]
    has_human_approval: bool


def assurance_contract_allows_execution(
    contract: AssuranceContract,
    runtime: AssuranceRuntimeInput,
) -> tuple[bool, tuple[str, ...]]:
    """Validate execution against an assurance contract envelope."""
    blockers: list[str] = []
    if not contract.contract_id.strip():
        blockers.append("contract_id_missing")
    if runtime.action_scope not in contract.permission_scope:
        blockers.append("action_scope_not_permitted")
    required_checks = (
        set(contract.execution_checks)
        | set(contract.evaluation_checks)
        | set(contract.rollback_checks)
    )
    missing_checks = sorted(required_checks - set(runtime.checks_passed))
    if missing_checks:
        blockers.append("required_checks_missing")
        blockers.extend(f"missing:{name}" for name in missing_checks)
    if "human_approval_required" in contract.approval_checks and not runtime.has_human_approval:
        blockers.append("human_approval_required")
    if not contract.rollback_checks:
        blockers.append("rollback_contract_missing")
    return len(blockers) == 0, tuple(blockers)
