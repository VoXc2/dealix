"""Client Quality Score — weighted 0–100 for intake and expansion fit."""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS: tuple[int, ...] = (15, 15, 15, 15, 15, 15, 10)


@dataclass(frozen=True, slots=True)
class ClientQualityDimensions:
    clear_pain: int
    data_readiness: int
    decision_owner: int
    willingness_to_pay: int
    governance_alignment: int
    retainer_potential: int
    strategic_logo_or_sector: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def client_quality_score(dimensions: ClientQualityDimensions) -> int:
    d = dimensions
    values = (
        _clamp_pct(d.clear_pain),
        _clamp_pct(d.data_readiness),
        _clamp_pct(d.decision_owner),
        _clamp_pct(d.willingness_to_pay),
        _clamp_pct(d.governance_alignment),
        _clamp_pct(d.retainer_potential),
        _clamp_pct(d.strategic_logo_or_sector),
    )
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def client_quality_band(score: int) -> str:
    if score >= 85:
        return "ideal_client"
    if score >= 70:
        return "good_client"
    if score >= 55:
        return "diagnostic_only"
    return "avoid"
