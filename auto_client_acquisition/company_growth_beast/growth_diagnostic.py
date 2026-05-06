"""One-page growth diagnostic from profile (deterministic)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.company_growth_beast.safety_policy import sector_requires_escalation


def _infer_bottleneck(text: str) -> str:
    low = (text or "").lower()
    if "retention" in low or "تجديد" in text or "churn" in low:
        return "retention"
    if "support" in low or "دعم" in text or "ticket" in low:
        return "support_load"
    if "conversion" in low or "تحويل" in text:
        return "conversion"
    if "proof" in low or "إثبات" in text:
        return "proof_gap"
    return "lead_flow"


def build_growth_diagnostic(profile: dict[str, Any]) -> dict[str, Any]:
    sector = str(profile.get("sector") or "")
    offer = str(profile.get("offer") or "")
    ideal = str(profile.get("ideal_customer") or "")
    channels = str(profile.get("current_channels") or "")
    problems = str(profile.get("common_objections") or "") + " " + str(profile.get("constraints") or "")

    bottleneck = _infer_bottleneck(problems + " " + offer)
    escalation = sector_requires_escalation(sector)

    return {
        "schema_version": 1,
        "growth_bottleneck": bottleneck,
        "best_customer_segment_hint_ar": ideal[:200] or "غير محدد — أضف وصفاً للعميل المثالي.",
        "weakest_funnel_stage": bottleneck,
        "highest_proof_opportunity_ar": "تجميع أدلة التسليم والردود المعتمدة قبل أي ادعاء علني.",
        "best_safe_channel_ar": "مقدمة دافئة أو inbound (صفحة تشخيص) — بدون واتساب بارد.",
        "seven_day_outline_ar": [
            "اليوم 1: توضيح ICP والقطاع",
            "اليوم 2: صقل العرض وما لا نعد به",
            "اليوم 3: زوايا رسائل ومتابعة (مسودة)",
            "اليوم 4: محتوى inbound مسودة",
            "اليوم 5: مسارات دافئة (شريك/عميل حالي)",
            "اليوم 6: خطة proof وأحداث قابلة للقياس",
            "اليوم 7: مراجعة تنفيذية وقرار التجربة القادمة",
        ],
        "first_safe_message_angle_ar": f"تركيز على {offer[:80] or 'قيمة الخدمة'} للعميل المثالي دون وعود رقمية.",
        "do_not_ar": [
            "لا إرسال حي بدون موافقة",
            "لا واتساب بارد",
            "لا ضمان نتائج أو إيراد",
        ],
        "unknowns": [x for x in (["sector_unknown"] if not sector.strip() else []) + (["offer_unknown"] if not offer.strip() else [])],
        "risk_flags": {"sensitive_sector_escalation": escalation},
        "action_mode": "draft_only",
        "language_primary": "ar",
    }
