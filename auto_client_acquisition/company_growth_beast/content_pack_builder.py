"""Draft-only content pack (Arabic primary)."""

from __future__ import annotations

from typing import Any


def build_content_pack(profile: dict[str, Any], offer: dict[str, Any] | None) -> dict[str, Any]:
    sector = str(profile.get("sector") or "الشركة")
    headline = ""
    if offer and isinstance(offer.get("offer"), dict):
        headline = str(offer["offer"].get("headline_ar") or "")

    return {
        "schema_version": 1,
        "action_mode": "draft_only",
        "linkedin_post_draft_ar": (
            f"نلاحظ أن قطاع {sector} يواجه ضغط إثبات القيمة. "
            f"{headline or 'نعمل على مسودات وخطة أسبوعية — بدون وعود وهمية.'} "
            "#مسودة_للمراجعة"
        ),
        "landing_section_ar": f"عنوان مقترح: {headline or 'تشخيص تشغيلي في 48 ساعة'} — زر: اطلب تشخيصاً (يدوي).",
        "newsletter_draft_ar": "ملخص الأسبوع: ما تعلمناه من الدعم والمبيعات — بدون أرقام إن لم تتوفر أدلة.",
        "diagnostic_cta_ar": "جاوب على 6 أسئلة لتلقي تشخيص صفحة واحدة (مراجعة بشرية).",
        "objection_post_ar": "الاعتراض الشائع: الوقت — الرد: نبدأ بمسودات وموافقات قبل أي إرسال خارجي.",
        "case_study_snippet_ar": "لا snippet علني بدون موافقة عميل — اطلب proof pack أولاً.",
        "approval_required": True,
        "language_primary": "ar",
    }
