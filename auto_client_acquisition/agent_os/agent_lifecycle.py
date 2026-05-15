"""Agent lifecycle — states, production gate, and kill transition."""

from __future__ import annotations

from dataclasses import replace
from enum import StrEnum

from auto_client_acquisition.agent_os.agent_card import AgentCard
from auto_client_acquisition.agent_os.agent_registry import get_agent, update_agent
from auto_client_acquisition.agent_os.agent_status import AgentStatus


class AgentLifecycleState(StrEnum):
    DRAFT = "draft"
    STAGING = "staging"
    PRODUCTION = "production"
    SUSPENDED = "suspended"
    RETIRED = "retired"


def lifecycle_allows_production_tools(state: AgentLifecycleState) -> bool:
    return state == AgentLifecycleState.PRODUCTION


def kill_agent(agent_id: str, reason: str) -> AgentCard:
    """Kill a registered agent — sets status KILLED and records the reason.

    Raises ValueError on a blank reason or an unknown agent.
    """
    if not reason or not reason.strip():
        raise ValueError("kill reason is required")
    card = get_agent(agent_id)
    if card is None:
        raise ValueError(f"unknown agent: {agent_id}")
    killed = replace(
        card,
        status=AgentStatus.KILLED.value,
        killed_reason=reason.strip(),
    )
    return update_agent(killed)


__all__ = [
    "AgentLifecycleState",
    "kill_agent",
    "lifecycle_allows_production_tools",
]
