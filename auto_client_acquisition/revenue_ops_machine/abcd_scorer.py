"""Revenue Ops Machine — the A/B/C/D lead-scoring layer.

This classifier is new and additive. It does NOT replace the existing
``LeadRecord.fit_score`` / ``urgency_score`` or ``sales_os`` ICP scoring — it
sits alongside them and is the signal that routes a lead through the funnel
(grade A/B → qualified, C/D → nurture).

Formula (founder-specified):

    +3 decision maker          -3 student / job seeker
    +3 uses CRM                -3 no company
    +3 has AI/revenue automation   -2 vague curiosity
    +2 GCC B2B
    +2 urgency within 30 days
    +2 budget 5k+ SAR

    score >= 10 -> A    6..9 -> B    3..5 -> C    < 3 -> D
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.revenue_ops_machine.funnel_state import FunnelState

_GCC_REGION_TOKENS = (
    "saudi",
    "ksa",
    "السعودية",
    "riyadh",
    "الرياض",
    "jeddah",
    "uae",
    "emirates",
    "الإمارات",
    "qatar",
    "قطر",
    "kuwait",
    "الكويت",
    "bahrain",
    "البحرين",
    "oman",
    "عمان",
    "gcc",
    "الخليج",
)


@dataclass(frozen=True, slots=True)
class ABCDSignals:
    """The nine boolean inputs to the A/B/C/D score."""

    is_decision_maker: bool = False
    uses_crm: bool = False
    has_ai_revenue_automation: bool = False
    is_gcc_b2b: bool = False
    urgency_within_30d: bool = False
    budget_5k_plus_sar: bool = False
    is_student_or_jobseeker: bool = False
    has_no_company: bool = False
    vague_curiosity: bool = False

    def to_dict(self) -> dict[str, bool]:
        return {
            "is_decision_maker": self.is_decision_maker,
            "uses_crm": self.uses_crm,
            "has_ai_revenue_automation": self.has_ai_revenue_automation,
            "is_gcc_b2b": self.is_gcc_b2b,
            "urgency_within_30d": self.urgency_within_30d,
            "budget_5k_plus_sar": self.budget_5k_plus_sar,
            "is_student_or_jobseeker": self.is_student_or_jobseeker,
            "has_no_company": self.has_no_company,
            "vague_curiosity": self.vague_curiosity,
        }


_WEIGHTS: dict[str, int] = {
    "is_decision_maker": +3,
    "uses_crm": +3,
    "has_ai_revenue_automation": +3,
    "is_gcc_b2b": +2,
    "urgency_within_30d": +2,
    "budget_5k_plus_sar": +2,
    "is_student_or_jobseeker": -3,
    "has_no_company": -3,
    "vague_curiosity": -2,
}


def abcd_score(signals: ABCDSignals) -> int:
    """Sum the weighted signal vector."""
    flags = signals.to_dict()
    return sum(weight for name, weight in _WEIGHTS.items() if flags[name])


def classify(score: int) -> str:
    """Map a numeric score to an A/B/C/D grade."""
    if score >= 10:
        return "A"
    if score >= 6:
        return "B"
    if score >= 3:
        return "C"
    return "D"


def abcd_to_funnel_state(grade: str) -> FunnelState:
    """Route an A/B/C/D grade to the funnel state qualification produces.

    A/B are qualified leads; C/D enter nurture. A grade D is never auto-closed
    here — closing is an explicit decision (declined / doctrine violation).
    """
    grade = (grade or "").strip().upper()
    if grade == "A":
        return FunnelState.qualified_A
    if grade == "B":
        return FunnelState.qualified_B
    return FunnelState.nurture


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    return str(value).strip().lower() in {"1", "true", "yes", "y", "نعم"}


def signals_from_form(form: dict[str, Any]) -> ABCDSignals:
    """Derive the nine booleans from a raw lead-capture form / dict.

    Accepts explicit booleans when present, otherwise infers from common
    fields (``role``, ``budget``, ``region``/``sector``, ``urgency``,
    ``current_crm``, ``ai_usage``, ``company_name``). Keeps the scorer pure.
    """
    f = {str(k).lower(): v for k, v in (form or {}).items()}

    def pick(*keys: str) -> Any:
        for k in keys:
            if k in f and f[k] not in (None, ""):
                return f[k]
        return None

    role = str(pick("role", "title", "job_title") or "").lower()
    region_blob = " ".join(
        str(pick(k) or "") for k in ("region", "sector", "country", "city", "company_location")
    ).lower()
    budget_raw = pick("budget", "budget_range", "budget_sar")
    company = str(pick("company", "company_name", "organization") or "").strip()

    is_decision_maker = _truthy(f.get("is_decision_maker")) or any(
        token in role
        for token in (
            "founder",
            "ceo",
            "owner",
            "coo",
            "cmo",
            "director",
            "head",
            "vp",
            "chief",
            "manager",
            "مدير",
            "مؤسس",
            "رئيس",
        )
    )
    uses_crm = _truthy(f.get("uses_crm")) or bool(
        str(pick("current_crm", "crm") or "").strip()
        and str(pick("current_crm", "crm") or "").strip().lower()
        not in {"none", "no", "لا يوجد", "لا"}
    )
    ai_blob = str(pick("ai_usage", "ai_usage_today", "has_ai") or "").strip().lower()
    has_ai = _truthy(f.get("has_ai_revenue_automation")) or (
        bool(ai_blob) and ai_blob not in {"none", "no", "لا", "لا يوجد"}
    )
    is_gcc_b2b = _truthy(f.get("is_gcc_b2b")) or any(
        token in region_blob for token in _GCC_REGION_TOKENS
    )

    urgency = str(pick("urgency", "timeline") or "").lower()
    urgency_within_30d = _truthy(f.get("urgency_within_30d")) or any(
        token in urgency for token in ("now", "immediate", "30", "asap", "urgent", "عاجل", "فوري")
    )

    budget_5k_plus = _truthy(f.get("budget_5k_plus_sar"))
    if not budget_5k_plus and budget_raw is not None:
        if isinstance(budget_raw, (int, float)):
            budget_5k_plus = budget_raw >= 5000
        else:
            digits = "".join(ch for ch in str(budget_raw) if ch.isdigit())
            budget_5k_plus = bool(digits) and int(digits) >= 5000

    is_student_or_jobseeker = _truthy(f.get("is_student_or_jobseeker")) or any(
        token in role
        for token in (
            "student",
            "graduate",
            "job seeker",
            "jobseeker",
            "looking for",
            "طالب",
            "خريج",
            "باحث عن عمل",
        )
    )
    has_no_company = _truthy(f.get("has_no_company")) or not company
    vague_curiosity = _truthy(f.get("vague_curiosity"))

    return ABCDSignals(
        is_decision_maker=is_decision_maker,
        uses_crm=uses_crm,
        has_ai_revenue_automation=has_ai,
        is_gcc_b2b=is_gcc_b2b,
        urgency_within_30d=urgency_within_30d,
        budget_5k_plus_sar=budget_5k_plus,
        is_student_or_jobseeker=is_student_or_jobseeker,
        has_no_company=has_no_company,
        vague_curiosity=vague_curiosity,
    )


@dataclass(frozen=True, slots=True)
class ABCDResult:
    """Score + grade + the signal vector that produced them."""

    score: int
    grade: str
    signals: ABCDSignals = field(default_factory=ABCDSignals)

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "grade": self.grade,
            "signals": self.signals.to_dict(),
        }


def score_form(form: dict[str, Any]) -> ABCDResult:
    """Convenience: form dict -> full A/B/C/D result."""
    signals = signals_from_form(form)
    score = abcd_score(signals)
    return ABCDResult(score=score, grade=classify(score), signals=signals)


# Grade -> recommended offer from the existing 5-rung ladder (read-only routing;
# pricing is never changed by the machine).
_OFFER_BY_GRADE: dict[str, str] = {
    "A": "revenue_proof_sprint_499",
    "B": "free_mini_diagnostic",
    "C": "free_mini_diagnostic",
    "D": "free_mini_diagnostic",
}


def recommend_offer(grade: str) -> str:
    """Return the existing-ladder offer id to route this grade toward."""
    return _OFFER_BY_GRADE.get((grade or "").strip().upper(), "free_mini_diagnostic")


__all__ = [
    "ABCDSignals",
    "ABCDResult",
    "abcd_score",
    "classify",
    "abcd_to_funnel_state",
    "signals_from_form",
    "score_form",
    "recommend_offer",
]
