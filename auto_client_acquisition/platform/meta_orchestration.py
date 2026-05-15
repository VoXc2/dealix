"""Meta-orchestration updates."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.platform.meta_governance import GovernanceDriftReport
from auto_client_acquisition.platform.process_optimization import ProcessOptimizationResult


@dataclass(frozen=True, slots=True)
class MetaOrchestrationPlan:
    version: str
    changes: tuple[str, ...]
    rollback_ready: bool


def propose_meta_orchestration_changes(
    *, optimization: ProcessOptimizationResult, drift: GovernanceDriftReport
) -> MetaOrchestrationPlan:
    changes = list(optimization.recommendations)
    if drift.violations:
        changes.append('enforce_governance_runtime_hard_gates')
    if not changes:
        changes.append('no_change_monitor_only')
    return MetaOrchestrationPlan(version='1.0.0', changes=tuple(changes), rollback_ready=True)


__all__ = ['MetaOrchestrationPlan', 'propose_meta_orchestration_changes']
