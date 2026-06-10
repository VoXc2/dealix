"""Client health score — expansion vs pause discipline."""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS: tuple[int, ...] = (15, 15, 15, 20, 15, 10, 10)


@dataclass(frozen=True, slots=True)
class ClientHealthDimensions:
    clear_owner: int
    data_readiness: int
    stakeholder_engagement: int
    proof_strength: int
    governance_alignment: int
    monthly_workflow_need: int
    expansion_potential: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def client_health_score(dimensions: ClientHealthDimensions) -> int:
    d = dimensions
    values = (
        _clamp_pct(d.clear_owner),
        _clamp_pct(d.data_readiness),
        _clamp_pct(d.stakeholder_engagement),
        _clamp_pct(d.proof_strength),
        _clamp_pct(d.governance_alignment),
        _clamp_pct(d.monthly_workflow_need),
        _clamp_pct(d.expansion_potential),
    )
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def client_health_band(score: int) -> str:
    if score >= 85:
        return "expand_aggressively"
    if score >= 70:
        return "offer_retainer"
    if score >= 55:
        return "continue_carefully"
    return "pause_or_diagnostic_only"
