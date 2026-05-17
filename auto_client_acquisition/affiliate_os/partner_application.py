"""Partner / affiliate application scoring — Full Ops spec §9.

Pure logic. Scores an inbound partner application so the founder sees a
ranked recommendation. The application is always routed to an
ApprovalRequest regardless of score — this only produces a recommendation,
never an auto-accept (non-negotiable: no external action without approval).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

# Spec §9 weights.
_W_B2B_AUDIENCE = 4
_W_GCC_AUDIENCE = 3
_W_CONSULTANT = 3
_W_PREV_REFERRALS = 2
_W_CONTENT_QUALITY = 2
_W_TRUSTS_BRAND = 2
_W_SPAM = -5
_W_FAKE_AUDIENCE = -4
_W_NO_DISCLOSURE = -3
_W_VAGUE_PLAN = -3

ACCEPT_THRESHOLD = 10
REVIEW_THRESHOLD = 4


@dataclass
class PartnerApplication:
    """A PII-free partner application. ``handle`` is a non-PII identifier;
    email is hashed by the caller before it ever reaches this layer."""

    handle: str = "applicant"
    audience_type: str = "unknown"          # b2b | b2c | mixed | unknown
    audience_in_gcc: bool = False
    is_consultant_or_operator: bool = False
    previous_b2b_referrals: int = 0
    content_quality_good: bool = False
    trusts_brand: bool = False              # accepts approved-messaging + disclosure
    spam_behavior: bool = False
    fake_audience_suspected: bool = False
    accepts_disclosure: bool = True
    promotion_plan_clear: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ApplicationScore:
    score: int
    recommendation: str        # recommend_accept | needs_review | recommend_reject
    breakdown: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def score_application(app: PartnerApplication) -> ApplicationScore:
    """Score a partner application per spec §9 and classify it."""
    score = 0
    breakdown: list[str] = []

    def add(points: int, label: str) -> None:
        nonlocal score
        score += points
        breakdown.append(f"{'+' if points >= 0 else ''}{points} {label}")

    if app.audience_type == "b2b":
        add(_W_B2B_AUDIENCE, "B2B audience")
    if app.audience_in_gcc:
        add(_W_GCC_AUDIENCE, "GCC audience")
    if app.is_consultant_or_operator:
        add(_W_CONSULTANT, "consultant/operator")
    if app.previous_b2b_referrals > 0:
        add(_W_PREV_REFERRALS, "previous B2B referrals")
    if app.content_quality_good:
        add(_W_CONTENT_QUALITY, "content quality")
    if app.trusts_brand:
        add(_W_TRUSTS_BRAND, "trusts brand / approved messaging")
    if app.spam_behavior:
        add(_W_SPAM, "spam behavior")
    if app.fake_audience_suspected:
        add(_W_FAKE_AUDIENCE, "fake audience suspected")
    if not app.accepts_disclosure:
        add(_W_NO_DISCLOSURE, "does not accept disclosure")
    if not app.promotion_plan_clear:
        add(_W_VAGUE_PLAN, "vague promotion plan")

    if score >= ACCEPT_THRESHOLD:
        recommendation = "recommend_accept"
    elif score >= REVIEW_THRESHOLD:
        recommendation = "needs_review"
    else:
        recommendation = "recommend_reject"

    return ApplicationScore(
        score=score,
        recommendation=recommendation,
        breakdown=breakdown,
    )


__all__ = [
    "ACCEPT_THRESHOLD",
    "REVIEW_THRESHOLD",
    "ApplicationScore",
    "PartnerApplication",
    "score_application",
]
