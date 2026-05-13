"""Agent Runtime States — 6 states with valid transitions."""

from __future__ import annotations

from enum import Enum


class AgentRuntimeState(str, Enum):
    SAFE = "safe"
    WATCH = "watch"
    RESTRICTED = "restricted"
    ESCALATED = "escalated"
    PAUSED = "paused"
    KILLED = "killed"


# Allowed forward transitions (the runtime may only move along these edges).
RUNTIME_STATE_TRANSITIONS: dict[AgentRuntimeState, frozenset[AgentRuntimeState]] = {
    AgentRuntimeState.SAFE: frozenset({AgentRuntimeState.WATCH, AgentRuntimeState.PAUSED, AgentRuntimeState.KILLED}),
    AgentRuntimeState.WATCH: frozenset({AgentRuntimeState.RESTRICTED, AgentRuntimeState.SAFE, AgentRuntimeState.PAUSED, AgentRuntimeState.KILLED}),
    AgentRuntimeState.RESTRICTED: frozenset({AgentRuntimeState.ESCALATED, AgentRuntimeState.WATCH, AgentRuntimeState.PAUSED, AgentRuntimeState.KILLED}),
    AgentRuntimeState.ESCALATED: frozenset({AgentRuntimeState.PAUSED, AgentRuntimeState.KILLED, AgentRuntimeState.RESTRICTED}),
    AgentRuntimeState.PAUSED: frozenset({AgentRuntimeState.SAFE, AgentRuntimeState.KILLED}),
    AgentRuntimeState.KILLED: frozenset(),  # terminal
}


def is_valid_transition(src: AgentRuntimeState, dst: AgentRuntimeState) -> bool:
    return dst in RUNTIME_STATE_TRANSITIONS[src]
