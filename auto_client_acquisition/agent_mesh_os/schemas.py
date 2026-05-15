"""Agent Mesh schemas."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class AgentDescriptor:
    agent_id: str
    tenant_id: str
    name: str
    owner: str
    capabilities: list[str]
    trust_tier: str
    status: str
    autonomy_level: int
    tool_permissions: list[str] = field(default_factory=list)
    endpoint: str = ""
    composite_score: float = 0.0
    registered_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
