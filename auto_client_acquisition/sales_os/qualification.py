"""Qualification — map discovery answers to a commercial verdict (no LLM)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from auto_client_acquisition.governance_os.draft_gate import audit_draft_text
from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals, client_risk_score
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score


class QualificationVerdict(StrEnum):
    ACCEPT = "accept"
    DIAGNOSTIC_ONLY = "diagnostic_only"
    REFRAME = "reframe"
    REJECT = "reject"
    REFER_OUT = "refer_out"


# Public alias — qualification decision values.
Decision = QualificationVerdict


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


@dataclass(frozen=True, slots=True)
class QualificationResult:
    """Outcome of a discovery-answer qualification pass."""

    decision: Decision
    score: int
    recommended_offer: str
    doctrine_violations: list[str] = field(default_factory=list)


# Forbidden-term substrings (English + Arabic) checked beyond ``audit_draft_text``.
_EXTRA_DOCTRINE_TERMS: tuple[tuple[str, str], ...] = (
    ("ضمان المبيعات", "guaranteed_sales"),
    ("ضمان مبيعات", "guaranteed_sales"),
)


def _map_doctrine_violation(flag: str) -> str:
    """Normalise a draft-gate flag into a stable doctrine violation token."""
    payload = flag.split(":", 1)[-1].strip().lower()
    if "whatsapp" in payload:
        return "cold_whatsapp"
    if "scrap" in payload:
        return "scraping"
    if "linkedin" in payload:
        return "linkedin_automation"
    if "guarantee" in payload:
        return "guaranteed_sales"
    return payload.replace(" ", "_")


def _scan_request_text(raw_request_text: str) -> list[str]:
    """Return doctrine violation tokens found in free-text intake."""
    violations: list[str] = []
    for flag in audit_draft_text(raw_request_text):
        token = _map_doctrine_violation(flag)
        if token not in violations:
            violations.append(token)
    blob = raw_request_text.lower()
    for term, token in _EXTRA_DOCTRINE_TERMS:
        if term in blob and token not in violations:
            violations.append(token)
    return violations


def qualify(
    *,
    pain_clear: bool,
    owner_present: bool,
    data_available: bool,
    accepts_governance: bool,
    has_budget: bool,
    wants_safe_methods: bool,
    proof_path_visible: bool,
    retainer_path_visible: bool,
    raw_request_text: str = "",
) -> QualificationResult:
    """Map discovery answers to a commercial verdict (deterministic, no LLM)."""
    signals = (
        pain_clear,
        owner_present,
        data_available,
        accepts_governance,
        has_budget,
        wants_safe_methods,
        proof_path_visible,
        retainer_path_visible,
    )
    score = round(sum(1 for signal in signals if signal) * 100 / len(signals))

    doctrine_violations = _scan_request_text(raw_request_text)
    if not wants_safe_methods and "declined_safe_methods" not in doctrine_violations:
        doctrine_violations.append("declined_safe_methods")

    if doctrine_violations:
        return QualificationResult(
            decision=Decision.REJECT,
            score=score,
            recommended_offer="none — doctrine violation must be resolved first",
            doctrine_violations=doctrine_violations,
        )

    if not accepts_governance:
        return QualificationResult(
            decision=Decision.REFER_OUT,
            score=score,
            recommended_offer="refer_out — governance model not accepted",
            doctrine_violations=doctrine_violations,
        )

    if score >= 95:
        decision = Decision.ACCEPT
        offer = "revenue_intelligence_sprint (data_to_revenue)"
    elif score >= 70:
        decision = Decision.DIAGNOSTIC_ONLY
        offer = "data_to_revenue_diagnostic"
    elif score >= 55:
        decision = Decision.REFRAME
        offer = "reframe_scope_then_diagnostic"
    elif score >= 35:
        decision = Decision.REFER_OUT
        offer = "refer_out — fit too low for a Dealix engagement"
    else:
        decision = Decision.REJECT
        offer = "none — insufficient readiness to engage"

    return QualificationResult(
        decision=decision,
        score=score,
        recommended_offer=offer,
        doctrine_violations=doctrine_violations,
    )


__all__ = [
    "Decision",
    "QualificationResult",
    "QualificationVerdict",
    "qualify",
    "qualify_opportunity",
]
