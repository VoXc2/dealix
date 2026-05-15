"""Registry for governed agents (identity gate before production wiring).

In-memory module-global, optionally backed by a JSONL file when
``DEALIX_AGENT_REGISTRY_PATH`` is set so registrations survive a process
restart in long-running deployments.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import replace
from pathlib import Path

from auto_client_acquisition.agent_os.agent_card import (
    AgentCard,
    AgentStatus,
    agent_card_valid,
)

_REGISTRY: dict[str, AgentCard] = {}
_lock = threading.RLock()
_STATE: dict[str, bool] = {"loaded": False}


def _path() -> Path | None:
    raw = os.environ.get("DEALIX_AGENT_REGISTRY_PATH")
    if not raw:
        return None
    p = Path(raw)
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _persist() -> None:
    path = _path()
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for card in _REGISTRY.values():
            f.write(json.dumps(card.to_dict(), ensure_ascii=False) + "\n")


def _load_if_needed() -> None:
    if _STATE["loaded"]:
        return
    _STATE["loaded"] = True
    path = _path()
    if path is None or not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                card = AgentCard(**data)
            except Exception:  # noqa: BLE001
                continue
            _REGISTRY[card.agent_id] = card


def register_agent(card: AgentCard) -> AgentCard:
    """Register a validated agent card. Raises ``ValueError`` on bad input."""
    if not agent_card_valid(card):
        raise ValueError("invalid_agent_card")
    with _lock:
        _load_if_needed()
        if card.agent_id in _REGISTRY:
            raise ValueError(f"agent_id already registered: {card.agent_id}")
        _REGISTRY[card.agent_id] = card
        _persist()
    return card


def get_agent(agent_id: str) -> AgentCard | None:
    with _lock:
        _load_if_needed()
        return _REGISTRY.get(agent_id)


def list_agents(
    *,
    status: str | None = None,
    owner: str | None = None,
) -> list[AgentCard]:
    """List registered agents, optionally filtered by status and/or owner."""
    with _lock:
        _load_if_needed()
        cards = list(_REGISTRY.values())
    if status is not None:
        cards = [c for c in cards if c.status == status]
    if owner is not None:
        cards = [c for c in cards if c.owner == owner]
    return cards


def kill_agent(agent_id: str, *, reason: str) -> AgentCard | None:
    """Mark an agent as killed. Requires a non-empty reason."""
    if not (reason and reason.strip()):
        raise ValueError("kill reason is required")
    with _lock:
        _load_if_needed()
        existing = _REGISTRY.get(agent_id)
        if existing is None:
            return None
        killed = replace(
            existing,
            status=AgentStatus.KILLED.value,
            killed_reason=reason.strip(),
        )
        _REGISTRY[agent_id] = killed
        _persist()
    return killed


def clear_agent_registry_for_tests() -> None:
    with _lock:
        _REGISTRY.clear()
        _STATE["loaded"] = False
        path = _path()
        if path is not None and path.exists():
            path.write_text("", encoding="utf-8")


# Alias used by the agent_os test suite and the JSONL-store convention.
clear_for_test = clear_agent_registry_for_tests


__all__ = [
    "clear_agent_registry_for_tests",
    "clear_for_test",
    "get_agent",
    "kill_agent",
    "list_agents",
    "register_agent",
]
