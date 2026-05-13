"""Risk register → default board motion (advisory)."""

from __future__ import annotations

RISK_DECISIONS: dict[str, tuple[str, str]] = {
    "R1": ("Productization Ledger", "فرض سجل منتَجات لتجنب فخ الوكالة."),
    "R2": ("Platform pull signals before SaaS GA", "تأجيل SaaS العام حتى إشارات سحب منصة واضحة."),
    "R3": ("Freeze external actions", "تجميد الإجراءات الخارجية حتى قاعدة + اختبار."),
    "R4": ("Block case study / retainer push", "منع دراسة الحالة/الريتينر حتى عتبة دليل."),
    "R5": ("Delivery playbook before hiring", "Playbook تسليم قبل التوظيف."),
    "R6": ("Partner escalation", "تصعيد شريك + تجميد اتصالات حتى السبب."),
    "R7": ("Multi-provider + cost guardrails", "تعدد مزودين + حدود تكلفة."),
    "R8": ("Reduce tools + autonomy", "تقليل الأدوات ومستوى الاستقلالية."),
    "R9": ("Reject bad revenue", "رفض إيراد سيئ أو تحويله لتشخيص مدفوع."),
    "R10": ("Arabic QA + PDPL evidence", "جودة عربية + حزمة أدلة PDPL."),
}


def list_risk_register() -> list[dict[str, str]]:
    return [
        {
            "id": rid,
            "default_motion_en": motion[0],
            "default_motion_ar": motion[1],
        }
        for rid, motion in sorted(RISK_DECISIONS.items())
    ]
