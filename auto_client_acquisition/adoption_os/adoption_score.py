"""Client adoption score — usage and cadence signals weighted 0–100."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

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


def _adoption_tier(score: float) -> str:
    """Doctrine tiers — latent<20, exploring<40, active<70, embedded<90, power."""
    if score < 20:
        return "latent"
    if score < 40:
        return "exploring"
    if score < 70:
        return "active"
    if score < 90:
        return "embedded"
    return "power"


@dataclass(frozen=True, slots=True)
class AdoptionScoreResult:
    """Composite adoption score result with governance envelope."""

    customer_id: str
    score: float
    tier: str
    adoption_subscore: float
    engagement_subscore: float
    drivers: list[str] = field(default_factory=list)
    trend: float = 0.0
    governance_decision: str = "allow"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compute(
    *,
    customer_id: str,
    channels_enabled: int = 0,
    integrations_connected: int = 0,
    sectors_targeted: int = 0,
    total_drafts_lifetime: int = 0,
    logins_last_30d: int = 0,
    drafts_approved_last_30d: int = 0,
    replies_acted_on_last_30d: int = 0,
    previous_score: float | None = None,
) -> AdoptionScoreResult:
    """Composite adoption score (0-100) delegating to customer_success.health_score.

    Blends product adoption breadth and 30-day engagement cadence. Returns a
    tiered, bounded result carrying a governance decision envelope.
    """
    from auto_client_acquisition.customer_success import health_score

    adoption_sub = health_score.compute_adoption(
        channels_enabled=channels_enabled,
        integrations_connected=integrations_connected,
        sectors_targeted=sectors_targeted,
        total_drafts_lifetime=total_drafts_lifetime,
    )
    engagement_sub = health_score.compute_engagement(
        logins_last_30d=logins_last_30d,
        drafts_approved_last_30d=drafts_approved_last_30d,
        replies_acted_on_last_30d=replies_acted_on_last_30d,
    )

    score = round(adoption_sub * 0.6 + engagement_sub * 0.4, 1)
    score = max(0.0, min(100.0, score))
    tier = _adoption_tier(score)

    candidates: list[tuple[str, float]] = [
        ("adoption_breadth", adoption_sub),
        ("engagement_cadence", engagement_sub),
    ]
    drivers = [f"{name}:{value:.0f}" for name, value in sorted(candidates, key=lambda x: -x[1])]
    drivers = drivers[:3]

    trend = 0.0 if previous_score is None else round(score - previous_score, 1)

    return AdoptionScoreResult(
        customer_id=customer_id,
        score=score,
        tier=tier,
        adoption_subscore=round(adoption_sub, 1),
        engagement_subscore=round(engagement_sub, 1),
        drivers=drivers,
        trend=trend,
        governance_decision="allow",
    )
