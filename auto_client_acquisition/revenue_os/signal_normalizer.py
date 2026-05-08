"""
Normalize MarketSignal → Tier-1 output (Why Now, Pain, Offer, Risk, Action, Proof).

Uses caller-supplied signals only — aligns with growth_beast.market_radar (no HTTP).
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.growth_beast.market_radar import MarketSignal, evaluate_signals

# Arabic-first UX strings; English secondary in *_en fields.
_SIGNAL_PLAYBOOK: dict[str, dict[str, str]] = {
    "hiring_sales_team": {
        "business_pain_ar": "ضغط على خط أنابيب المبيعات وتوسعة يدوية غير منظمة",
        "business_pain_en": "Pipeline strain / unstructured outbound scaling.",
        "best_offer_ar": "جلسة تشخيص مصغّر + ترتيب أولى الفرص",
        "best_offer_en": "Mini diagnostic + ranked opportunities.",
        "risk_ar": "قنوات باردة أو بيانات من جهات غير موافقة ترفع المخاطر",
        "risk_en": "Cold channels or non-consented data raises compliance risk.",
    },
    "expanding_support": {
        "business_pain_ar": "ازدياد الحجم بدون نظام متابعة وخدمة عملاء",
        "business_pain_en": "Volume growth without follow-up / CS systems.",
        "best_offer_ar": "Support OS خفيف + خطة متابعة",
        "best_offer_en": "Light Support OS + follow-up plan.",
        "risk_ar": "تعهدات SLA بدون قياس قد تضر الثقة",
        "risk_en": "SLA promises without measurement hurt trust.",
    },
    "launching_product": {
        "business_pain_ar": "إطلاق جديد يحتاج توافق رسائل وجلب فرص بسرعة",
        "business_pain_en": "Launch needs messaging coherence + fast opportunity intake.",
        "best_offer_ar": "7-Day Revenue Proof Sprint",
        "best_offer_en": "7-Day Revenue Proof Sprint.",
        "risk_ar": "محتوى وعود خارجية قبل الموافقة",
        "risk_en": "External promises before approvals.",
    },
    "raised_funding": {
        "business_pain_ar": "تسريع النمو مع ضغط على الكفاءة والامتثال",
        "business_pain_en": "Growth acceleration + efficiency/compliance pressure.",
        "best_offer_ar": "تشغيل نمو إداري + قياس أسبوعي",
        "best_offer_en": "Managed growth ops + weekly measurement.",
        "risk_ar": "توسعة عشوائية بالأدوات",
        "risk_en": "Random tool sprawl.",
    },
    "support_complaints": {
        "business_pain_ar": "شكاوى متكررة أو تجربة عميل ضعيفة",
        "business_pain_en": "Repeated complaints / weak CX.",
        "best_offer_ar": "Support OS + خريطة اعتراضات",
        "best_offer_en": "Support OS + objection map.",
        "risk_ar": "ردود آلية خارجية بدون موافقة",
        "risk_en": "Auto external replies without approval.",
    },
    "weak_followup": {
        "business_pain_ar": "متابعة ضعيفة وفرص ضائعة",
        "business_pain_en": "Weak follow-up / leaked pipeline.",
        "best_offer_ar": "مخطط رسائل (مسودات) + تسلسل متابعة",
        "best_offer_en": "Draft sequence + follow-up plan.",
        "risk_ar": "سبام أو قنوات باردة",
        "risk_en": "Spam or cold channels.",
    },
    "no_proof_visible": {
        "business_pain_ar": "لا يوجد إثبات قيمة ظاهر للقرار",
        "business_pain_en": "No visible proof for buyers.",
        "best_offer_ar": "Proof Pack داخلي ثم موافقة عميل",
        "best_offer_en": "Internal proof pack → customer consent.",
        "risk_ar": "نشر proof بدون موافقة",
        "risk_en": "Publishing proof without consent.",
    },
    "needs_growth_clarity": {
        "business_pain_ar": "ضبابية في الأولويات والعرض",
        "business_pain_en": "Unclear priorities / offer.",
        "best_offer_ar": "Executive Radar + Decision Passport",
        "best_offer_en": "Executive radar + Decision Passport.",
        "risk_ar": "توسعة نطاق بدون قرار",
        "risk_en": "Scope creep without decisions.",
    },
    "asking_about_dealix": {
        "business_pain_ar": "اهتمام مباشر يحتاج تأهيل سريع",
        "business_pain_en": "Direct interest — fast qualification.",
        "best_offer_ar": "Mini Diagnostic",
        "best_offer_en": "Mini Diagnostic.",
        "risk_ar": "منخفض إذا كانت قناة دافئة",
        "risk_en": "Low if inbound/warm.",
    },
    "other": {
        "business_pain_ar": "إشارة عامة — يحتاج تمييز يدوي",
        "business_pain_en": "Generic signal — needs manual refinement.",
        "best_offer_ar": "Mini Diagnostic",
        "best_offer_en": "Mini Diagnostic.",
        "risk_ar": "مصادر غير موثقة",
        "risk_en": "Unverified sources.",
    },
}


def _why_now_from_signal(s: MarketSignal) -> tuple[str, str]:
    if s.why_now.strip():
        return s.why_now, s.why_now
    pb = _SIGNAL_PLAYBOOK.get(s.signal_type, _SIGNAL_PLAYBOOK["other"])
    ar = f"إشارة: {s.signal_type} — {pb['business_pain_ar']}"
    en = f"Signal: {s.signal_type} — {pb['business_pain_en']}"
    return ar, en


def normalize_market_signal(signal: MarketSignal) -> dict[str, Any]:
    """Single signal → golden-chain-aligned bundle."""
    pb = _SIGNAL_PLAYBOOK.get(signal.signal_type, _SIGNAL_PLAYBOOK["other"])
    why_ar, why_en = _why_now_from_signal(signal)

    recommended_action = "prepare_mini_diagnostic"
    proof_target = "demo_booked"
    if signal.signal_type in ("weak_followup", "support_complaints"):
        proof_target = "reply_rate_lift_internal"
    if signal.signal_type == "no_proof_visible":
        proof_target = "proof_pack_internal"
        recommended_action = "assemble_proof_pack_draft"

    blocked_actions = ["cold_whatsapp", "linkedin_automation", "scraping", "purchased_list_bulk"]

    return {
        "signal_type": signal.signal_type,
        "source_type": signal.source_type,
        "sector_hint": signal.sector_hint,
        "why_now_ar": why_ar,
        "why_now_en": why_en,
        "business_pain_ar": pb["business_pain_ar"],
        "business_pain_en": pb["business_pain_en"],
        "best_offer_ar": pb["best_offer_ar"],
        "best_offer_en": pb["best_offer_en"],
        "risk_ar": pb["risk_ar"],
        "risk_en": pb["risk_en"],
        "recommended_action": recommended_action,
        "blocked_actions": blocked_actions,
        "proof_target": proof_target,
        "confidence": signal.confidence,
        "action_mode": "suggest_only",
        "signal_text_redacted": signal.signal_text_redacted,
        "contains_personal_data": signal.contains_personal_data,
        "risk_flags": signal.risk_flags,
    }


def normalize_signals_batch(signals: list[MarketSignal]) -> dict[str, Any]:
    """Batch normalize + rollup counts (evaluate_signals)."""
    normalized = [normalize_market_signal(s) for s in signals]
    rollup = evaluate_signals(signals)
    return {"signals": normalized, "rollup": rollup}
