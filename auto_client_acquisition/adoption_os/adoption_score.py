"""Client adoption score — usage and cadence signals weighted 0–100."""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS: tuple[int, ...] = (15, 15, 10, 15, 10, 15, 10, 10)


@dataclass(frozen=True, slots=True)
class AdoptionDimensions:
    executive_sponsor: int
    workflow_owner: int
    data_readiness: int
    user_engagement: int
    approval_completion: int
    proof_visibility: int
    monthly_cadence: int
    expansion_pull: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def adoption_score(dimensions: AdoptionDimensions) -> int:
    d = dimensions
    values = (
        _clamp_pct(d.executive_sponsor),
        _clamp_pct(d.workflow_owner),
        _clamp_pct(d.data_readiness),
        _clamp_pct(d.user_engagement),
        _clamp_pct(d.approval_completion),
        _clamp_pct(d.proof_visibility),
        _clamp_pct(d.monthly_cadence),
        _clamp_pct(d.expansion_pull),
    )
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def adoption_band(score: int) -> str:
    if score >= 85:
        return "scale_account"
    if score >= 70:
        return "retainer_ready"
    if score >= 55:
        return "needs_enablement"
    return "risky_adoption"
