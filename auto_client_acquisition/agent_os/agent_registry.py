"""Registry for governed agents (identity gate before production wiring).

In-memory map is the source of truth within a process. A JSONL audit log
mirrors registrations and status changes for durability; its path is
overridable via ``DEALIX_AGENT_REGISTRY_PATH`` (default ``var/agents.jsonl``).
"""

from __future__ import annotations

import json
import os
import threading
from collections.abc import Iterable
from pathlib import Path

from auto_client_acquisition.agent_os.agent_card import AgentCard, AgentStatus, agent_card_valid

_DEFAULT_PATH = "var/agents.jsonl"
_REGISTRY: dict[str, AgentCard] = {}
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_AGENT_REGISTRY_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _append_log(event: str, card: AgentCard) -> None:
    path = _path()
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"event": event, "agent": card.to_dict()}
    with _lock:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def register_agent(card: AgentCard) -> AgentCard:
    if not agent_card_valid(card):
        msg = "invalid_agent_card"
        raise ValueError(msg)
    if card.agent_id in _REGISTRY:
        msg = f"agent_id_already_registered:{card.agent_id}"
        raise ValueError(msg)
    _REGISTRY[card.agent_id] = card
    _append_log("registered", card)
    return card


def get_agent(agent_id: str) -> AgentCard | None:
    return _REGISTRY.get(agent_id)


def list_agents(
    *,
    status: str | None = None,
    owner: str | None = None,
) -> list[AgentCard]:
    cards: Iterable[AgentCard] = _REGISTRY.values()
    out: list[AgentCard] = []
    for card in cards:
        if status is not None and card.status != status:
            continue
        if owner is not None and card.owner != owner:
            continue
        out.append(card)
    return out


def set_agent_status(agent_id: str, status: str) -> AgentCard | None:
    """Replace an agent card with an updated status (cards are frozen)."""
    current = _REGISTRY.get(agent_id)
    if current is None:
        return None
    from dataclasses import replace

    updated = replace(current, status=status)
    _REGISTRY[agent_id] = updated
    _append_log("status_changed", updated)
    return updated


def kill_agent(agent_id: str, *, reason: str) -> AgentCard | None:
    if not reason.strip():
        msg = "kill reason is required"
        raise ValueError(msg)
    return set_agent_status(agent_id, AgentStatus.KILLED.value)


def clear_agent_registry_for_tests() -> None:
    _REGISTRY.clear()
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


# Wave 14F alias used by the agent-lifecycle test suite.
clear_for_test = clear_agent_registry_for_tests


__all__ = [
    "clear_agent_registry_for_tests",
    "clear_for_test",
    "get_agent",
    "kill_agent",
    "list_agents",
    "register_agent",
    "set_agent_status",
]
