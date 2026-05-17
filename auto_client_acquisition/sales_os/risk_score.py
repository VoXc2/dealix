"""AI & Revenue Ops Risk Score — the lead-magnet scorer (no LLM).

A 7-question diagnostic that maps a team's answers to a deterministic
Low / Medium / High governance-risk band plus a recommended next step.
Mirrors the weighted-flag pattern of ``sales_os.qualification.qualify``.

Risk semantics: a *gap* in governance raises the score. The questions
probe the four pillars Dealix sells against — source clarity, approval
boundaries, evidence trails, proof of value.

Doctrine: if the free-text context asks for scraping, cold WhatsApp, or
guaranteed-sales claims, the band is forced to High — those are
non-negotiable governance failures regardless of the questionnaire score.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class RiskLevel(StrEnum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# Weight of each risk signal — sums to 100. A signal is "present" when the
# answer reveals a governance gap (see ``score_risk``).
_RISK_WEIGHTS: dict[str, int] = {
    "no_approval_boundary": 22,
    "cannot_link_ai_to_value": 16,
    "no_ai_evidence_pack": 16,
    "decision_source_unknown": 14,
    "followup_undocumented": 12,
    "no_crm": 12,
    "uses_ai": 8,
}

_MEDIUM_THRESHOLD = 30
_HIGH_THRESHOLD = 60

# Doctrine triggers checked against the free-text context (English + Arabic).
_DOCTRINE_TEXT_TRIGGERS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("cold_whatsapp", ("cold whatsapp", "whatsapp blast", "blast leads", "واتساب")),
    (
        "guaranteed_sales",
        ("guarantee sales", "guaranteed sales", "guaranteed results",
         "guaranteed roi", "ضمان المبيعات", "نضمن"),
    ),
    ("scraping", ("scrape", "scraping", "web scrape", "harvest emails")),
    ("linkedin_automation", ("linkedin automation", "automate linkedin")),
)

_RECOMMENDED_OFFER = "governed_diagnostic_starter_4999"

_NEXT_STEP: dict[RiskLevel, tuple[str, str]] = {
    RiskLevel.LOW: (
        "Your operating layer is relatively governed. Book a Diagnostic "
        "Review to validate one workflow and confirm the evidence trail.",
        "book_diagnostic_review",
    ),
    RiskLevel.MEDIUM: (
        "Governance gaps are creating measurable revenue and AI risk. Get a "
        "sample Proof Pack, then start with the 7-Day Governed Diagnostic.",
        "get_sample_proof_pack",
    ),
    RiskLevel.HIGH: (
        "Multiple governance gaps — high risk of revenue leakage and unsafe "
        "AI usage. Book a Diagnostic Review; the Standard or Executive tier "
        "is recommended given the scope.",
        "book_diagnostic_review",
    ),
}


@dataclass(frozen=True, slots=True)
class RiskScoreResult:
    """Outcome of the AI & Revenue Ops Risk Score questionnaire."""

    risk_level: str
    score: int
    risk_signals: list[str] = field(default_factory=list)
    recommended_next_step: str = ""
    cta: str = ""
    recommended_offer: str = _RECOMMENDED_OFFER
    doctrine_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _scan_doctrine(text: str) -> list[str]:
    lowered = (text or "").lower()
    flags: list[str] = []
    for label, triggers in _DOCTRINE_TEXT_TRIGGERS:
        if any(t in lowered for t in triggers):
            flags.append(label)
    return flags


def score_risk(
    *,
    has_crm: bool = False,
    uses_ai_in_sales_or_ops: bool = False,
    approval_before_external_messages: bool = False,
    can_link_ai_to_financial_outcome: bool = False,
    followup_documented: bool = False,
    knows_source_of_every_decision: bool = False,
    has_ai_evidence_pack: bool = False,
    context_text: str = "",
) -> RiskScoreResult:
    """Score the 7-question questionnaire into a Low/Medium/High band.

    Each argument is the team's answer (``True`` = yes). A *gap* — the
    answer that reveals missing governance — turns on the matching risk
    signal. ``uses_ai_in_sales_or_ops`` is the only signal where ``True``
    itself adds risk: AI in use is surface area that the other gaps amplify.
    """
    risk_flags = {
        "no_crm": not has_crm,
        "uses_ai": uses_ai_in_sales_or_ops,
        "no_approval_boundary": not approval_before_external_messages,
        "cannot_link_ai_to_value": not can_link_ai_to_financial_outcome,
        "followup_undocumented": not followup_documented,
        "decision_source_unknown": not knows_source_of_every_decision,
        "no_ai_evidence_pack": not has_ai_evidence_pack,
    }
    score = sum(_RISK_WEIGHTS[k] for k, present in risk_flags.items() if present)
    signals = sorted(k for k, present in risk_flags.items() if present)

    doctrine_flags = _scan_doctrine(context_text)

    if doctrine_flags or score >= _HIGH_THRESHOLD:
        level = RiskLevel.HIGH
    elif score >= _MEDIUM_THRESHOLD:
        level = RiskLevel.MEDIUM
    else:
        level = RiskLevel.LOW

    next_step, cta = _NEXT_STEP[level]
    if doctrine_flags:
        next_step = (
            "Your request includes a non-governed practice "
            f"({', '.join(doctrine_flags)}). " + next_step
        )

    return RiskScoreResult(
        risk_level=level.value,
        score=score,
        risk_signals=signals,
        recommended_next_step=next_step,
        cta=cta,
        recommended_offer=_RECOMMENDED_OFFER,
        doctrine_flags=doctrine_flags,
    )


__all__ = [
    "RiskLevel",
    "RiskScoreResult",
    "score_risk",
]
