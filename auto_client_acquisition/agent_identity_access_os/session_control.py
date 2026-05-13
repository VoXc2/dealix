"""Agent Session — scoped runtime context."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AgentSession:
    session_id: str
    agent_id: str
    client_id: str
    project_id: str
    task: str
    allowed_tools: tuple[str, ...]
    expires_at: datetime
    status: str  # active | paused | expired | killed

    def __post_init__(self) -> None:
        if not self.session_id:
            raise ValueError("session_id_required")
        if not self.client_id:
            raise ValueError("client_id_required_no_cross_client_sessions")
        if not self.project_id:
            raise ValueError("project_id_required")
        if not self.allowed_tools:
            raise ValueError("session_requires_explicit_tool_list")
        if self.status not in {"active", "paused", "expired", "killed"}:
            raise ValueError("invalid_status")
