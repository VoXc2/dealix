"""Agent Transparency Card — shown alongside any agent-involved output."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.endgame_os.agent_control import AutonomyLevel


@dataclass(frozen=True)
class AgentTransparencyCard:
    agent: str
    task: str
    autonomy_level: AutonomyLevel
    human_owner: str
    external_action_allowed: bool
    approval_required: bool
    audit_event: str | None = None
