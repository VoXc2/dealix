"""Adoption Score — wraps customer_success.health_score.compute_adoption
(breadth 0.6) + compute_engagement (activity 0.4).

The math is NEVER duplicated; this module delegates to those existing
functions so the dimensions stay aligned with the Health Score model.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.client_os.badges import StatusBadge
from auto_client_acquisition.customer_success import health_score as _health_score
from auto_client_acquisition.governance_os.runtime_decision import GovernanceDecision


_TIER_THRESHOLDS = (
    ("latent", 0, 20),
    ("exploring", 20, 40),
    ("active", 40, 70),
    ("embedded", 70, 90),
    ("power", 90, 101),
)


def _tier_for(score: float) -> str:
    for name, lo, hi in _TIER_THRESHOLDS:
        if lo <= score < hi:
            return name
    return "power"


@dataclass
class AdoptionScore:
    customer_id: str
    score: float
    breadth: float
    activity: float
    tier: str
    drivers: list[str] = field(default_factory=list)
    trend: float = 0.0
    recommended_action: str = ""
    governance_decision: str = GovernanceDecision.ALLOW.value
    status_badge: str = StatusBadge.DRAFT.value
    computed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

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
    """Composite adoption score.

    breadth (0–100) := compute_adoption(channels, integrations, sectors, total_drafts)
    activity (0–100) := compute_engagement(logins, drafts_approved, replies_acted)
    score := 0.6 * breadth + 0.4 * activity
    """
    # Resolve attributes at call-time so test patches on
    # auto_client_acquisition.customer_success.health_score.compute_adoption
    # are observed (no import-time aliasing).
    breadth = _health_score.compute_adoption(
        channels_enabled=channels_enabled,
        integrations_connected=integrations_connected,
        sectors_targeted=sectors_targeted,
        total_drafts_lifetime=total_drafts_lifetime,
    )
    activity = _health_score.compute_engagement(
        logins_last_30d=logins_last_30d,
        drafts_approved_last_30d=drafts_approved_last_30d,
        replies_acted_on_last_30d=replies_acted_on_last_30d,
    )
    score = round(0.6 * breadth + 0.4 * activity, 1)
    tier = _tier_for(score)

    # Drivers — at most three.
    drivers: list[str] = []
    if channels_enabled == 0:
        drivers.append("no_channels_enabled")
    if integrations_connected == 0:
        drivers.append("no_integrations_connected")
    if logins_last_30d < 4:
        drivers.append(f"low_logins:{logins_last_30d}")
    if drafts_approved_last_30d < 5:
        drivers.append(f"low_drafts_approved:{drafts_approved_last_30d}")
    if total_drafts_lifetime >= 100 and not drivers:
        drivers.append("mature_lifetime_usage")
    if tier == "power" and not drivers:
        drivers.append("all_dimensions_healthy")
    drivers = drivers[:3]

    trend = 0.0 if previous_score is None else round(score - float(previous_score), 1)

    if tier == "latent":
        action = "onboarding_session_within_7d"
    elif tier == "exploring":
        action = "enable_one_more_channel_or_integration"
    elif tier == "active":
        action = "monthly_review_cadence"
    elif tier == "embedded":
        action = "raise_retainer_conversation"
    else:
        action = "expansion_or_referral_ask"

    badge = (
        StatusBadge.CLIENT_READY.value
        if tier in ("embedded", "power")
        else StatusBadge.DRAFT.value
    )

    return AdoptionScore(
        customer_id=customer_id,
        score=score,
        breadth=round(breadth, 1),
        activity=round(activity, 1),
        tier=tier,
        drivers=drivers,
        trend=trend,
        recommended_action=action,
        governance_decision=GovernanceDecision.ALLOW.value,
        status_badge=badge,
    )


__all__ = ["AdoptionScore", "compute"]
