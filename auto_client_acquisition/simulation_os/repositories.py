"""Simulation OS tenant-scoped scenarios."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(slots=True)
class SimulationScenario:
    scenario_id: str
    tenant_id: str
    name: str
    status: str = "draft"
    created_at: datetime = field(default_factory=_now)


__all__ = ["SimulationScenario"]
