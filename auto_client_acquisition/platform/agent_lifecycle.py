"""Agent lifecycle and safe transition rules."""

from __future__ import annotations

from enum import StrEnum


class AgentLifecycleState(StrEnum):
    DRAFT = 'draft'
    STAGING = 'staging'
    PRODUCTION = 'production'
    SUSPENDED = 'suspended'
    RETIRED = 'retired'


_ALLOWED_TRANSITIONS: dict[AgentLifecycleState, frozenset[AgentLifecycleState]] = {
    AgentLifecycleState.DRAFT: frozenset({AgentLifecycleState.STAGING, AgentLifecycleState.RETIRED}),
    AgentLifecycleState.STAGING: frozenset(
        {AgentLifecycleState.PRODUCTION, AgentLifecycleState.SUSPENDED, AgentLifecycleState.RETIRED}
    ),
    AgentLifecycleState.PRODUCTION: frozenset(
        {AgentLifecycleState.SUSPENDED, AgentLifecycleState.RETIRED}
    ),
    AgentLifecycleState.SUSPENDED: frozenset(
        {AgentLifecycleState.STAGING, AgentLifecycleState.RETIRED}
    ),
    AgentLifecycleState.RETIRED: frozenset(),
}


def lifecycle_transition_allowed(current: AgentLifecycleState, target: AgentLifecycleState) -> bool:
    if current == target:
        return True
    return target in _ALLOWED_TRANSITIONS[current]


def lifecycle_allows_live_execution(state: AgentLifecycleState) -> bool:
    return state == AgentLifecycleState.PRODUCTION


__all__ = [
    'AgentLifecycleState',
    'lifecycle_allows_live_execution',
    'lifecycle_transition_allowed',
]
