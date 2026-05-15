"""Client adoption score — usage and cadence signals weighted 0–100."""

from __future__ import annotations

from dataclasses import dataclass, field

from auto_client_acquisition.customer_success import health_score as _hs

_WEIGHTS: tuple[int, ...] = (15, 15, 10, 15, 10, 15, 10, 10)

_TIER_LATENT = "latent"
_TIER_EXPLORING = "exploring"
_TIER_ACTIVE = "active"
_TIER_EMBEDDED = "embedded"
_TIER_POWER = "power"


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


def adoption_tier(score: float) -> str:
    """Doctrine tier mapping: latent<20, exploring<40, active<70, embedded<90, power."""
    if score < 20:
        return _TIER_LATENT
    if score < 40:
        return _TIER_EXPLORING
    if score < 70:
        return _TIER_ACTIVE
    if score < 90:
        return _TIER_EMBEDDED
    return _TIER_POWER


@dataclass(frozen=True, slots=True)
class AdoptionScore:
    """Result of compute() — composite adoption score with governance envelope."""

    customer_id: str
    score: float
    tier: str
    band: str
    trend: float
    drivers: list[str] = field(default_factory=list)
    governance_decision: str = "allow_with_review"


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
) -> AdoptionScore:
    """Composite adoption score 0–100 from breadth (adoption) + cadence (engagement).

    Delegates the sub-scores to customer_success.health_score so the adoption
    and engagement axes stay consistent with the customer health model.
    """
    if not customer_id:
        raise ValueError("customer_id is required")

    adoption_sub = _hs.compute_adoption(
        channels_enabled=channels_enabled,
        integrations_connected=integrations_connected,
        sectors_targeted=sectors_targeted,
        total_drafts_lifetime=total_drafts_lifetime,
    )
    engagement_sub = _hs.compute_engagement(
        logins_last_30d=logins_last_30d,
        drafts_approved_last_30d=drafts_approved_last_30d,
        replies_acted_on_last_30d=replies_acted_on_last_30d,
    )

    # Adoption breadth 55%, engagement cadence 45%.
    raw = adoption_sub * 0.55 + engagement_sub * 0.45
    score = round(max(0.0, min(100.0, raw)), 1)
    tier = adoption_tier(score)
    band = adoption_band(int(score))

    trend = 0.0
    if previous_score is not None:
        trend = round(score - float(previous_score), 1)

    drivers: list[str] = []
    if adoption_sub >= 60.0:
        drivers.append(f"adoption_breadth:{adoption_sub:.0f}")
    elif adoption_sub < 40.0:
        drivers.append(f"weak_adoption_breadth:{adoption_sub:.0f}")
    if engagement_sub >= 60.0:
        drivers.append(f"engagement_cadence:{engagement_sub:.0f}")
    elif engagement_sub < 40.0:
        drivers.append(f"weak_engagement_cadence:{engagement_sub:.0f}")
    if trend > 0.0:
        drivers.append(f"trend_up:{trend:.0f}")
    elif trend < 0.0:
        drivers.append(f"trend_down:{trend:.0f}")

    return AdoptionScore(
        customer_id=customer_id,
        score=score,
        tier=tier,
        band=band,
        trend=trend,
        drivers=drivers[:3],
        governance_decision="allow_with_review",
    )


__all__ = [
    "AdoptionDimensions",
    "AdoptionScore",
    "adoption_band",
    "adoption_score",
    "adoption_tier",
    "compute",
]
