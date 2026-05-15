"""Qualification — map discovery answers to a commercial verdict (no LLM)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals, client_risk_score
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score


class QualificationVerdict(StrEnum):
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


# ── Discovery-answer qualifier (deterministic, doctrine-gated) ────────

# ``Decision`` is the public alias used by the discovery-answer qualifier;
# values are identical to ``QualificationVerdict``.
Decision = QualificationVerdict

# Doctrine red lines — any hit forces REJECT (Article 8 non-negotiables).
_DOCTRINE_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("scraping", ("scrape", "scraping", "كشط", "سحب بيانات")),
    (
        "cold_whatsapp_automation",
        ("cold whatsapp", "whatsapp automation", "whatsapp blast", "واتساب بارد"),
    ),
    ("linkedin_automation", ("linkedin automation", "auto connect", "أتمتة لينكدإن")),
    (
        "guaranteed_sales_claim",
        ("guarantee sales", "guaranteed sales", "ضمان المبيعات", "نضمن المبيعات"),
    ),
)


@dataclass(frozen=True, slots=True)
class QualificationResult:
    decision: QualificationVerdict
    score: int
    recommended_offer: str
    reasons: tuple[str, ...]
    doctrine_violations: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "decision": self.decision.value,
            "score": self.score,
            "recommended_offer": self.recommended_offer,
            "reasons": list(self.reasons),
            "doctrine_violations": list(self.doctrine_violations),
        }


def _scan_doctrine(raw_request_text: str) -> list[str]:
    hits: list[str] = []
    lowered = raw_request_text.lower()
    for violation, needles in _DOCTRINE_PATTERNS:
        if any(n in lowered or n in raw_request_text for n in needles):
            hits.append(violation)
    return hits


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
    """Map discovery answers + the raw request to a commercial verdict.

    Deterministic and doctrine-gated: any non-negotiable red line in the
    request text — or a client declining safe methods — forces REJECT.
    """
    answers = {
        "pain_clear": pain_clear,
        "owner_present": owner_present,
        "data_available": data_available,
        "accepts_governance": accepts_governance,
        "has_budget": has_budget,
        "wants_safe_methods": wants_safe_methods,
        "proof_path_visible": proof_path_visible,
        "retainer_path_visible": retainer_path_visible,
    }
    score = round(100 * sum(1 for v in answers.values() if v) / len(answers))

    violations = _scan_doctrine(raw_request_text)
    if not wants_safe_methods:
        violations.append("declined_safe_methods")

    if violations:
        return QualificationResult(
            decision=QualificationVerdict.REJECT,
            score=score,
            recommended_offer="none_doctrine_block",
            reasons=("doctrine_red_line",),
            doctrine_violations=tuple(violations),
        )

    reasons = tuple(k for k, v in answers.items() if not v) or ("all_signals_present",)

    if score >= 90:
        offer = (
            "revenue_intelligence_sprint" if data_available else "data_to_revenue_pack"
        )
        decision = QualificationVerdict.ACCEPT
    elif score >= 60:
        offer = "ai_ops_diagnostic" if not data_available else "data_to_revenue_pack"
        decision = QualificationVerdict.DIAGNOSTIC_ONLY
    elif score >= 40:
        offer = "free_diagnostic"
        decision = QualificationVerdict.REFRAME
    else:
        offer = "refer_out"
        decision = QualificationVerdict.REFER_OUT

    return QualificationResult(
        decision=decision,
        score=score,
        recommended_offer=offer,
        reasons=reasons,
        doctrine_violations=(),
    )


__all__ = [
    "Decision",
    "QualificationResult",
    "QualificationVerdict",
    "qualify",
    "qualify_opportunity",
]
