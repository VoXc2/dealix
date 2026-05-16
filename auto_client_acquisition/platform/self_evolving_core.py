"""Self-evolving enterprise core orchestrator."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.continuous_optimization import (
    ContinuousOptimizationSummary,
    build_continuous_optimization_summary,
)
from auto_client_acquisition.platform.meta_governance import GovernanceDriftReport, assess_meta_governance
from auto_client_acquisition.platform.meta_orchestration import (
    MetaOrchestrationPlan,
    propose_meta_orchestration_changes,
)
from auto_client_acquisition.platform.org_learning import LearningCycle, run_org_learning_cycle
from auto_client_acquisition.platform.process_optimization import ProcessOptimizationResult


@dataclass(frozen=True, slots=True)
class SelfEvolvingCoreReport:
    cycle_id: str
    governance_drift: GovernanceDriftReport
    orchestration_plan: MetaOrchestrationPlan
    learning_cycle: LearningCycle
    optimization_summary: ContinuousOptimizationSummary
    ready_for_next_cycle: bool


def run_self_evolving_core(
    *,
    cycle_id: str,
    process_optimization: ProcessOptimizationResult,
    strategic_recommendations: tuple[str, ...],
    policy_violation_rate: float,
    unaudited_action_rate: float,
    approval_sla_miss_rate: float,
) -> SelfEvolvingCoreReport:
    drift = assess_meta_governance(
        policy_violation_rate=policy_violation_rate,
        unaudited_action_rate=unaudited_action_rate,
        approval_sla_miss_rate=approval_sla_miss_rate,
    )
    plan = propose_meta_orchestration_changes(optimization=process_optimization, drift=drift)
    learning_cycle = run_org_learning_cycle(
        cycle_id=cycle_id,
        recommendations=strategic_recommendations,
        optimization_actions=plan.changes,
    )
    summary = build_continuous_optimization_summary(learning_cycle=learning_cycle, plan=plan)
    ready = drift.drift_score < 0.7 and summary.optimization_score >= 0.5
    return SelfEvolvingCoreReport(
        cycle_id=cycle_id,
        governance_drift=drift,
        orchestration_plan=plan,
        learning_cycle=learning_cycle,
        optimization_summary=summary,
        ready_for_next_cycle=ready,
    )


__all__ = ['SelfEvolvingCoreReport', 'run_self_evolving_core']
