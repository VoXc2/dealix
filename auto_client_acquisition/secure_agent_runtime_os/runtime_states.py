"""Runtime states — finite state machine for agent runtime supervision."""
from __future__ import annotations

from enum import StrEnum


class RuntimeState(StrEnum):
    SAFE = "safe"
    WATCH = "watch"
    RESTRICTED = "restricted"
    ESCALATED = "escalated"
    PAUSED = "paused"
    KILLED = "killed"


# Allowed transitions: from → set of legal "to" states.
_TRANSITIONS: dict[str, frozenset[str]] = {
    RuntimeState.SAFE.value: frozenset({
        RuntimeState.WATCH.value, RuntimeState.RESTRICTED.value,
        RuntimeState.PAUSED.value, RuntimeState.KILLED.value,
    }),
    RuntimeState.WATCH.value: frozenset({
        RuntimeState.SAFE.value, RuntimeState.RESTRICTED.value,
        RuntimeState.ESCALATED.value, RuntimeState.PAUSED.value,
        RuntimeState.KILLED.value,
    }),
    RuntimeState.RESTRICTED.value: frozenset({
        RuntimeState.WATCH.value, RuntimeState.ESCALATED.value,
        RuntimeState.PAUSED.value, RuntimeState.KILLED.value,
    }),
    RuntimeState.ESCALATED.value: frozenset({
        RuntimeState.RESTRICTED.value, RuntimeState.PAUSED.value,
        RuntimeState.KILLED.value,
    }),
    RuntimeState.PAUSED.value: frozenset({
        RuntimeState.WATCH.value, RuntimeState.KILLED.value,
    }),
    RuntimeState.KILLED.value: frozenset(),  # terminal
}


def can_transition(from_state: str | RuntimeState, to_state: str | RuntimeState) -> bool:
    fs = from_state.value if isinstance(from_state, RuntimeState) else str(from_state)
    ts = to_state.value if isinstance(to_state, RuntimeState) else str(to_state)
    return ts in _TRANSITIONS.get(fs, frozenset())


def is_safe_to_run(state: str | RuntimeState) -> bool:
    s = state.value if isinstance(state, RuntimeState) else str(state)
    return s in {RuntimeState.SAFE.value, RuntimeState.WATCH.value}


__all__ = ["RuntimeState", "can_transition", "is_safe_to_run"]
