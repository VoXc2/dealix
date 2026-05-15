"""System 28 — Assurance contract evaluation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AssuranceContract:
    action_name: str
    allow_read: bool
    allow_propose: bool
    allow_execute: bool
    required_checks: tuple[str, ...]
    rollback_required: bool
    governance_policy: str

    def __post_init__(self) -> None:
        if not self.action_name.strip():
            raise ValueError("action_name_required")
        if not self.governance_policy.strip():
            raise ValueError("governance_policy_required")


@dataclass(frozen=True)
class AssuranceEvaluation:
    allowed: bool
    decision: str
    missing_checks: tuple[str, ...]
    rollback_ready: bool
    trace_id: str
    reason: str


def evaluate_contract(
    contract: AssuranceContract,
    *,
    mode: str,
    provided_checks: set[str],
    policy_ok: bool,
    rollback_available: bool,
    trace_id: str,
) -> AssuranceEvaluation:
    clean_mode = mode.strip().lower()
    if clean_mode not in {"read", "propose", "execute"}:
        raise ValueError("invalid_mode")
    if not trace_id.strip():
        raise ValueError("trace_id_required")

    mode_allowed = {
        "read": contract.allow_read,
        "propose": contract.allow_propose,
        "execute": contract.allow_execute,
    }[clean_mode]
    if not mode_allowed:
        return AssuranceEvaluation(
            allowed=False,
            decision="BLOCK",
            missing_checks=(),
            rollback_ready=rollback_available,
            trace_id=trace_id,
            reason=f"{clean_mode}_not_permitted",
        )

    missing = tuple(
        sorted(check for check in contract.required_checks if check not in provided_checks)
    )
    if missing:
        return AssuranceEvaluation(
            allowed=False,
            decision="BLOCK",
            missing_checks=missing,
            rollback_ready=rollback_available,
            trace_id=trace_id,
            reason="missing_checks",
        )

    if not policy_ok:
        return AssuranceEvaluation(
            allowed=False,
            decision="BLOCK",
            missing_checks=(),
            rollback_ready=rollback_available,
            trace_id=trace_id,
            reason="policy_blocked",
        )

    if contract.rollback_required and not rollback_available:
        return AssuranceEvaluation(
            allowed=False,
            decision="BLOCK",
            missing_checks=(),
            rollback_ready=False,
            trace_id=trace_id,
            reason="rollback_unavailable",
        )

    return AssuranceEvaluation(
        allowed=True,
        decision="ALLOW",
        missing_checks=(),
        rollback_ready=rollback_available,
        trace_id=trace_id,
        reason="contract_satisfied",
    )
