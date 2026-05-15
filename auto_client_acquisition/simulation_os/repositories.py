"""Simulation OS tenant-scoped scenarios."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class SimulationScenario:
    scenario_id: str
    tenant_id: str
    name: str
    status: str = "draft"
    created_at: datetime = field(default_factory=_now)


__all__ = ["SimulationScenario"]
