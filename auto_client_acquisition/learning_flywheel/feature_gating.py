"""Wave 12 §32.3.11 — Feature Request Triage.

Implements the founder's "build only when justified" rule from plan §32.3.11:

    Only mark a feature as BUILD_QUEUE when:
    - ≥3 different customers asked for it, OR
    - it closed a paid deal, OR
    - it would reduce delivery time (founder hours), OR
    - it would raise retention/proof level

Otherwise: DEFER (with explicit reason).

Hard rule (Article 11): protects against speculative feature work
that doesn't serve revenue.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

FeatureRequestStatus = Literal[
    "BUILD_QUEUE",          # all gates met — safe to build
    "BUILD_QUEUE_PAID",     # auto-build because tied to paid deal
    "DEFER_INSUFFICIENT",   # < 3 customers asked + no paid tie
    "DEFER_NO_REVENUE_TIE", # asked but no measurable benefit
    "REJECTED_UNSAFE",      # violates a hard gate
]


@dataclass(frozen=True, slots=True)
class TriageDecision:
    """Triage outcome for a feature request."""

    status: FeatureRequestStatus
    customer_count: int
    closes_paid_deal: bool
    reduces_delivery_time: bool
    raises_retention_or_proof: bool
    violates_hard_gate: bool
    reason_ar: str
    reason_en: str
    rationale_tags: tuple[str, ...] = field(default_factory=tuple)


# Hard-gate violations — ANY of these → REJECTED_UNSAFE regardless
# of customer demand. Article 4 immutable.
_GATE_VIOLATION_KEYWORDS: tuple[str, ...] = (
    # English
    "auto send", "auto-send", "blast", "cold whatsapp", "cold outreach",
    "scrape", "scraping", "linkedin auto", "live charge", "auto charge",
    "guaranteed", "fake proof", "without consent",
    # Arabic
    "إرسال تلقائي", "بلاست", "واتساب بارد", "تواصل بارد",
    "مضمون", "نضمن", "أتمتة لينكدإن", "بدون موافقة",
)


def _violates_gate(request_text: str) -> bool:
    """True when the request text mentions a hard-gate violation."""
    lower = (request_text or "").lower()
    return any(kw in lower for kw in _GATE_VIOLATION_KEYWORDS)


def triage_feature_request(
    *,
    request_text: str,
    customer_handles_who_asked: list[str] | tuple[str, ...],
    closes_paid_deal: bool = False,
    reduces_delivery_time: bool = False,
    raises_retention_or_proof: bool = False,
) -> TriageDecision:
    """Triage a feature request per the §32.3.11 rule.

    Args:
        request_text: Free-form description of the requested feature.
        customer_handles_who_asked: Set/list of distinct customers who
            asked for this feature. Length determines the ≥3 gate.
        closes_paid_deal: Founder confirmed this would close a deal.
        reduces_delivery_time: Founder confirmed this would cut hours.
        raises_retention_or_proof: Founder confirmed this would lift
            retention or proof level.

    Returns:
        TriageDecision with status + bilingual reason + tags.
    """
    # Step 1: hard-gate check (always blocks)
    if _violates_gate(request_text):
        return TriageDecision(
            status="REJECTED_UNSAFE",
            customer_count=len(set(customer_handles_who_asked)),
            closes_paid_deal=closes_paid_deal,
            reduces_delivery_time=reduces_delivery_time,
            raises_retention_or_proof=raises_retention_or_proof,
            violates_hard_gate=True,
            reason_ar="مرفوض — يخالف أحد البوابات الصارمة (Article 4)",
            reason_en="Rejected — violates one of the 8 hard gates (Article 4)",
            rationale_tags=("hard_gate_violation",),
        )

    # Step 2: paid-deal shortcut → auto-build
    if closes_paid_deal:
        return TriageDecision(
            status="BUILD_QUEUE_PAID",
            customer_count=len(set(customer_handles_who_asked)),
            closes_paid_deal=True,
            reduces_delivery_time=reduces_delivery_time,
            raises_retention_or_proof=raises_retention_or_proof,
            violates_hard_gate=False,
            reason_ar="موافقة فورية — يربط بصفقة مدفوعة",
            reason_en="Approved — tied to a paid deal",
            rationale_tags=("closes_paid_deal",),
        )

    # Step 3: standard gate (≥3 customers OR delivery-time / retention)
    customer_count = len(set(customer_handles_who_asked))
    has_revenue_tie = reduces_delivery_time or raises_retention_or_proof
    if customer_count >= 3:
        return TriageDecision(
            status="BUILD_QUEUE",
            customer_count=customer_count,
            closes_paid_deal=False,
            reduces_delivery_time=reduces_delivery_time,
            raises_retention_or_proof=raises_retention_or_proof,
            violates_hard_gate=False,
            reason_ar=f"موافقة — طلب {customer_count} عملاء",
            reason_en=f"Approved — {customer_count} customers asked",
            rationale_tags=("3plus_customers",),
        )
    if has_revenue_tie:
        return TriageDecision(
            status="BUILD_QUEUE",
            customer_count=customer_count,
            closes_paid_deal=False,
            reduces_delivery_time=reduces_delivery_time,
            raises_retention_or_proof=raises_retention_or_proof,
            violates_hard_gate=False,
            reason_ar="موافقة — يقلّل وقت التسليم أو يرفع الاحتفاظ/الإثبات",
            reason_en="Approved — reduces delivery time or raises retention/proof",
            rationale_tags=("revenue_tie",),
        )

    # Step 4: default → defer
    if customer_count == 0:
        return TriageDecision(
            status="DEFER_INSUFFICIENT",
            customer_count=0,
            closes_paid_deal=False,
            reduces_delivery_time=reduces_delivery_time,
            raises_retention_or_proof=raises_retention_or_proof,
            violates_hard_gate=False,
            reason_ar="مؤجَّل — لا يوجد عميل طلبه",
            reason_en="Deferred — no customer asked for it yet",
            rationale_tags=("zero_customer_demand",),
        )
    return TriageDecision(
        status="DEFER_INSUFFICIENT",
        customer_count=customer_count,
        closes_paid_deal=False,
        reduces_delivery_time=reduces_delivery_time,
        raises_retention_or_proof=raises_retention_or_proof,
        violates_hard_gate=False,
        reason_ar=f"مؤجَّل — طلبه {customer_count} عميل فقط (يحتاج ≥3)",
        reason_en=f"Deferred — only {customer_count} customer(s) asked (need ≥3)",
        rationale_tags=("under_3_customers",),
    )
