"""Workflow governance contract checks."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowGovernanceStatus:
    owner: str
    sla_minutes: int
    metrics_available: bool
    rollbackable: bool
    evals_enabled: bool


def assess_workflow_governance(status: WorkflowGovernanceStatus) -> tuple[bool, tuple[str, ...]]:
    failures: list[str] = []
    if not status.owner.strip():
        failures.append('workflow_owner_missing')
    if status.sla_minutes <= 0:
        failures.append('workflow_sla_invalid')
    if not status.metrics_available:
        failures.append('workflow_metrics_missing')
    if not status.rollbackable:
        failures.append('workflow_not_rollbackable')
    if not status.evals_enabled:
        failures.append('workflow_evals_disabled')
    return len(failures) == 0, tuple(failures)


__all__ = ['WorkflowGovernanceStatus', 'assess_workflow_governance']
