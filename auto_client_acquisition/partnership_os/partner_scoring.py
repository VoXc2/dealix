"""Partner application scoring — playbook section 6 rubric.

Pure function. Takes a partner application dict, returns a
``PartnerScore`` with the numeric score, the per-signal breakdown
and a recommendation (``auto_review`` / ``approve_candidate`` /
``reject``).

The rubric only scores declared/auditable signals — it never scrapes
or enriches. A negative recommendation never auto-rejects a partner;
it routes the application to human review (doctrine: no external
action without approval).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Positive signals — declared on the application.
_POS_B2B_AUDIENCE = 4
_POS_GCC = 3
_POS_CONSULTANT_OPERATOR = 3
_POS_PRIOR_REFERRALS = 2
_POS_CONTENT_QUALITY = 2
_POS_TRUSTED_BRAND = 2

# Negative signals — observed/flagged behaviour.
_NEG_SPAM_BEHAVIOR = -5
_NEG_FAKE_AUDIENCE = -4
_NEG_NO_DISCLOSURE = -3
_NEG_VAGUE_PLAN = -3

_B2B_AUDIENCE_TYPES = {"b2b", "smb_b2b", "enterprise", "operators", "consultants"}
_GCC_COUNTRIES = {
    "sa", "ksa", "saudi arabia", "saudi", "ae", "uae",
    "qa", "qatar", "kw", "kuwait", "bh", "bahrain", "om", "oman",
}
_CONSULTANT_CHANNELS = {"consulting", "consultant", "advisory", "operator", "agency"}

# Recommendation thresholds.
_APPROVE_CANDIDATE_AT = 8
_REJECT_BELOW = 0


@dataclass(slots=True)
class PartnerScore:
    """Result of scoring one partner application."""

    score: int
    recommendation: str
    breakdown: dict[str, int] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "recommendation": self.recommendation,
            "breakdown": dict(self.breakdown),
            "reasons": list(self.reasons),
        }


def _truthy(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def score_partner(application: dict[str, Any]) -> PartnerScore:
    """Score a partner application against the playbook section 6 rubric.

    ``application`` keys consulted (all optional, declared-only):
      - ``audience_type`` (str) — ``b2b`` family scores +4
      - ``country`` (str) — a GCC country scores +3
      - ``main_channel`` (str) — consultant/operator/agency scores +3
      - ``prior_referrals`` (int|bool) — > 0 scores +2
      - ``content_quality`` (bool) — +2 when the founder rates it good
      - ``trusted_brand`` (bool) — +2 for a recognised brand
      - ``spam_behavior`` (bool) — -5
      - ``fake_audience`` (bool) — -4
      - ``disclosure_accepted`` (bool) — -3 when False
      - ``plan`` (str) — a vague/empty go-to-market plan scores -3
    """
    breakdown: dict[str, int] = {}
    reasons: list[str] = []

    audience = str(application.get("audience_type") or "").strip().lower()
    if audience in _B2B_AUDIENCE_TYPES:
        breakdown["b2b_audience"] = _POS_B2B_AUDIENCE
        reasons.append("declared B2B audience")

    country = str(application.get("country") or "").strip().lower()
    if country in _GCC_COUNTRIES:
        breakdown["gcc"] = _POS_GCC
        reasons.append("based in the GCC")

    channel = str(application.get("main_channel") or "").strip().lower()
    if channel in _CONSULTANT_CHANNELS:
        breakdown["consultant_operator"] = _POS_CONSULTANT_OPERATOR
        reasons.append("consultant / operator channel")

    prior = application.get("prior_referrals", 0)
    try:
        prior_n = int(prior)
    except (TypeError, ValueError):
        prior_n = 1 if _truthy(prior) else 0
    if prior_n > 0:
        breakdown["prior_referrals"] = _POS_PRIOR_REFERRALS
        reasons.append("has prior referral track record")

    if _truthy(application.get("content_quality")):
        breakdown["content_quality"] = _POS_CONTENT_QUALITY
        reasons.append("quality content presence")

    if _truthy(application.get("trusted_brand")):
        breakdown["trusted_brand"] = _POS_TRUSTED_BRAND
        reasons.append("recognised / trusted brand")

    if _truthy(application.get("spam_behavior")):
        breakdown["spam_behavior"] = _NEG_SPAM_BEHAVIOR
        reasons.append("flagged for spam behaviour")

    if _truthy(application.get("fake_audience")):
        breakdown["fake_audience"] = _NEG_FAKE_AUDIENCE
        reasons.append("flagged for fake / inflated audience")

    if not _truthy(application.get("disclosure_accepted")):
        breakdown["no_disclosure"] = _NEG_NO_DISCLOSURE
        reasons.append("disclosure not accepted")

    plan = str(application.get("plan") or "").strip()
    if len(plan) < 20:
        breakdown["vague_plan"] = _NEG_VAGUE_PLAN
        reasons.append("vague or missing go-to-market plan")

    score = sum(breakdown.values())

    if score <= _REJECT_BELOW:
        recommendation = "reject"
    elif score >= _APPROVE_CANDIDATE_AT:
        recommendation = "approve_candidate"
    else:
        recommendation = "auto_review"

    return PartnerScore(
        score=score,
        recommendation=recommendation,
        breakdown=breakdown,
        reasons=reasons,
    )


__all__ = ["PartnerScore", "score_partner"]
