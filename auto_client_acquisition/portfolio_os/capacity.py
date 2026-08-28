"""V18 Capacity & Attention Allocator (Workstream F / §13).

Explicitly allocates scarce founder/agent/event resources across lanes.
Capacity overload must reduce acquisition, never degrade follow-up quality.
The allocator fails closed when demands exceed budget — it never overbooks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CapacityBudget:
    """Weekly default capacity. All values are hard caps."""

    founder_minutes: int = 600
    event_hours: int = 20
    research_hours: int = 10
    local_llm_minutes: int = 240
    cloud_llm_budget_usd: float = 10.0
    proposal_bandwidth: int = 5
    review_bandwidth: int = 10
    delivery_capacity: int = 2
    partner_followup_capacity: int = 5

    def to_dict(self) -> dict[str, Any]:
        return {
            "founder_minutes": self.founder_minutes,
            "event_hours": self.event_hours,
            "research_hours": self.research_hours,
            "local_llm_minutes": self.local_llm_minutes,
            "cloud_llm_budget_usd": self.cloud_llm_budget_usd,
            "proposal_bandwidth": self.proposal_bandwidth,
            "review_bandwidth": self.review_bandwidth,
            "delivery_capacity": self.delivery_capacity,
            "partner_followup_capacity": self.partner_followup_capacity,
        }


def default_capacity_budget() -> CapacityBudget:
    return CapacityBudget()


@dataclass(frozen=True, slots=True)
class CapacityAllocation:
    """One lane's requested consumption. All fields are demands."""

    lane: str
    founder_minutes: int = 0
    event_hours: int = 0
    research_hours: int = 0
    local_llm_minutes: int = 0
    cloud_llm_budget_usd: float = 0.0
    proposals: int = 0
    reviews: int = 0
    delivery_slots: int = 0
    partner_followups: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "lane": self.lane,
            "founder_minutes": self.founder_minutes,
            "event_hours": self.event_hours,
            "research_hours": self.research_hours,
            "local_llm_minutes": self.local_llm_minutes,
            "cloud_llm_budget_usd": self.cloud_llm_budget_usd,
            "proposals": self.proposals,
            "reviews": self.reviews,
            "delivery_slots": self.delivery_slots,
            "partner_followups": self.partner_followups,
        }


@dataclass(frozen=True, slots=True)
class AllocationViolation:
    resource: str
    requested: float
    available: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "resource": self.resource,
            "requested": self.requested,
            "available": self.available,
        }


@dataclass(frozen=True, slots=True)
class AllocationResult:
    accepted: tuple[CapacityAllocation, ...]
    violations: tuple[AllocationViolation, ...] = ()
    accepted_lanes: tuple[str, ...] = ()

    @property
    def feasible(self) -> bool:
        return not self.violations

    def to_dict(self) -> dict[str, Any]:
        return {
            "feasible": self.feasible,
            "accepted_lanes": list(self.accepted_lanes),
            "violations": [v.to_dict() for v in self.violations],
        }


def _sum_field(allocations: list[CapacityAllocation], attr: str) -> float:
    return float(sum(getattr(a, attr, 0) for a in allocations))


def allocate_capacity(
    budget: CapacityBudget, demands: list[CapacityAllocation]
) -> AllocationResult:
    """Deterministic allocator. Any overbooked resource produces a violation
    and the plan is infeasible. Lane ordering is preserved for accepted lanes
    only when feasible; when infeasible, all lanes are rejected (fail closed)
    so nobody's follow-up quality is degraded."""
    if not demands:
        return AllocationResult(accepted=(), accepted_lanes=())

    totals: dict[str, float] = {
        "founder_minutes": _sum_field(demands, "founder_minutes"),
        "event_hours": _sum_field(demands, "event_hours"),
        "research_hours": _sum_field(demands, "research_hours"),
        "local_llm_minutes": _sum_field(demands, "local_llm_minutes"),
        "cloud_llm_budget_usd": _sum_field(demands, "cloud_llm_budget_usd"),
        "proposals": _sum_field(demands, "proposals"),
        "reviews": _sum_field(demands, "reviews"),
        "delivery_slots": _sum_field(demands, "delivery_slots"),
        "partner_followups": _sum_field(demands, "partner_followups"),
    }
    caps: dict[str, float] = {
        "founder_minutes": float(budget.founder_minutes),
        "event_hours": float(budget.event_hours),
        "research_hours": float(budget.research_hours),
        "local_llm_minutes": float(budget.local_llm_minutes),
        "cloud_llm_budget_usd": float(budget.cloud_llm_budget_usd),
        "proposals": float(budget.proposal_bandwidth),
        "reviews": float(budget.review_bandwidth),
        "delivery_slots": float(budget.delivery_capacity),
        "partner_followups": float(budget.partner_followup_capacity),
    }
    violations = [
        AllocationViolation(resource=r, requested=totals[r], available=caps[r])
        for r in caps
        if totals[r] > caps[r] + 1e-9
    ]
    if violations:
        return AllocationResult(accepted=(), violations=tuple(violations))
    return AllocationResult(
        accepted=tuple(demands),
        accepted_lanes=tuple(d.lane for d in demands),
    )
