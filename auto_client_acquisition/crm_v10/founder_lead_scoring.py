"""Founder lead scoring — the additive intake formula (no LLM).

Scores a freshly-captured lead from explicit boolean signals and maps the
total to a :class:`LeadClassification`. Deterministic: same inputs in,
same score out. Complements ``crm_v10.lead_scoring.score_lead`` (which
derives a fit/urgency pair 0..1 from Account+Lead) — this one is the
coarse founder triage used at the top of the funnel.

Bands (from the founder revenue-machine doctrine):
  >= 12        → qualified_A
  8 .. 11      → qualified_B
  5 .. 7       → nurture
  < 5          → drop

A lead flagged as a partner is classified ``partner_candidate``
regardless of score — partners take a different path than buyers.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from auto_client_acquisition.crm_v10.pipeline_view import LeadClassification

# Positive signals — a stronger fit raises the score.
_POSITIVE_WEIGHTS: dict[str, int] = {
    "decision_maker": 3,
    "is_b2b": 3,
    "has_crm_or_revenue_process": 3,
    "uses_or_plans_ai": 3,
    "in_gcc": 2,
    "urgent_within_30_days": 2,
    "budget_5k_plus_sar": 2,
}

# Negative signals — a poor fit lowers the score.
_NEGATIVE_WEIGHTS: dict[str, int] = {
    "no_company": -3,
    "student_or_jobseeker": -3,
    "vague_curiosity": -2,
}

_QUALIFIED_A_THRESHOLD = 12
_QUALIFIED_B_THRESHOLD = 8
_NURTURE_THRESHOLD = 5


@dataclass(frozen=True, slots=True)
class FounderLeadScore:
    """Outcome of the founder intake scorer."""

    score: int
    classification: str
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _classify(score: int) -> LeadClassification:
    if score >= _QUALIFIED_A_THRESHOLD:
        return LeadClassification.QUALIFIED_A
    if score >= _QUALIFIED_B_THRESHOLD:
        return LeadClassification.QUALIFIED_B
    if score >= _NURTURE_THRESHOLD:
        return LeadClassification.NURTURE
    return LeadClassification.DROP


def score_founder_lead(
    *,
    decision_maker: bool = False,
    is_b2b: bool = False,
    has_crm_or_revenue_process: bool = False,
    uses_or_plans_ai: bool = False,
    in_gcc: bool = False,
    urgent_within_30_days: bool = False,
    budget_5k_plus_sar: bool = False,
    no_company: bool = False,
    student_or_jobseeker: bool = False,
    vague_curiosity: bool = False,
    is_partner: bool = False,
) -> FounderLeadScore:
    """Score a captured lead and classify it for the founder pipeline."""
    signals = {
        "decision_maker": decision_maker,
        "is_b2b": is_b2b,
        "has_crm_or_revenue_process": has_crm_or_revenue_process,
        "uses_or_plans_ai": uses_or_plans_ai,
        "in_gcc": in_gcc,
        "urgent_within_30_days": urgent_within_30_days,
        "budget_5k_plus_sar": budget_5k_plus_sar,
        "no_company": no_company,
        "student_or_jobseeker": student_or_jobseeker,
        "vague_curiosity": vague_curiosity,
    }
    score = 0
    reasons: list[str] = []
    for key, present in signals.items():
        if not present:
            continue
        weight = _POSITIVE_WEIGHTS.get(key) or _NEGATIVE_WEIGHTS[key]
        score += weight
        reasons.append(f"{key}:{weight:+d}")

    if is_partner:
        classification = LeadClassification.PARTNER_CANDIDATE
        reasons.append("flagged_partner:classification_overridden")
    else:
        classification = _classify(score)

    return FounderLeadScore(
        score=score,
        classification=classification.value,
        reasons=reasons,
    )


__all__ = [
    "FounderLeadScore",
    "score_founder_lead",
]
