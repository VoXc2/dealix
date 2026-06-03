"""Multi-factor AI lead scoring engine for the Saudi B2B market.

Extends the heuristic ``LeadScorer`` with BANT analysis, behavioural signals,
Saudi-sector weights, and PDPL consent tracking.  Pure-function core; no I/O.

Score tiers:
  HOT   80-100
  WARM  60-79
  COOL  40-59
  COLD  0-39
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.intelligence.lead_scorer import LeadFeatures, LeadScorer, ScoreResult

# ---------------------------------------------------------------------------
# Saudi sector weights (0.5–1.5 multiplier applied to sector_fit sub-score)
# ---------------------------------------------------------------------------
_SECTOR_WEIGHTS: dict[str, float] = {
    "real_estate": 1.4,
    "healthcare": 1.3,
    "fintech": 1.5,
    "b2b_saas": 1.3,
    "agency": 1.0,
    "logistics": 1.2,
    "engineering": 1.1,
}
_DEFAULT_SECTOR_WEIGHT = 0.9

_HOT_THRESHOLD = 80
_WARM_THRESHOLD = 60
_COOL_THRESHOLD = 40


@dataclass
class BANTSignals:
    """Budget-Authority-Need-Timeline signals for a single lead."""

    budget_sar: float = 0.0
    has_decision_maker: bool = False
    pain_score: float = 0.0      # 0-1 from intake
    timeline_days: int = 0        # 0 == unknown


@dataclass
class BehaviouralSignals:
    """Digital and offline engagement signals."""

    pages_visited: int = 0
    email_opens: int = 0
    whatsapp_replies: int = 0
    referral_source: bool = False
    attended_event: bool = False
    content_downloads: int = 0


@dataclass
class PDPLConsent:
    """Minimal PDPL consent record required before AI scoring."""

    consent_obtained: bool = False
    consent_ref: str = ""
    lawful_basis: str = ""      # e.g. "legitimate_interest", "consent"


@dataclass
class AILeadInput:
    """All signals fed into the AI lead scorer."""

    customer_id: str
    sector: str = ""
    base_features: LeadFeatures = field(default_factory=LeadFeatures)
    bant: BANTSignals = field(default_factory=BANTSignals)
    behavioural: BehaviouralSignals = field(default_factory=BehaviouralSignals)
    pdpl_consent: PDPLConsent = field(default_factory=PDPLConsent)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class AILeadScoreResult:
    """Bilingual scoring output with tier, numeric score, and reasoning."""

    score: int                              # 0-100
    tier: str                               # HOT | WARM | COOL | COLD
    tier_ar: str
    raw_heuristic: float                    # 0-1 from LeadScorer
    bant_score: int                         # 0-100
    behavioural_score: int                  # 0-100
    pdpl_cleared: bool
    reasons_en: list[str] = field(default_factory=list)
    reasons_ar: list[str] = field(default_factory=list)
    recommended_action_en: str = ""
    recommended_action_ar: str = ""
    governance_decision: str = "ALLOW_WITH_REVIEW"


# ---------------------------------------------------------------------------
# Internal scoring helpers
# ---------------------------------------------------------------------------

def _bant_score(bant: BANTSignals) -> int:
    """Convert BANT signals to a 0-100 sub-score."""
    points = 0

    if bant.budget_sar >= 50_000:
        points += 35
    elif bant.budget_sar >= 15_000:
        points += 22
    elif bant.budget_sar >= 5_000:
        points += 10

    if bant.has_decision_maker:
        points += 25

    pain = max(0.0, min(1.0, bant.pain_score))
    points += int(pain * 25)

    if 0 < bant.timeline_days <= 30:
        points += 15
    elif 31 <= bant.timeline_days <= 90:
        points += 8
    elif 91 <= bant.timeline_days <= 180:
        points += 3

    return min(100, points)


def _behavioural_score(b: BehaviouralSignals) -> int:
    """Convert behavioural signals to a 0-100 sub-score."""
    points = 0
    points += min(20, b.pages_visited * 3)
    points += min(15, b.email_opens * 5)
    points += min(20, b.whatsapp_replies * 7)
    if b.referral_source:
        points += 20
    if b.attended_event:
        points += 15
    points += min(10, b.content_downloads * 4)
    return min(100, points)


def _sector_multiplier(sector: str) -> float:
    return _SECTOR_WEIGHTS.get(sector.lower().strip(), _DEFAULT_SECTOR_WEIGHT)


def _tier_label(score: int) -> tuple[str, str]:
    if score >= _HOT_THRESHOLD:
        return "HOT", "ساخن"
    if score >= _WARM_THRESHOLD:
        return "WARM", "دافئ"
    if score >= _COOL_THRESHOLD:
        return "COOL", "فاتر"
    return "COLD", "بارد"


def _recommended_action(tier: str) -> tuple[str, str]:
    mapping = {
        "HOT": (
            "Schedule a diagnostic call within 24 hours.",
            "جدولة مكالمة تشخيصية خلال 24 ساعة.",
        ),
        "WARM": (
            "Send a personalised value proposal within 48 hours.",
            "إرسال مقترح قيمة مخصص خلال 48 ساعة.",
        ),
        "COOL": (
            "Add to nurture sequence; re-evaluate in 14 days.",
            "إضافة إلى تسلسل رعاية؛ إعادة التقييم بعد 14 يوماً.",
        ),
        "COLD": (
            "Enrich data and re-qualify; no outreach until score improves.",
            "إثراء البيانات وإعادة التأهيل؛ لا تواصل حتى تتحسن النقاط.",
        ),
    }
    return mapping.get(tier, ("", ""))


def _bant_reasons(bant: BANTSignals) -> tuple[list[str], list[str]]:
    en: list[str] = []
    ar: list[str] = []
    if bant.budget_sar >= 15_000:
        en.append("Strong budget signal")
        ar.append("إشارة ميزانية قوية")
    elif bant.budget_sar < 5_000:
        en.append("Weak budget signal")
        ar.append("إشارة ميزانية ضعيفة")
    if bant.has_decision_maker:
        en.append("Decision maker confirmed")
        ar.append("صانع القرار مؤكَّد")
    if bant.pain_score >= 0.7:
        en.append("High pain / urgency")
        ar.append("ألم / إلحاح عالٍ")
    if 0 < bant.timeline_days <= 90:
        en.append("Near-term buying timeline")
        ar.append("جدول شراء قريب")
    return en, ar


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_base_scorer = LeadScorer()


def score_lead(lead: AILeadInput) -> AILeadScoreResult:
    """Score a single lead across BANT, behavioural, and heuristic dimensions.

    Returns an :class:`AILeadScoreResult` with bilingual reasoning.

    PDPL gate: if ``pdpl_consent.consent_obtained`` is False the governance
    decision is set to ``REQUIRE_APPROVAL`` and the score is capped at 30.
    """
    pdpl_cleared = lead.pdpl_consent.consent_obtained

    # Base heuristic (0-1)
    base: ScoreResult = _base_scorer.score(lead.base_features)
    heuristic_100 = base.score * 100

    # BANT (0-100)
    bant = _bant_score(lead.bant)

    # Behavioural (0-100)
    behav = _behavioural_score(lead.behavioural)

    # Sector multiplier applied to sector-fit component of the base score
    sector_mult = _sector_multiplier(lead.sector)
    sector_adjusted = min(100.0, heuristic_100 * sector_mult)

    # Weighted composite
    composite = (sector_adjusted * 0.40) + (bant * 0.35) + (behav * 0.25)
    final_score = int(min(100, max(0, composite)))

    # PDPL cap
    governance_decision = "ALLOW_WITH_REVIEW"
    if not pdpl_cleared:
        final_score = min(final_score, 30)
        governance_decision = "REQUIRE_APPROVAL"

    tier_en, tier_ar = _tier_label(final_score)
    action_en, action_ar = _recommended_action(tier_en)

    # Reasons
    reasons_en: list[str] = list(base.reasons)
    reasons_ar: list[str] = []
    bant_en, bant_ar = _bant_reasons(lead.bant)
    reasons_en.extend(bant_en)
    reasons_ar.extend(bant_ar)

    if not pdpl_cleared:
        reasons_en.append("PDPL consent not recorded — score capped at 30")
        reasons_ar.append("لم يُسجَّل موافقة نظام حماية البيانات — النقاط محدودة بـ 30")

    if lead.sector and sector_mult >= 1.3:
        reasons_en.append(f"High-priority Saudi sector: {lead.sector}")
        reasons_ar.append(f"قطاع سعودي ذو أولوية عالية: {lead.sector}")

    if lead.behavioural.referral_source:
        reasons_en.append("Referral source — higher trust signal")
        reasons_ar.append("مصدر إحالة — إشارة ثقة أعلى")

    return AILeadScoreResult(
        score=final_score,
        tier=tier_en,
        tier_ar=tier_ar,
        raw_heuristic=base.score,
        bant_score=bant,
        behavioural_score=behav,
        pdpl_cleared=pdpl_cleared,
        reasons_en=reasons_en,
        reasons_ar=reasons_ar,
        recommended_action_en=action_en,
        recommended_action_ar=action_ar,
        governance_decision=governance_decision,
    )


def batch_score(leads: list[AILeadInput]) -> list[AILeadScoreResult]:
    """Score a batch of leads and return results in the same order."""
    return [score_lead(lead) for lead in leads]


__all__ = [
    "AILeadInput",
    "AILeadScoreResult",
    "BANTSignals",
    "BehaviouralSignals",
    "PDPLConsent",
    "batch_score",
    "score_lead",
]
