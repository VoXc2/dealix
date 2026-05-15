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


def get_agent(agent_id: str, *, tenant_id: str | None = None) -> AgentCard | None:
    """Fetch an agent. When ``tenant_id`` is given, a card belonging to a
    different tenant is treated as not found (tenant isolation)."""
    card = _REGISTRY.get(agent_id)
    if card is None:
        return None
    if tenant_id is not None and card.tenant_id != tenant_id:
        return None
    return card


def list_agents(*, tenant_id: str | None = None) -> Mapping[str, AgentCard]:
    """All agents, optionally scoped to a single tenant."""
    if tenant_id is None:
        return dict(_REGISTRY)
    return {k: v for k, v in _REGISTRY.items() if v.tenant_id == tenant_id}


def clear_agent_registry_for_tests() -> None:
    _REGISTRY.clear()


__all__ = ["clear_agent_registry_for_tests", "get_agent", "list_agents", "register_agent"]
