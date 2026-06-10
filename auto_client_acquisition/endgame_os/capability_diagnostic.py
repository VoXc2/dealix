"""Capability diagnostic outputs — 0–5 maturity per capability."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CapabilityDiagnosticProfile:
    """Current capability levels 0–5 for core dimensions."""

    revenue: int
    data: int
    governance: int

    def __post_init__(self) -> None:
        for name, v in (("revenue", self.revenue), ("data", self.data), ("governance", self.governance)):
            if not 0 <= v <= 5:
                msg = f"{name} must be 0..5"
                raise ValueError(msg)


def recommended_sprints(p: CapabilityDiagnosticProfile) -> tuple[str, ...]:
    out: list[str] = []
    if p.revenue <= 2:
        out.append("Revenue Intelligence Sprint")
    if p.governance <= 1:
        out.append("AI Governance Review")
    if p.data <= 2 and p.revenue >= 2:
        out.append("Data Readiness work (pre-AI workflow)")
    if not out:
        out.append("Company Brain Sprint or AI Quick Win Sprint")
    return tuple(dict.fromkeys(out))  # de-dup preserve order
