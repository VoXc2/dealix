"""Qualification — map discovery answers to a commercial verdict (no LLM)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals, client_risk_score
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score


class QualificationVerdict(StrEnum):
    ACCEPT = "accept"
    DIAGNOSTIC_ONLY = "diagnostic_only"
    REFRAME = "reframe"
    REJECT = "reject"
    REFER_OUT = "refer_out"


class Decision(StrEnum):
    """Commercial qualification decision (aligned with the verdict ladder)."""

    ACCEPT = "accept"
    DIAGNOSTIC_ONLY = "diagnostic_only"
    REFRAME = "reframe"
    REJECT = "reject"
    REFER_OUT = "refer_out"


def qualify_opportunity(
    *,
    icp: ICPDimensions,
    risk: ClientRiskSignals,
    accepts_governance: bool,
    proof_path_possible: bool,
) -> tuple[QualificationVerdict, tuple[str, ...]]:
    reasons: list[str] = []
    icp_s = icp_score(icp)
    r = client_risk_score(risk)
    if risk.wants_scraping_or_spam or risk.wants_guaranteed_sales:
        return QualificationVerdict.REJECT, ("non_negotiable_risk",)
    if r >= 55:
        return QualificationVerdict.REJECT, ("high_client_risk",)
    if not accepts_governance:
        return QualificationVerdict.REFER_OUT, ("governance_not_accepted",)
    if not proof_path_possible:
        reasons.append("weak_proof_path")
        if icp_s < 50:
            return QualificationVerdict.DIAGNOSTIC_ONLY, tuple(reasons)
        return QualificationVerdict.REFRAME, tuple(reasons)
    if icp_s < 45:
        return QualificationVerdict.DIAGNOSTIC_ONLY, ("icp_low_start_with_diagnostic",)
    if icp_s < 60:
        return QualificationVerdict.REFRAME, ("icp_mid_package_shape",)
    return QualificationVerdict.ACCEPT, ("icp_ok_risk_ok",)


# Weight of each discovery flag — sums to 100.
_QUALIFY_WEIGHTS: dict[str, int] = {
    "pain_clear": 15,
    "owner_present": 15,
    "data_available": 15,
    "accepts_governance": 10,
    "has_budget": 10,
    "wants_safe_methods": 10,
    "proof_path_visible": 15,
    "retainer_path_visible": 10,
}

# Doctrine triggers checked against the free-text request (English + Arabic).
_DOCTRINE_TEXT_TRIGGERS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "cold_whatsapp",
        ("cold whatsapp", "whatsapp blast", "blast leads", "واتساب"),
    ),
    (
        "guaranteed_sales",
        ("guarantee sales", "guaranteed sales", "guaranteed results",
         "guaranteed roi", "ضمان المبيعات", "نضمن"),
    ),
    (
        "scraping",
        ("scrape", "scraping", "web scrape", "harvest emails"),
    ),
    (
        "linkedin_automation",
        ("linkedin automation", "automate linkedin", "scrape linkedin"),
    ),
)


@dataclass(frozen=True, slots=True)
class QualificationResult:
    """Outcome of a discovery-call qualification."""

    decision: str
    score: int
    recommended_offer: str
    reasons: list[str] = field(default_factory=list)
    doctrine_violations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _scan_doctrine(text: str) -> list[str]:
    lowered = (text or "").lower()
    violations: list[str] = []
    for label, triggers in _DOCTRINE_TEXT_TRIGGERS:
        if any(t in lowered for t in triggers):
            violations.append(label)
    return violations


def qualify(
    *,
    pain_clear: bool = False,
    owner_present: bool = False,
    data_available: bool = False,
    accepts_governance: bool = False,
    has_budget: bool = False,
    wants_safe_methods: bool = True,
    proof_path_visible: bool = False,
    retainer_path_visible: bool = False,
    raw_request_text: str = "",
    sector: str = "",
    city: str = "",
) -> QualificationResult:
    """Score a discovery call and return a deterministic commercial verdict.

    Doctrine violations (cold WhatsApp, guaranteed-sales claims, scraping,
    LinkedIn automation, or a refusal of safe methods) force a reject — they
    are non-negotiable regardless of score.
    """
    flags = {
        "pain_clear": pain_clear,
        "owner_present": owner_present,
        "data_available": data_available,
        "accepts_governance": accepts_governance,
        "has_budget": has_budget,
        "wants_safe_methods": wants_safe_methods,
        "proof_path_visible": proof_path_visible,
        "retainer_path_visible": retainer_path_visible,
    }
    score = sum(_QUALIFY_WEIGHTS[k] for k, v in flags.items() if v)

    doctrine_violations = _scan_doctrine(raw_request_text)
    if not wants_safe_methods:
        doctrine_violations.append("declined_safe_methods")

    reasons: list[str] = []
    if doctrine_violations:
        reasons.append("doctrine_violation_blocks_engagement")
        return QualificationResult(
            decision=Decision.REJECT.value,
            score=score,
            recommended_offer="not_a_fit_decline_politely",
            reasons=reasons,
            doctrine_violations=doctrine_violations,
        )

    if not accepts_governance:
        return QualificationResult(
            decision=Decision.REFER_OUT.value,
            score=score,
            recommended_offer="refer_out_governance_not_accepted",
            reasons=["governance_not_accepted"],
        )

    if score >= 85:
        decision = Decision.ACCEPT
        offer = "revenue_intelligence_sprint"
        reasons.append("strong_fit_across_discovery_signals")
    elif score >= 70:
        decision = Decision.REFRAME if data_available else Decision.DIAGNOSTIC_ONLY
        offer = "data_to_revenue_diagnostic"
        reasons.append("partial_fit_shape_a_smaller_first_step")
    elif score >= 45:
        decision = Decision.DIAGNOSTIC_ONLY
        offer = "capability_diagnostic"
        reasons.append("low_signal_start_with_a_diagnostic")
    else:
        decision = Decision.REFER_OUT
        offer = "refer_out_not_enough_fit"
        reasons.append("insufficient_fit_to_engage")

    return QualificationResult(
        decision=decision.value,
        score=score,
        recommended_offer=offer,
        reasons=reasons,
        doctrine_violations=doctrine_violations,
    )


__all__ = [
    "Decision",
    "QualificationResult",
    "QualificationVerdict",
    "qualify",
    "qualify_opportunity",
]
