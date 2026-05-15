"""Agent governance checks for scale-safe autonomy."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AgentGovernanceStatus:
    registered: bool
    versioned: bool
    governed: bool
    observable: bool
    evaluated_score: float
    rollbackable: bool
    memory_scope: str


def assess_agent_governance(status: AgentGovernanceStatus) -> tuple[bool, tuple[str, ...]]:
    failures: list[str] = []
    if not status.registered:
        failures.append('agent_not_registered')
    if not status.versioned:
        failures.append('agent_not_versioned')
    if not status.governed:
        failures.append('agent_not_governed')
    if not status.observable:
        failures.append('agent_not_observable')
    if status.evaluated_score < 0.8:
        failures.append('agent_eval_below_threshold')
    if not status.rollbackable:
        failures.append('agent_not_rollbackable')
    if not status.memory_scope.strip():
        failures.append('agent_memory_scope_missing')
    return len(failures) == 0, tuple(failures)


__all__ = ['AgentGovernanceStatus', 'assess_agent_governance']
