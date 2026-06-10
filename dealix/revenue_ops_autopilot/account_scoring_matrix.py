"""Account Scoring Matrix — ranks accounts by composite revenue potential.

Scoring weights (§ spec):
    pain_score       30 %
    engagement_score 25 %
    deal_readiness   25 %
    sector_fit       20 %

All scores are deterministic; no LLM calls, no external I/O.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

DealReadiness = Literal["HIGH", "MEDIUM", "LOW"]

# GCC / Saudi-relevant high-fit sectors
_HIGH_FIT_SECTORS: frozenset[str] = frozenset(
    {
        "logistics",
        "retail",
        "ecommerce",
        "fintech",
        "real_estate",
        "construction",
        "healthcare",
        "education",
        "technology",
        "telecom",
        "manufacturing",
        "oil_gas",
        "hospitality",
    }
)

_MEDIUM_FIT_SECTORS: frozenset[str] = frozenset(
    {
        "consulting",
        "legal",
        "media",
        "advertising",
        "hr",
        "recruitment",
        "training",
        "ngo",
        "government",
    }
)

_DEAL_READINESS_SCORE: dict[DealReadiness, float] = {
    "HIGH": 100.0,
    "MEDIUM": 60.0,
    "LOW": 20.0,
}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class AccountProfile(BaseModel):
    """Input profile for a single account."""

    model_config = ConfigDict(extra="forbid")

    company_name: str = Field(..., min_length=1)
    sector: str = Field(default="", description="Industry vertical (lowercase, underscored).")
    current_revenue_sar: float = Field(
        default=0.0, ge=0.0, description="Estimated or known annual revenue in SAR."
    )
    growth_signals: list[str] = Field(
        default_factory=list,
        description="Observable growth indicators, e.g. 'hiring_fast', 'new_funding'.",
    )
    pain_score: float = Field(
        ..., ge=0.0, le=10.0, description="Assessed pain intensity 0-10."
    )
    engagement_score: float = Field(
        ..., ge=0.0, le=10.0, description="Interaction depth 0-10."
    )
    deal_readiness: DealReadiness = Field(
        ..., description="Buyer readiness: HIGH / MEDIUM / LOW."
    )


class ScoredAccount(BaseModel):
    """Output — account with composite score and recommended actions."""

    model_config = ConfigDict(extra="forbid")

    account: AccountProfile
    composite_score: float = Field(..., ge=0.0, le=100.0)
    priority_rank: int = Field(..., ge=1)
    recommended_action_ar: str = ""
    recommended_action_en: str = ""


# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------


def _sector_fit_score(sector: str) -> float:
    """Map a sector string to a 0-100 fit score."""
    s = sector.strip().lower().replace(" ", "_").replace("-", "_")
    if s in _HIGH_FIT_SECTORS:
        return 100.0
    if s in _MEDIUM_FIT_SECTORS:
        return 60.0
    return 30.0  # unknown / low-fit


def _growth_bonus(growth_signals: list[str]) -> float:
    """Small composite bonus (0-10) for observable growth signals."""
    _SIGNAL_SCORES: dict[str, float] = {
        "new_funding": 4.0,
        "hiring_fast": 3.0,
        "product_launch": 3.0,
        "geographic_expansion": 3.0,
        "new_leadership": 2.5,
        "ipo_preparation": 4.0,
        "partnership_announced": 2.0,
        "revenue_milestone": 3.5,
    }
    total = sum(_SIGNAL_SCORES.get(sig.lower().strip().replace(" ", "_"), 1.0) for sig in growth_signals)
    return min(10.0, total)


def _recommend(account: AccountProfile, score: float) -> tuple[str, str]:
    """Generate short bilingual recommended action based on score bucket."""
    name = account.company_name
    if score >= 80:
        ar = f"أولوية قصوى: تواصل مع {name} فوراً، اعرض Sprint خلال 48 ساعة."
        en = f"Top priority: reach out to {name} immediately; propose Sprint within 48 h."
    elif score >= 60:
        ar = f"أولوية عالية: جدوِّل اجتماعاً مع {name} هذا الأسبوع لتأهيل الفرصة."
        en = f"High priority: schedule a call with {name} this week to qualify the opportunity."
    elif score >= 40:
        ar = f"متابعة: أرسل حزمة توعية لـ{name} وأعِد التقييم بعد 30 يوماً."
        en = f"Nurture: send a value-education package to {name} and re-evaluate in 30 days."
    else:
        ar = f"منخفض: ضع {name} في قائمة المتابعة بعيدة المدى، لا إجراء فوري."
        en = f"Low priority: place {name} in a long-term watch list; no immediate action."
    return ar, en


class AccountScoringMatrix:
    """Scores and ranks a list of AccountProfile objects."""

    # Weights must sum to 1.0
    _W_PAIN = 0.30
    _W_ENGAGEMENT = 0.25
    _W_DEAL_READINESS = 0.25
    _W_SECTOR_FIT = 0.20

    def score_accounts(self, accounts: list[AccountProfile]) -> list[ScoredAccount]:
        """Return accounts sorted descending by composite score (rank 1 = best)."""
        if not accounts:
            return []

        scored: list[tuple[float, AccountProfile]] = []

        for account in accounts:
            # Normalise component inputs to 0-100 range
            pain_norm = account.pain_score * 10.0           # 0-10 → 0-100
            engagement_norm = account.engagement_score * 10.0  # 0-10 → 0-100
            readiness_norm = _DEAL_READINESS_SCORE[account.deal_readiness]
            sector_norm = _sector_fit_score(account.sector)

            composite = (
                self._W_PAIN * pain_norm
                + self._W_ENGAGEMENT * engagement_norm
                + self._W_DEAL_READINESS * readiness_norm
                + self._W_SECTOR_FIT * sector_norm
            )

            # Growth signals add a small bonus (max ~5 pts) on top of the
            # weighted composite to break ties meaningfully.
            growth_bonus = _growth_bonus(account.growth_signals) * 0.5
            composite = min(100.0, composite + growth_bonus)

            scored.append((round(composite, 2), account))

        # Sort descending
        scored.sort(key=lambda x: x[0], reverse=True)

        results: list[ScoredAccount] = []
        for rank, (score, account) in enumerate(scored, start=1):
            ar, en = _recommend(account, score)
            results.append(
                ScoredAccount(
                    account=account,
                    composite_score=score,
                    priority_rank=rank,
                    recommended_action_ar=ar,
                    recommended_action_en=en,
                )
            )

        return results
