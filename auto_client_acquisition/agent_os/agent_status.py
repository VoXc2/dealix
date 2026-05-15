"""Agent lifecycle status values for the governed registry."""

from __future__ import annotations

from enum import StrEnum


class AgentStatus(StrEnum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    KILLED = "killed"
    RETIRED = "retired"


DEFAULT_STATUS: AgentStatus = AgentStatus.PROPOSED


def valid_status(value: str) -> bool:
    return value in {s.value for s in AgentStatus}


__all__ = ["DEFAULT_STATUS", "AgentStatus", "valid_status"]
