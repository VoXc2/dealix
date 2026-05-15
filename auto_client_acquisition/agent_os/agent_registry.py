"""Governed agent registry.

In-memory source of truth for reads, with an append-only JSONL audit trail
when ``DEALIX_AGENT_REGISTRY_PATH`` is set. Doctrine: every agent registration
and kill is recorded.
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path

from auto_client_acquisition.agent_os.agent_card import AgentCard, agent_card_valid

_DEFAULT_PATH = "var/agent-registry.jsonl"
_lock = threading.RLock()
_REGISTRY: dict[str, AgentCard] = {}


def _path() -> Path | None:
    """Resolve the JSONL audit path, or None when persistence is disabled."""
    raw = os.environ.get("DEALIX_AGENT_REGISTRY_PATH")
    if raw is None:
        return None
    p = Path(raw or _DEFAULT_PATH)
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _append(card: AgentCard) -> None:
    path = _path()
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(card.to_dict(), ensure_ascii=False) + "\n")


def register_agent(card: AgentCard) -> AgentCard:
    """Register a new agent. Raises on an invalid card or a duplicate id."""
    if not agent_card_valid(card):
        raise ValueError("invalid_agent_card")
    with _lock:
        if card.agent_id in _REGISTRY:
            raise ValueError(f"duplicate agent_id: {card.agent_id}")
        _REGISTRY[card.agent_id] = card
        _append(card)
    return card


def update_agent(card: AgentCard) -> AgentCard:
    """Replace an already-registered agent (used by lifecycle transitions)."""
    if not agent_card_valid(card):
        raise ValueError("invalid_agent_card")
    with _lock:
        if card.agent_id not in _REGISTRY:
            raise ValueError(f"unknown agent: {card.agent_id}")
        _REGISTRY[card.agent_id] = card
        _append(card)
    return card


def get_agent(agent_id: str) -> AgentCard | None:
    with _lock:
        return _REGISTRY.get(agent_id)


def list_agents(
    status: str | None = None,
    owner: str | None = None,
) -> list[AgentCard]:
    with _lock:
        cards = list(_REGISTRY.values())
    if status is not None:
        cards = [c for c in cards if c.status == status]
    if owner is not None:
        cards = [c for c in cards if c.owner == owner]
    return sorted(cards, key=lambda c: c.agent_id)


def clear_for_test() -> None:
    """Reset the in-memory registry and truncate the JSONL audit file."""
    with _lock:
        _REGISTRY.clear()
        path = _path()
        if path is not None and path.exists():
            path.write_text("", encoding="utf-8")


# Legacy alias — kept for existing importers.
clear_agent_registry_for_tests = clear_for_test


__all__ = [
    "clear_agent_registry_for_tests",
    "clear_for_test",
    "get_agent",
    "list_agents",
    "register_agent",
    "update_agent",
]
