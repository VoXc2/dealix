"""Agent lifecycle states for governed production promotion."""

from __future__ import annotations

from enum import StrEnum


class AgentLifecycleState(StrEnum):
    DRAFT = "draft"
    STAGING = "staging"
    PRODUCTION = "production"
    SUSPENDED = "suspended"
    RETIRED = "retired"


def lifecycle_allows_production_tools(state: AgentLifecycleState) -> bool:
    return state == AgentLifecycleState.PRODUCTION


__all__ = ["AgentLifecycleState", "lifecycle_allows_production_tools"]
