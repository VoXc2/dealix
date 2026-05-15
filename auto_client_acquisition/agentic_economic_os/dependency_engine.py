"""Organizational dependency scoring for infrastructure status."""

from __future__ import annotations

from dataclasses import dataclass


def _ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    if numerator < 0:
        raise ValueError("numerator must be >= 0")
    return min(1.0, numerator / denominator)


@dataclass(frozen=True)
class DependencySignals:
    """Measured execution and governance signals from operations."""

    core_processes_on_dealix: int
    core_processes_total: int
    workflows_total: int
    traceable_workflows: int
    pausable_workflows: int
    rollbackable_workflows: int
    auditable_workflows: int
    reroutable_workflows: int
    governed_external_actions: int
    external_actions_total: int
    self_healed_failures: int
    failures_total: int
    executive_decisions_via_dealix: int
    executive_decisions_total: int
    bypass_attempts_blocked: int
    bypass_attempts_total: int


@dataclass(frozen=True)
class DependencyScorecard:
    """Computed dependency metrics and total score."""

    organizational_dependency_index: float
    process_dependency_pct: float
    execution_control_pct: float
    governance_dependency_pct: float
    recovery_autonomy_pct: float
    executive_dependency_pct: float
    no_bypass_rate_pct: float
    weights_version: str = "v1"


@dataclass(frozen=True)
class InfrastructureThresholds:
    """Hard gates for infrastructure status."""

    odi_min: float = 75.0
    no_bypass_min: float = 98.0
    rollback_min: float = 90.0
    audit_min: float = 95.0
    executive_dependency_min: float = 60.0


def compute_dependency_scorecard(signals: DependencySignals) -> DependencyScorecard:
    """Compute ODI and all primary dependency metrics."""
    process_dependency = _ratio(signals.core_processes_on_dealix, signals.core_processes_total)

    execution_axes = (
        _ratio(signals.traceable_workflows, signals.workflows_total),
        _ratio(signals.pausable_workflows, signals.workflows_total),
        _ratio(signals.rollbackable_workflows, signals.workflows_total),
        _ratio(signals.auditable_workflows, signals.workflows_total),
        _ratio(signals.reroutable_workflows, signals.workflows_total),
    )
    execution_control = sum(execution_axes) / len(execution_axes)

    governance_dependency = _ratio(signals.governed_external_actions, signals.external_actions_total)
    recovery_autonomy = _ratio(signals.self_healed_failures, signals.failures_total)
    executive_dependency = _ratio(signals.executive_decisions_via_dealix, signals.executive_decisions_total)
    no_bypass_rate = _ratio(signals.bypass_attempts_blocked, signals.bypass_attempts_total)

    # Weights reflect the operator thesis: dependency on operations beats pure model quality.
    odi = (
        process_dependency * 0.25
        + execution_control * 0.20
        + governance_dependency * 0.20
        + recovery_autonomy * 0.15
        + executive_dependency * 0.10
        + no_bypass_rate * 0.10
    ) * 100

    return DependencyScorecard(
        organizational_dependency_index=round(odi, 2),
        process_dependency_pct=round(process_dependency * 100, 2),
        execution_control_pct=round(execution_control * 100, 2),
        governance_dependency_pct=round(governance_dependency * 100, 2),
        recovery_autonomy_pct=round(recovery_autonomy * 100, 2),
        executive_dependency_pct=round(executive_dependency * 100, 2),
        no_bypass_rate_pct=round(no_bypass_rate * 100, 2),
    )


def infrastructure_status(
    signals: DependencySignals,
    *,
    thresholds: InfrastructureThresholds | None = None,
) -> dict[str, object]:
    """Evaluate whether Dealix has reached infrastructure status."""
    scorecard = compute_dependency_scorecard(signals)
    gates = thresholds or InfrastructureThresholds()

    gate_results = {
        "odi_gate": scorecard.organizational_dependency_index >= gates.odi_min,
        "no_bypass_gate": scorecard.no_bypass_rate_pct >= gates.no_bypass_min,
        "rollback_gate": _ratio(signals.rollbackable_workflows, signals.workflows_total) * 100 >= gates.rollback_min,
        "audit_gate": _ratio(signals.auditable_workflows, signals.workflows_total) * 100 >= gates.audit_min,
        "executive_dependency_gate": scorecard.executive_dependency_pct >= gates.executive_dependency_min,
    }
    reached = all(gate_results.values())

    return {
        "infrastructure_status": reached,
        "scorecard": scorecard,
        "gate_results": gate_results,
    }
