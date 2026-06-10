"""Retainer Eligibility Engine — determines whether a sprint client qualifies
for a Managed Ops retainer after completing the Revenue Intelligence Sprint.

Eligibility rules:
  - proof_level >= L1
  - satisfaction_score >= 7
  - measurable_result_achieved is True

Recommended tier is determined by proof level and satisfaction:
  - L3-L4 + satisfaction >= 9  → scale_4999
  - L2-L3 + satisfaction >= 8  → growth_3999
  - Otherwise eligible         → starter_2999
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

ProofLevel = Literal["L0", "L1", "L2", "L3", "L4"]
RetainerTier = Literal["starter_2999", "growth_3999", "scale_4999"]

_PROOF_LEVEL_RANK: dict[ProofLevel, int] = {
    "L0": 0,
    "L1": 1,
    "L2": 2,
    "L3": 3,
    "L4": 4,
}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class RetainerEligibilityCheck(BaseModel):
    """Result of the retainer eligibility evaluation for one sprint."""

    model_config = ConfigDict(extra="forbid")

    sprint_id: str = Field(..., min_length=1)
    account_id: str = Field(..., min_length=1)
    proof_level: ProofLevel = Field(..., description="Highest proof level achieved in the sprint.")
    satisfaction_score: float = Field(
        ..., ge=0.0, le=10.0, description="Founder/client satisfaction 0-10."
    )
    measurable_result_achieved: bool = Field(
        ..., description="At least one measurable, documented outcome reached."
    )
    is_eligible: bool = Field(
        default=False, description="True when all eligibility criteria are met."
    )
    recommended_tier: RetainerTier | None = Field(
        default=None, description="Tier to propose when eligible."
    )
    ineligibility_reasons: list[str] = Field(
        default_factory=list,
        description="Reasons for ineligibility (empty when eligible).",
    )
    upsell_pitch_ar: str = Field(default="", description="Arabic upsell pitch text.")
    upsell_pitch_en: str = Field(default="", description="English upsell pitch text.")


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

_MIN_PROOF_LEVEL: ProofLevel = "L1"
_MIN_SATISFACTION: float = 7.0

_TIER_PITCHES: dict[RetainerTier, tuple[str, str]] = {
    "starter_2999": (
        "انضم إلى باقة Starter بـ 2,999 ريال/شهر واحصل على دعم عمليات منتظم، "
        "ومراجعة شهرية للعملاء المحتملين، وتقارير أداء موثَّقة.",
        "Join the Starter plan at 2,999 SAR/month for regular operations support, "
        "monthly pipeline reviews, and documented performance reports.",
    ),
    "growth_3999": (
        "ارتقِ إلى باقة Growth بـ 3,999 ريال/شهر لتحصل على إدارة كاملة للعملاء المحتملين، "
        "وسِجل قيمة شهري، ومراجعة استراتيجية كل أسبوعين.",
        "Upgrade to the Growth plan at 3,999 SAR/month for full pipeline management, "
        "a monthly value ledger, and bi-weekly strategy reviews.",
    ),
    "scale_4999": (
        "انضم إلى باقة Scale بـ 4,999 ريال/شهر وادفع نمو مؤسستك عبر عمليات ذكاء اصطناعي "
        "مُدارة بالكامل، وتقارير مجلس الإدارة، وتكامل مع أنظمة CRM.",
        "Join the Scale plan at 4,999 SAR/month to power your growth with fully managed "
        "AI operations, board-ready reports, and CRM system integration.",
    ),
}


def _determine_tier(proof_level: ProofLevel, satisfaction: float) -> RetainerTier:
    rank = _PROOF_LEVEL_RANK[proof_level]
    if rank >= 3 and satisfaction >= 9.0:
        return "scale_4999"
    if rank >= 2 and satisfaction >= 8.0:
        return "growth_3999"
    return "starter_2999"


class RetainerEligibilityEngine:
    """Evaluates post-sprint retainer eligibility. No external I/O."""

    def check(self, sprint_result: dict) -> RetainerEligibilityCheck:
        """Evaluate eligibility from a sprint result dict.

        Required keys in *sprint_result*:
            sprint_id (str), account_id (str), proof_level (str),
            satisfaction_score (float), measurable_result_achieved (bool).
        """
        sprint_id: str = str(sprint_result.get("sprint_id", ""))
        account_id: str = str(sprint_result.get("account_id", ""))
        proof_level_raw: str = str(sprint_result.get("proof_level", "L0"))
        satisfaction: float = float(sprint_result.get("satisfaction_score", 0.0))
        measurable: bool = bool(sprint_result.get("measurable_result_achieved", False))

        # Normalise proof level
        proof_level: ProofLevel = proof_level_raw if proof_level_raw in _PROOF_LEVEL_RANK else "L0"  # type: ignore[assignment]

        ineligibility_reasons: list[str] = []

        # Gate 1: proof level
        if _PROOF_LEVEL_RANK[proof_level] < _PROOF_LEVEL_RANK[_MIN_PROOF_LEVEL]:
            ineligibility_reasons.append(
                f"proof_level_too_low: {proof_level} < {_MIN_PROOF_LEVEL}"
            )

        # Gate 2: satisfaction
        if satisfaction < _MIN_SATISFACTION:
            ineligibility_reasons.append(
                f"satisfaction_below_threshold: {satisfaction} < {_MIN_SATISFACTION}"
            )

        # Gate 3: measurable result
        if not measurable:
            ineligibility_reasons.append("no_measurable_result_achieved")

        is_eligible = len(ineligibility_reasons) == 0
        recommended_tier: RetainerTier | None = None
        upsell_ar = ""
        upsell_en = ""

        if is_eligible:
            recommended_tier = _determine_tier(proof_level, satisfaction)
            upsell_ar, upsell_en = _TIER_PITCHES[recommended_tier]

        return RetainerEligibilityCheck(
            sprint_id=sprint_id,
            account_id=account_id,
            proof_level=proof_level,
            satisfaction_score=satisfaction,
            measurable_result_achieved=measurable,
            is_eligible=is_eligible,
            recommended_tier=recommended_tier,
            ineligibility_reasons=ineligibility_reasons,
            upsell_pitch_ar=upsell_ar,
            upsell_pitch_en=upsell_en,
        )
