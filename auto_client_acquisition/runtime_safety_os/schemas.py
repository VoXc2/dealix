"""Runtime safety schemas."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class KillSwitchState:
    tenant_id: str
    agent_id: str
    enabled: bool
    reason: str = ""
    activated_by: str = ""
    activated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class CircuitBreakerState:
    tenant_id: str
    breaker_key: str
    failure_count: int = 0
    threshold: int = 3
    status: str = "closed"
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
