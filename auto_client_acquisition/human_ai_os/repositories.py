"""Human-AI oversight data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Delegation:
    delegation_id: str
    tenant_id: str
    run_id: str
    delegated_by: str
    delegated_to: str
    created_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class Escalation:
    escalation_id: str
    tenant_id: str
    run_id: str
    reason: str
    requested_by: str
    state: str = "pending"
    created_at: datetime = field(default_factory=_now)


__all__ = ["Delegation", "Escalation"]
