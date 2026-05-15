"""System 35 — Controlled self-evolution recommendations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OptimizationProposal:
    proposal_id: str
    target_workflow: str
    change_summary: str
    expected_kpi_gain: float
    governance_checks: tuple[str, ...]
    requires_human_approval: bool
    risk_level: str

    def __post_init__(self) -> None:
        if not self.proposal_id.strip():
            raise ValueError("proposal_id_required")
        if not self.target_workflow.strip():
            raise ValueError("target_workflow_required")
        if not self.change_summary.strip():
            raise ValueError("change_summary_required")
        if self.risk_level not in {"low", "medium", "high"}:
            raise ValueError("invalid_risk_level")


@dataclass(frozen=True)
class EvolutionCycleInput:
    previous_kpi: float
    current_kpi: float
    incident_count: int
    policy_violations: int
    proposal: OptimizationProposal


def recommend_evolution(cycle: EvolutionCycleInput) -> tuple[bool, str]:
    if cycle.policy_violations > 0:
        return False, "governance_block_policy_violations"
    if cycle.proposal.risk_level == "high" and not cycle.proposal.requires_human_approval:
        return False, "high_risk_requires_human_approval"
    if not cycle.proposal.governance_checks:
        return False, "governance_checks_missing"
    if cycle.incident_count > 3:
        return False, "stability_block_incident_spike"
    if cycle.current_kpi < cycle.previous_kpi:
        return False, "rollback_and_recalibrate"
    return True, "apply_canary_optimization"


def continuous_optimization_ready(*, pass_rate: float, regression_cycles: int) -> bool:
    if not 0.0 <= pass_rate <= 1.0:
        raise ValueError("pass_rate_out_of_range")
    if regression_cycles < 0:
        raise ValueError("regression_cycles_invalid")
    return pass_rate >= 0.95 and regression_cycles == 0
