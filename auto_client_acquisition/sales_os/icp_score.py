"""ICP score — lightweight 0–100 fit for Saudi B2B services (deterministic)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ICPDimensions:
    b2b_service_fit: int  # 0–100
    data_maturity: int
    governance_posture: int
    budget_signal: int
    decision_velocity: int


def icp_score(dimensions: ICPDimensions) -> int:
    d = dimensions
    vals = (d.b2b_service_fit, d.data_maturity, d.governance_posture, d.budget_signal, d.decision_velocity)
    clipped = tuple(max(0, min(100, v)) for v in vals)
    return min(100, sum(clipped) // len(clipped))


__all__ = ["ICPDimensions", "icp_score"]
