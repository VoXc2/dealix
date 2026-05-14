"""Dealix Capability Index (DCI) — seven capabilities, levels 0–5."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class CapabilityDimension(StrEnum):
    REVENUE = "revenue"
    CUSTOMER = "customer"
    OPERATIONS = "operations"
    KNOWLEDGE = "knowledge"
    DATA = "data"
    GOVERNANCE = "governance"
    REPORTING = "reporting"


CAPABILITY_LEVELS = range(0, 6)


@dataclass(frozen=True, slots=True)
class CapabilityIndexProfile:
    revenue: int
    customer: int
    operations: int
    knowledge: int
    data: int
    governance: int
    reporting: int

    def __post_init__(self) -> None:
        for name, v in (
            ("revenue", self.revenue),
            ("customer", self.customer),
            ("operations", self.operations),
            ("knowledge", self.knowledge),
            ("data", self.data),
            ("governance", self.governance),
            ("reporting", self.reporting),
        ):
            if not 0 <= v <= 5:
                msg = f"{name} must be 0..5"
                raise ValueError(msg)

    def transformation_gap(self, target: CapabilityIndexProfile) -> int:
        fields = (
            "revenue",
            "customer",
            "operations",
            "knowledge",
            "data",
            "governance",
            "reporting",
        )
        return sum(max(0, getattr(target, f) - getattr(self, f)) for f in fields)


def average_capability_level(p: CapabilityIndexProfile) -> int:
    vals = (
        p.revenue,
        p.customer,
        p.operations,
        p.knowledge,
        p.data,
        p.governance,
        p.reporting,
    )
    return sum(vals) // len(vals)
