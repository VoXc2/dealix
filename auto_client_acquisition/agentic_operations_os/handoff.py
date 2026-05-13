"""Agent → Human handoff record."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentHandoff:
    handoff_id: str
    agent_id: str
    output_id: str
    handoff_to: str
    reason: str
    required_action: str
    deadline: str

    def __post_init__(self) -> None:
        if not self.handoff_to:
            raise ValueError("handoff_to_required")
        if not self.required_action:
            raise ValueError("required_action_required")
        if not self.reason:
            raise ValueError("reason_required")
