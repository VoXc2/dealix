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

    offer_key = "managed_growth_ops"
    offer_ar = "تشغيل نمو إداري شهرية"
    offer_en = "Managed Growth Ops (monthly)"

    if any(k in pain for k in ("data", "crm", "sheet", "excel", "بيانات")):
        offer_key = "data_to_revenue"
        offer_ar = "حزمة من البيانات إلى الإيرادات"
        offer_en = "Data-to-Revenue Pack"
    elif any(k in pain for k in ("support", "شكوى", "عملاء", "رد")):
        offer_key = "support_os"
        offer_ar = "نظام دعم وتذاكر خفيف"
        offer_en = "Support OS"
    elif any(k in pain for k in ("report", "إدارة", "مجلس", "executive")):
        offer_key = "executive_command_center"
        offer_ar = "غرفة قيادة تنفيذية"
        offer_en = "Executive Command Center"
    elif "agency" in sec or "وكالة" in (primary_pain_keyword or ""):
        offer_key = "agency_partner_os"
        offer_ar = "نظام شركاء الوكالات"
        offer_en = "Agency Partner OS"

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
