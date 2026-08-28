"""V18 Event Portfolio Optimizer (Workstream G / §14).

Joint Big 5 / LEAP / DeepFest allocation. No physically impossible
schedules: allocations that overlap in time across different venues are
conflicts and are rejected. Exhibitor ≠ lead; only real interaction
creates relationship evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.portfolio_os.capacity import (
    CapacityAllocation,
    allocate_capacity,
)

# Canonical event windows (reverify before execution; per V18 config).
CANONICAL_EVENT_WINDOWS: dict[str, dict[str, str]] = {
    "BIG5": {
        "start": "2026-08-30",
        "end": "2026-09-02",
        "hours": "16:00-22:00",
        "venue": "Riyadh Front / ROSHN Front",
        "focus": "construction, hvac, fm, industrial, contractor, distribution, operations",
    },
    "LEAP": {
        "start": "2026-08-31",
        "end": "2026-09-03",
        "hours": "09:00-18:00",
        "venue": "RECC Malham",
        "focus": "saudi_b2b_saas, business_services, ai_it, si, partners, enterprise_tech, innovation_buyers",
    },
    "DEEPFEST": {
        "start": "2026-08-31",
        "end": "2026-09-03",
        "hours": "09:00-18:00",
        "venue": "RECC Malham",
        "focus": "ai_adoption, ai_governance, enterprise_ai, agentic_ai, ai_partners",
    },
}


@dataclass(frozen=True, slots=True)
class EventWindow:
    name: str
    start: str
    end: str
    hours: str
    venue: str
    focus: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "name": self.name,
            "start": self.start,
            "end": self.end,
            "hours": self.hours,
            "venue": self.venue,
            "focus": self.focus,
        }


def canonical_event_windows() -> list[EventWindow]:
    return [
        EventWindow(
            name=name,
            start=w["start"],
            end=w["end"],
            hours=w["hours"],
            venue=w["venue"],
            focus=w["focus"],
        )
        for name, w in CANONICAL_EVENT_WINDOWS.items()
    ]


@dataclass(frozen=True, slots=True)
class EventAllocation:
    """One planned block: event + day + time window + expected value inputs."""

    allocation_id: str
    event_name: str
    day: str  # ISO date
    start_hour: int  # 0..23
    end_hour: int  # 0..23, exclusive
    venue: str
    focus: str = ""
    expected_relationship_value: int = 0  # 0..5
    probability: float = 0.3  # 0..1 ordinal
    strategic_reuse: int = 0  # 0..5
    travel_cost: int = 1  # 0..5
    founder_hours: int = 1

    def overlaps(self, other: "EventAllocation") -> bool:
        """Same day, overlapping hours, different venue → physical conflict."""
        if self.day != other.day:
            return False
        if self.venue == other.venue:
            return False
        return self.start_hour < other.end_hour and other.start_hour < self.end_hour

    def score(self) -> float:
        return (
            (self.expected_relationship_value + 1)
            * self.probability
            * (self.strategic_reuse + 1)
            / max(1, self.travel_cost + 1)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "allocation_id": self.allocation_id,
            "event_name": self.event_name,
            "day": self.day,
            "start_hour": self.start_hour,
            "end_hour": self.end_hour,
            "venue": self.venue,
            "focus": self.focus,
            "expected_relationship_value": self.expected_relationship_value,
            "probability": self.probability,
            "strategic_reuse": self.strategic_reuse,
            "travel_cost": self.travel_cost,
            "founder_hours": self.founder_hours,
            "score": round(self.score(), 3),
        }


@dataclass(frozen=True, slots=True)
class EventConflict:
    allocation_id_a: str
    allocation_id_b: str
    day: str
    reason: str = "PHYSICAL_OVERLAP_DIFFERENT_VENUE"

    def to_dict(self) -> dict[str, str]:
        return {
            "allocation_id_a": self.allocation_id_a,
            "allocation_id_b": self.allocation_id_b,
            "day": self.day,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class OptimizedEventPlan:
    allocations: tuple[EventAllocation, ...]
    conflicts: tuple[EventConflict, ...] = ()
    capacity_feasible: bool = False
    capacity_violations: tuple[str, ...] = ()
    founder_hours_total: int = 0

    @property
    def feasible(self) -> bool:
        return not self.conflicts and self.capacity_feasible

    def to_dict(self) -> dict[str, Any]:
        return {
            "feasible": self.feasible,
            "allocations": [a.to_dict() for a in self.allocations],
            "conflicts": [c.to_dict() for c in self.conflicts],
            "capacity_feasible": self.capacity_feasible,
            "capacity_violations": list(self.capacity_violations),
            "founder_hours_total": self.founder_hours_total,
        }


def _parse_hours(hours: str) -> tuple[int, int]:
    start_s, end_s = hours.split("-", 1)
    return int(start_s.split(":")[0]), int(end_s.split(":")[0])


def optimize_event_plan(
    allocations: list[EventAllocation],
    *,
    event_hours_cap: int = 20,
    founder_minutes_cap: int = 600,
) -> OptimizedEventPlan:
    """Deterministic joint optimizer. Rejects physically impossible overlap
    (same day, overlapping hours, different venue) and enforces capacity."""
    # 1. Conflict detection.
    conflicts: list[EventConflict] = []
    for i in range(len(allocations)):
        for j in range(i + 1, len(allocations)):
            if allocations[i].overlaps(allocations[j]):
                conflicts.append(
                    EventConflict(
                        allocation_id_a=allocations[i].allocation_id,
                        allocation_id_b=allocations[j].allocation_id,
                        day=allocations[i].day,
                    )
                )
    # 2. Capacity check using the canonical allocator.
    lane_demands = [
        CapacityAllocation(
            lane="EVENT_RELATIONSHIP",
            founder_minutes=a.founder_hours * 60,
            event_hours=a.founder_hours,
        )
        for a in allocations
    ]
    from auto_client_acquisition.portfolio_os.capacity import CapacityBudget

    budget = CapacityBudget(event_hours=event_hours_cap, founder_minutes=founder_minutes_cap)
    capacity_result = allocate_capacity(budget, lane_demands)
    violations = tuple(
        f"{v.resource}: requested {v.requested} > available {v.available}"
        for v in capacity_result.violations
    )

    founder_hours_total = sum(a.founder_hours for a in allocations)
    return OptimizedEventPlan(
        allocations=tuple(sorted(allocations, key=lambda a: (-a.score(), a.allocation_id))),
        conflicts=tuple(conflicts),
        capacity_feasible=capacity_result.feasible,
        capacity_violations=violations,
        founder_hours_total=founder_hours_total,
    )
