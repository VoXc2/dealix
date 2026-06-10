"""Client adoption score — usage and cadence signals weighted 0–100."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
)
from auto_client_acquisition.customer_success import health_score

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


def adoption_tier(score: float) -> str:
    """Map a 0-100 adoption score to a maturity tier.

    Doctrine thresholds: latent<20, exploring<40, active<70, embedded<90, power.
    """
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
class AdoptionScore:
    """Computed adoption score for a single customer."""

    customer_id: str
    score: float
    tier: str
    drivers: list[str] = field(default_factory=list)
    trend: float = 0.0
    governance_decision: str = GovernanceDecision.ALLOW_WITH_REVIEW.value

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
) -> AdoptionScore:
    """Compute a 0-100 adoption score from usage and engagement signals.

    Delegates the two sub-scores to ``customer_success.health_score`` so the
    adoption economics stay consistent with the customer health model.
    """
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

    # Adoption breadth weighted slightly above raw engagement.
    score = round(adoption_sub * 0.55 + engagement_sub * 0.45, 1)
    score = max(0.0, min(100.0, score))
    tier = adoption_tier(score)

    drivers: list[str] = []
    if adoption_sub < 50:
        drivers.append(f"weak_adoption_breadth:{adoption_sub:.0f}")
    if engagement_sub < 50:
        drivers.append(f"weak_engagement:{engagement_sub:.0f}")
    if adoption_sub >= 70:
        drivers.append(f"strong_adoption_breadth:{adoption_sub:.0f}")
    if engagement_sub >= 70:
        drivers.append(f"strong_engagement:{engagement_sub:.0f}")
    drivers = drivers[:3]

    trend = 0.0 if previous_score is None else round(score - previous_score, 1)

    return AdoptionScore(
        customer_id=customer_id,
        score=score,
        tier=tier,
        drivers=drivers,
        trend=trend,
        governance_decision=GovernanceDecision.ALLOW_WITH_REVIEW.value,
    )
