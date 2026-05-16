"""Decision passport assembly for the Revenue Ops Diagnostic.

A decision passport is the diagnostic's single-page recommendation: where the
account stands, what is recommended next, and the evidence behind it. It is a
governed summary — every recommendation is an estimate, never a guarantee.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from auto_client_acquisition.revenue_ops.scoring import ReadinessScore

# Readiness band -> the next recommended service in the ladder.
_BAND_TO_NEXT_SERVICE: dict[str, str] = {
    "ai_ready": "governed_ops_retainer",
    "sprint_ready": "revenue_intelligence_sprint",
    "diagnostic_in_progress": "revenue_intelligence_sprint",
    "foundational_gaps": "crm_data_readiness_for_ai",
}


@dataclass(frozen=True)
class DecisionPassportSummary:
    """A governed, evidence-backed next-step recommendation."""

    diagnostic_id: str
    customer_id: str
    account_id: str
    readiness_score: int
    readiness_band: str
    recommended_next_service: str
    rationale_en: str
    rationale_ar: str
    evidence: dict[str, object] = field(default_factory=dict)
    is_estimate: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "diagnostic_id": self.diagnostic_id,
            "customer_id": self.customer_id,
            "account_id": self.account_id,
            "readiness_score": self.readiness_score,
            "readiness_band": self.readiness_band,
            "recommended_next_service": self.recommended_next_service,
            "rationale_en": self.rationale_en,
            "rationale_ar": self.rationale_ar,
            "evidence": dict(self.evidence),
            "is_estimate": self.is_estimate,
        }


def build_decision_passport(
    *,
    diagnostic_id: str,
    customer_id: str,
    account_id: str,
    readiness: ReadinessScore,
    commercial_state: str | None = None,
    cel: str | None = None,
) -> DecisionPassportSummary:
    """Assemble a decision passport from a diagnostic's readiness score.

    Args:
        diagnostic_id: the diagnostic this passport summarizes.
        customer_id: the Dealix customer.
        account_id: the diagnosed account.
        readiness: the deterministic `ReadinessScore`.
        commercial_state: the account's current CEL state, if known.
        cel: the account's current CEL level, if known.

    Returns:
        A `DecisionPassportSummary`. Recommendations are estimates.
    """
    next_service = _BAND_TO_NEXT_SERVICE.get(
        readiness.band, "revenue_intelligence_sprint"
    )
    rationale_en = (
        f"Revenue readiness scored {readiness.score}/100 "
        f"({readiness.band}); the recommended next step is "
        f"'{next_service}'. This is an estimate based on the signals reviewed."
    )
    rationale_ar = (
        f"درجة جاهزية الإيراد {readiness.score}/100 "
        f"({readiness.band})؛ الخطوة التالية الموصى بها هي '{next_service}'. "
        "هذا تقدير مبني على الإشارات التي تمت مراجعتها."
    )
    return DecisionPassportSummary(
        diagnostic_id=diagnostic_id,
        customer_id=customer_id,
        account_id=account_id,
        readiness_score=readiness.score,
        readiness_band=readiness.band,
        recommended_next_service=next_service,
        rationale_en=rationale_en,
        rationale_ar=rationale_ar,
        evidence={
            "present_signals": list(readiness.present_signals),
            "missing_signals": list(readiness.missing_signals),
            "commercial_state": commercial_state,
            "cel": cel,
        },
    )
