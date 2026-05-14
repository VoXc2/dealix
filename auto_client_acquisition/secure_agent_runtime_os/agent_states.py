"""Agent runtime states for Secure Agent Runtime (assurance loop)."""

from __future__ import annotations

from enum import StrEnum


class AgentRuntimeState(StrEnum):
    SAFE = "SAFE"
    WATCH = "WATCH"
    RESTRICTED = "RESTRICTED"
    ESCALATED = "ESCALATED"
    PAUSED = "PAUSED"
    KILLED = "KILLED"


__all__ = ["AgentRuntimeState"]
