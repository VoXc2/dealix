"""Aggregate support themes without exposing PII."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from auto_client_acquisition.company_growth_beast.safety_policy import redact_free_text


def support_questions_to_insights(raw_questions: str) -> dict[str, Any]:
    text = redact_free_text(raw_questions or "", max_len=2000)
    lowered = text.lower()

    themes: list[str] = []
    if any(k in lowered for k in ("refund", "استرداد", "money back")):
        themes.append("refund_policy_clarity")
    if any(k in lowered for k in ("privacy", "pdpl", "خصوصية", "حذف بيانات")):
        themes.append("privacy_and_consent")
    if any(k in lowered for k in ("price", "سعر", "تكلفة", "discount")):
        themes.append("pricing_and_packaging")
    if any(k in lowered for k in ("delay", "تأخير", "sla", "متى")):
        themes.append("delivery_expectations")
    if not themes:
        themes.append("general_operational_questions")

    words = re.findall(r"[\w\u0600-\u06FF]{4,}", text.lower())
    common = [w for w, _ in Counter(words).most_common(5)]

    return {
        "schema_version": 1,
        "action_mode": "suggest_only",
        "themes": themes,
        "kb_gap_candidates_ar": [
            x
            for x in (
                "مقالة توضح سياسة الاسترداد والحدود" if "refund_policy_clarity" in themes else "",
                "مقالة موافقة وبيانات شخصية (PDPL)" if "privacy_and_consent" in themes else "",
                "جدول تسعير واضح مع ما هو خارج النطاق" if "pricing_and_packaging" in themes else "",
                "اتفاقية SLA وتوقعات التسليم" if "delivery_expectations" in themes else "",
            )
            if x
        ],
        "content_ideas_ar": [
            (
                "بوست يشرح كيف تتعامل الشركة مع طلبات الاسترداد بدون جدل"
                if "refund_policy_clarity" in themes
                else "بوست عن أهمية التشخيص قبل العرض"
            )
        ],
        "non_pii_keywords": [k for k in common if "@" not in k],
        "language_primary": "ar",
    }
