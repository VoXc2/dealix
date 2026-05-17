"""Revenue Autopilot lead scorer — deterministic point system.

Separate from ``crm_v10/lead_scoring.py`` (fit + urgency floats). This
scorer implements the founder doctrine point system: same signals in →
identical score and tier out. No randomness, no LLM.

Doctrine: docs/REVENUE_AUTOPILOT.md §4.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

LeadTier = Literal["qualified_A", "qualified_B", "nurture", "closed_lost"]


# (signal field, points, human label) — the founder point system, verbatim.
_SCORE_RULES: tuple[tuple[str, int, str], ...] = (
    ("is_decision_maker", 3, "decision maker"),
    ("is_b2b_company", 3, "B2B company"),
    ("has_revenue_workflow", 3, "has CRM/revenue workflow"),
    ("uses_or_plans_ai", 3, "uses or plans AI"),
    ("is_saudi_or_gcc", 2, "Saudi/GCC"),
    ("urgency_within_30_days", 2, "urgency within 30 days"),
    ("budget_5k_plus", 2, "budget 5k+ SAR"),
    ("no_company", -3, "no company"),
    ("is_student_or_job_seeker", -3, "student/job seeker"),
    ("vague_curiosity_only", -2, "vague curiosity"),
)


class LeadSignals(BaseModel):
    """The 10 boolean signals that drive the autopilot lead score."""

    model_config = ConfigDict(extra="forbid")

    is_decision_maker: bool = False
    is_b2b_company: bool = False
    has_revenue_workflow: bool = False
    uses_or_plans_ai: bool = False
    is_saudi_or_gcc: bool = False
    urgency_within_30_days: bool = False
    budget_5k_plus: bool = False
    no_company: bool = False
    is_student_or_job_seeker: bool = False
    vague_curiosity_only: bool = False


class LeadScore(BaseModel):
    """Result of scoring — total points, tier, and a per-rule breakdown."""

    model_config = ConfigDict(extra="forbid")

    points: int
    tier: LeadTier
    breakdown: list[str]


def tier_for_points(points: int) -> LeadTier:
    """Map a point total to a funnel tier (founder thresholds)."""
    if points >= 12:
        return "qualified_A"
    if points >= 8:
        return "qualified_B"
    if points >= 5:
        return "nurture"
    return "closed_lost"


def score_lead(signals: LeadSignals) -> LeadScore:
    """Score a lead deterministically from its signals."""
    points = 0
    breakdown: list[str] = []
    for field, pts, label in _SCORE_RULES:
        if getattr(signals, field):
            points += pts
            breakdown.append(f"{label}:{pts:+d}")
    return LeadScore(points=points, tier=tier_for_points(points), breakdown=breakdown)


__all__ = ["LeadScore", "LeadSignals", "LeadTier", "score_lead", "tier_for_points"]
