"""Sandbox OS repositories."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class SandboxRun:
    sandbox_id: str
    tenant_id: str
    run_id: str
    status: str = "running"
    created_at: datetime = field(default_factory=_now)


@dataclass(slots=True)
class CanaryRollout:
    rollout_id: str
    tenant_id: str
    target: str
    status: str = "planned"
    created_at: datetime = field(default_factory=_now)


__all__ = ["CanaryRollout", "SandboxRun"]
