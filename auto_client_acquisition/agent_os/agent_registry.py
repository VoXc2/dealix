"""In-memory registry for governed agents (identity gate before production wiring)."""

from __future__ import annotations

from collections.abc import Mapping

from auto_client_acquisition.agent_os.agent_card import AgentCard, agent_card_valid

_REGISTRY: dict[str, AgentCard] = {}


def register_agent(card: AgentCard) -> None:
    if not agent_card_valid(card):
        msg = "invalid_agent_card"
        raise ValueError(msg)
    _REGISTRY[card.agent_id] = card


def get_agent(agent_id: str) -> AgentCard | None:
    return _REGISTRY.get(agent_id)


def list_agents() -> Mapping[str, AgentCard]:
    return dict(_REGISTRY)


def clear_agent_registry_for_tests() -> None:
    _REGISTRY.clear()


__all__ = ["clear_agent_registry_for_tests", "get_agent", "list_agents", "register_agent"]
