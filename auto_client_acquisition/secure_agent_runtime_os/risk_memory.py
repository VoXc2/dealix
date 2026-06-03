"""Stateful risk memory — lightweight ring buffer of recent risk codes."""

from __future__ import annotations

from collections import deque

_MAX = 128
_MEMORY: dict[str, deque[str]] = {}


def append_risk(agent_id: str, code: str) -> None:
    q = _MEMORY.setdefault(agent_id, deque(maxlen=_MAX))
    q.append(code.strip())


def recent_risks(agent_id: str) -> tuple[str, ...]:
    return tuple(_MEMORY.get(agent_id, ()))


def clear_risk_memory_for_tests() -> None:
    _MEMORY.clear()


__all__ = ["append_risk", "clear_risk_memory_for_tests", "recent_risks"]
