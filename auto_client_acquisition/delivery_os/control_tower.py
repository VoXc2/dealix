"""Delivery control tower risk and stage gate helpers."""

from __future__ import annotations

from dataclasses import dataclass

REQUIRED_STAGE_GATES: tuple[str, ...] = (
    "intake_ready",
    "scope_ready",
    "data_ready",
    "governance_ready",
    "qa_ready",
    "proof_ready",
    "handoff_ready",
)


@dataclass(frozen=True, slots=True)
class DeliveryRisk:
    engagement_id: str
    blocker_count: int
    quality_exceptions: int
    governance_exceptions: int
    schedule_delay_days: int


def stage_gate_passes(gates: dict[str, bool]) -> tuple[bool, tuple[str, ...]]:
    missing = [gate for gate in REQUIRED_STAGE_GATES if not gates.get(gate, False)]
    return not missing, tuple(missing)


def compute_delivery_risk_score(risk: DeliveryRisk) -> int:
    score = (
        (risk.blocker_count * 15)
        + (risk.quality_exceptions * 20)
        + (risk.governance_exceptions * 25)
        + (max(0, risk.schedule_delay_days) * 5)
    )
    return min(100, max(0, score))


def delivery_risk_band(score: int) -> str:
    if score >= 70:
        return "critical"
    if score >= 45:
        return "high"
    if score >= 20:
        return "medium"
    return "low"


__all__ = [
    "REQUIRED_STAGE_GATES",
    "DeliveryRisk",
    "compute_delivery_risk_score",
    "delivery_risk_band",
    "stage_gate_passes",
]
