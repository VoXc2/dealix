"""Match offer template to sector / bottleneck (no revenue guarantees)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.company_growth_beast.schemas import OfferRecommendation


def match_offer(profile: dict[str, Any], diagnostic: dict[str, Any] | None) -> dict[str, Any]:
    sector_raw = str(profile.get("sector") or "")
    sector = sector_raw.lower()
    bottleneck = (diagnostic or {}).get("growth_bottleneck") or "lead_flow"

    if "agency" in sector or "وكالة" in sector_raw or "تسويق" in sector_raw:
        name_ar, name_en = "سبrint إثبات لعملاء الوكالة", "Client Proof Sprint"
        headline_ar = "ننظم أدلة التسليم والتقارير للعملاء خلال أسبوع"
    elif "saas" in sector:
        name_ar, name_en = "سبrint الدعم إلى النمو", "Support-to-Growth Sprint"
        headline_ar = "من أسئلة الدعم إلى فجوات معرفة ومحتوى مسودة"
    elif "consult" in sector or "استشارة" in sector or "تدريب" in sector:
        name_ar, name_en = "سبrint العرض والتسجيل", "Offer & Enrollment Sprint"
        headline_ar = "توضيح العرض ومسارات المتابعة اليدوية الآمنة"
    else:
        name_ar, name_en = "سبrint المتابعة B2B", "B2B Follow-up Sprint"
        headline_ar = "ترتيب المتابعة والاعتراضات بدون قنوات عالية المخاطر"

    plan = [
        "يوم 1: تأكيد ICP والقطاع",
        "يوم 2: صياغة العرض وحدود الوعد",
        "يوم 3: بنك رسائل ومتابعات (مسودة)",
        "يوم 4: حزمة محتوى inbound (مسودة)",
        "يوم 5: مسارات دافئة مقترحة",
        "يوم 6: أحداث proof قابلة للتسجيل",
        "يوم 7: مراجعة تنفيذية وقرار التجربة التالية",
    ]

    rec = OfferRecommendation(
        offer_name_ar=name_ar,
        offer_name_en=name_en,
        target_segment=str(bottleneck),
        headline_ar=headline_ar,
        headline_en=f"Sprint focused on {bottleneck}; drafts only; approval before any send.",
        promise="وضوح تشغيلي ومسودات قابلة للتنفيذ بعد موافقتك",
        non_promise="لا نضمن مبيعات أو عدد leads; لا إرسال تلقائي; لا واتساب بارد",
        seven_day_plan=plan,
        proof_metric="عدد أحداث proof المسجلة بعد التسليم المعتمد",
        blocked_claims=["ضمان إيراد", "نتائج مؤكدة 100%", "cold WhatsApp", "auto publish"],
        approval_required=True,
    )
    return {"schema_version": 1, "offer": rec.model_dump(), "action_mode": "draft_only"}
