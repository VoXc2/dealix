"""System 29 — Sandbox, simulation, canary, replay gates."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SandboxExecutionPlan:
    workflow_id: str
    simulation_passed: bool
    canary_percent: float
    replay_ready: bool
    rollback_ready: bool
    staged_environment: str


def sandbox_gate(plan: SandboxExecutionPlan) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not plan.workflow_id.strip():
        errors.append("workflow_id_required")
    if not plan.simulation_passed:
        errors.append("simulation_failed")
    if plan.canary_percent <= 0 or plan.canary_percent > 100:
        errors.append("canary_percent_invalid")
    if not plan.replay_ready:
        errors.append("replay_missing")
    if not plan.rollback_ready:
        errors.append("rollback_missing")
    if not plan.staged_environment.strip():
        errors.append("staged_environment_required")
    return (not errors, tuple(errors))


def promote_from_canary(
    plan: SandboxExecutionPlan,
    *,
    observed_error_rate: float,
    max_error_rate: float = 0.02,
) -> bool:
    ok, _errs = sandbox_gate(plan)
    if not ok:
        return False
    if observed_error_rate < 0 or max_error_rate < 0:
        return False
    return observed_error_rate <= max_error_rate
