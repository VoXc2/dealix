"""V12 Support OS — escalation decisions.

Mandatory-escalation categories per V12 plan:
- payment_issue / refund / privacy_pdpl
- angry_customer / security_incident
- data_deletion / system_outage
- customer_asks_for_guarantee
- customer_asks_for_cold_whatsapp
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from auto_client_acquisition.support_os.classifier import (
    ClassificationResult,
    SupportCategory,
)


_MANDATORY_ESCALATE: set[SupportCategory] = {
    "refund",
    "payment",
    "privacy_pdpl",
    "angry_customer",
}


# Phrases that ALWAYS escalate, regardless of classified category.
_ESCALATE_PATTERNS: tuple[str, ...] = (
    # English
    r"\b(guarantee|guaranteed)\b",
    r"\b(cold\s+whats?app|cold\s+email|cold\s+outreach|cold\s+dm)\b",
    r"\b(scrape|scraping|purchase\s+list|buy\s+leads)\b",
    r"\b(security\s+(incident|breach)|leak)\b",
    r"\b(outage|down|server\s+down)\b",
    r"\b(legal|lawyer|sue\s+you)\b",
    # Arabic
    r"نضمن|اضمنوا\s+لي|تضمنون",
    r"واتساب\s+بارد|إيميل\s+بارد",
    r"اخترق|تسريب|اختراق\s+أمني",
    r"محامي|أرفع\s+قضيّة|دعوى\s+قضائيّة",
)


@dataclass
class EscalationDecision:
    should_escalate: bool
    reason_ar: str
    reason_en: str
    category: SupportCategory
    matched_phrases: list[str]


def should_escalate(
    *, classification: ClassificationResult, message: str = ""
) -> EscalationDecision:
    matched: list[str] = []
    for pat in _ESCALATE_PATTERNS:
        m = re.search(pat, message, flags=re.IGNORECASE)
        if m:
            matched.append(m.group(0))

    if classification.category in _MANDATORY_ESCALATE:
        reason_en = (
            f"Mandatory escalation: category '{classification.category}' "
            "requires human review per V12 policy."
        )
        reason_ar = (
            f"تصعيد إجباري: التصنيف '{classification.category}' يتطلّب "
            "مراجعة بشريّة وفق سياسة V12."
        )
        return EscalationDecision(
            should_escalate=True,
            reason_ar=reason_ar,
            reason_en=reason_en,
            category=classification.category,
            matched_phrases=matched,
        )

    if matched:
        return EscalationDecision(
            should_escalate=True,
            reason_ar=(
                "تصعيد إجباري: العبارة تتعلّق بالضمانات/الأمان/الإرسال البارد "
                "أو ما شابه — تتطلّب مراجعة بشريّة."
            ),
            reason_en=(
                "Mandatory escalation: the message references "
                "guarantees/security/cold outreach or similar — human "
                "review required."
            ),
            category=classification.category,
            matched_phrases=matched,
        )

    return EscalationDecision(
        should_escalate=False,
        reason_ar="لا حاجة للتصعيد حسب القواعد الحاليّة.",
        reason_en="No escalation required per current rules.",
        category=classification.category,
        matched_phrases=[],
    )
