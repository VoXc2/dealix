"""JSONL-backed registry for governed agents (identity gate before wiring).

Persistence: append-only JSONL at ``DEALIX_AGENT_REGISTRY_PATH`` (dev fallback
``var/agent-registry.jsonl``). Each line is the latest snapshot of a card;
``kill_agent`` appends an updated snapshot and the loader keeps the last one.
"""

from __future__ import annotations

import json
import os
import threading
from datetime import UTC, datetime
from pathlib import Path

from auto_client_acquisition.agent_os.agent_card import AgentCard, AgentStatus, agent_card_valid

_DEFAULT_PATH = "var/agent-registry.jsonl"
_lock = threading.Lock()


def _path() -> Path:
    p = Path(os.environ.get("DEALIX_AGENT_REGISTRY_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _load() -> dict[str, AgentCard]:
    path = _path()
    if not path.exists():
        return {}
    registry: dict[str, AgentCard] = {}
    with _lock, path.open("r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            try:
                card = AgentCard.from_dict(json.loads(line))
            except (json.JSONDecodeError, TypeError, ValueError):
                continue
            registry[card.agent_id] = card
    return registry


def _append(card: AgentCard) -> None:
    path = _path()
    _ensure_dir(path)
    with _lock, path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(card.to_dict(), ensure_ascii=False) + "\n")


def register_agent(card: AgentCard) -> None:
    if not agent_card_valid(card):
        raise ValueError("invalid_agent_card")
    if card.agent_id in _load():
        raise ValueError(f"agent_id '{card.agent_id}' is already registered")
    stamped = card if card.created_at else card.__class__(
        agent_id=card.agent_id,
        name=card.name,
        owner=card.owner,
        purpose=card.purpose,
        autonomy_level=card.autonomy_level,
        status=card.status,
        kill_switch_owner=card.kill_switch_owner,
        allowed_tools=card.allowed_tools,
        created_at=datetime.now(UTC).isoformat(),
    )
    _append(stamped)


def get_agent(agent_id: str) -> AgentCard | None:
    return _load().get(agent_id)


def list_agents(*, status: str | AgentStatus | None = None) -> list[AgentCard]:
    cards = list(_load().values())
    if status is None:
        return cards
    status_value = status.value if isinstance(status, AgentStatus) else str(status)
    return [c for c in cards if c.status == status_value]


def kill_agent(agent_id: str, *, reason: str) -> AgentCard | None:
    if not reason.strip():
        raise ValueError("reason is required to kill an agent")
    card = get_agent(agent_id)
    if card is None:
        return None
    killed = card.with_status(AgentStatus.KILLED.value)
    _append(killed)
    return killed


def clear_agent_registry_for_tests() -> None:
    path = _path()
    if path.exists():
        with _lock:
            path.write_text("", encoding="utf-8")


# Alias used by Wave 14F test fixtures.
clear_for_test = clear_agent_registry_for_tests


__all__ = [
    "clear_agent_registry_for_tests",
    "clear_for_test",
    "get_agent",
    "kill_agent",
    "list_agents",
    "register_agent",
]
