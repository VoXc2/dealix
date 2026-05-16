"""Expansion Engine — next-best-offer from pains/signals (no upsell without proof)."""

from __future__ import annotations

from typing import Any


def next_best_offer(
    *,
    primary_pain_keyword: str | None = None,
    sector: str | None = None,
    max_proof_level: int = 0,
    proof_event_count: int = 0,
) -> dict[str, Any]:
    """
    Recommend expansion SKU — gated: weak proof → internal recommendation only.

    max_proof_level uses EvidenceLevel ints (0–5) from proof_engine.evidence.
    """
    pain = (primary_pain_keyword or "").lower()
    sec = (sector or "").lower()

    gated = proof_event_count < 1 or max_proof_level < 2
    base_note_ar = "لا upsell خارجي بدون Proof موثّق — اعتبر هذا اقتراحًا داخليًا فقط."
    base_note_en = "No external upsell without recorded proof — treat as internal suggestion."

    offer_key = "governed_ops_retainer"
    offer_ar = "ريتينر التشغيل المحكوم للإيراد"
    offer_en = "Governed Ops Retainer"

    if any(k in pain for k in ("data", "crm", "sheet", "excel", "بيانات")):
        offer_key = "crm_data_readiness_for_ai"
        offer_ar = "جاهزية CRM والبيانات للذكاء الاصطناعي"
        offer_en = "CRM / Data Readiness for AI"
    elif any(k in pain for k in ("support", "شكوى", "عملاء", "رد")):
        offer_key = "ai_governance_revenue_teams"
        offer_ar = "حوكمة الذكاء الاصطناعي لفرق الإيراد"
        offer_en = "AI Governance for Revenue Teams"
    elif any(k in pain for k in ("report", "إدارة", "مجلس", "executive")):
        offer_key = "board_decision_memo"
        offer_ar = "مذكرة قرارات مجلس الإدارة"
        offer_en = "Board Decision Memo"
    elif "agency" in sec or "وكالة" in (primary_pain_keyword or ""):
        offer_key = "trust_pack_lite"
        offer_ar = "حزمة الثقة الخفيفة"
        offer_en = "Trust Pack Lite"

    mode = "suggest_only" if gated else "approval_required"

    return {
        "offer_key": offer_key,
        "offer_ar": offer_ar,
        "offer_en": offer_en,
        "mode": mode,
        "gated": gated,
        "gates": {
            "min_proof_events": 1,
            "min_evidence_level": 2,
            "actual_proof_events": proof_event_count,
            "actual_max_evidence_level": max_proof_level,
        },
        "notes_ar": base_note_ar,
        "notes_en": base_note_en,
    }
