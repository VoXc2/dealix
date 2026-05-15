"""Continuous optimization summary."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.meta_orchestration import MetaOrchestrationPlan
from auto_client_acquisition.platform.org_learning import LearningCycle


@dataclass(frozen=True, slots=True)
class ContinuousOptimizationSummary:
    optimization_score: float
    next_cycle_focus: str
    actions: tuple[str, ...]


def build_continuous_optimization_summary(
    *, learning_cycle: LearningCycle, plan: MetaOrchestrationPlan
) -> ContinuousOptimizationSummary:
    adopted = len(learning_cycle.adopted_actions)
    planned = max(1, len(plan.changes))
    score = round(min(adopted / planned, 1.0), 4)
    focus = 'governance_hardening' if 'enforce_governance_runtime_hard_gates' in plan.changes else 'latency_and_cost'
    return ContinuousOptimizationSummary(
        optimization_score=score,
        next_cycle_focus=focus,
        actions=plan.changes,
    )


__all__ = ['ContinuousOptimizationSummary', 'build_continuous_optimization_summary']
