"""
Skill execution registry — maps `skills/MANIFEST.yaml` ids to concrete
Python handlers. A skill that has no registered handler responds with
`501 not_implemented`; tenants that need it can BYOA-register their
own.

Each handler is `async def handler(inputs: dict[str, Any]) -> dict[str, Any]`.
The dispatcher passes inputs unchanged after schema validation; the
handler returns a JSON-serialisable dict matching the skill's
`output_shape`.

Handlers are intentionally side-effect-light — they call no external
network APIs unless a key is configured, so unit-testing them is cheap.
"""

from __future__ import annotations

import os
import re
from typing import Any, Awaitable, Callable

from core.logging import get_logger

log = get_logger(__name__)


Handler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]

_REGISTRY: dict[str, Handler] = {}


def register(skill_id: str) -> Callable[[Handler], Handler]:
    def deco(fn: Handler) -> Handler:
        _REGISTRY[skill_id] = fn
        return fn

    return deco


def get_handler(skill_id: str) -> Handler | None:
    return _REGISTRY.get(skill_id)


def registered_ids() -> list[str]:
    return sorted(_REGISTRY)


# ───────────────────────── sales_qualifier ──────────────────────────


@register("sales_qualifier")
async def _sales_qualifier(inputs: dict[str, Any]) -> dict[str, Any]:
    """BANT + Saudi PDPL contactability scorer.

    Inputs (best-effort — missing fields are tolerated):
        lead_snapshot: {budget, authority, need, timeline, sector, phone}
        compliance_signals: {has_pdpl_consent: bool, dnc_listed: bool}
        locale: ar | en
    """
    lead = dict(inputs.get("lead_snapshot") or {})
    compliance = dict(inputs.get("compliance_signals") or {})
    locale = str(inputs.get("locale") or "ar")

    # Heuristic BANT score: 0.25 per filled dimension.
    bant_dims = ["budget", "authority", "need", "timeline"]
    bant_filled = sum(1 for d in bant_dims if lead.get(d))
    bant = round(bant_filled / 4.0, 2)

    pdpl_ok = bool(compliance.get("has_pdpl_consent"))
    dnc = bool(compliance.get("dnc_listed"))
    pdpl_gate = pdpl_ok and not dnc

    # Combined: cap at PDPL gate. If gate fails, max 0.30.
    score = min(bant, 0.30) if not pdpl_gate else bant

    reasoning = (
        f"BANT filled {bant_filled}/4 dimensions; "
        f"PDPL consent={'yes' if pdpl_ok else 'no'}; "
        f"DNC={'yes' if dnc else 'no'}."
    )
    if locale.startswith("ar"):
        reasoning = (
            f"BANT مكتمل {bant_filled}/4. "
            f"موافقة PDPL: {'نعم' if pdpl_ok else 'لا'}. "
            f"قائمة عدم الاتصال: {'نعم' if dnc else 'لا'}."
        )

    return {
        "score": score,
        "gates": {"bant": bant, "pdpl": pdpl_gate},
        "reasoning": reasoning,
        "recommended_action": (
            "qualify_and_book_meeting"
            if score >= 0.75
            else "nurture"
            if score >= 0.40
            else "disqualify"
        ),
    }


# ──────────────────────────── lead_scorer ───────────────────────────


@register("lead_scorer")
async def _lead_scorer(inputs: dict[str, Any]) -> dict[str, Any]:
    """Tunable fit + urgency + intent + sector weighting.

    Inputs:
        lead: {industry, company_size, role, source, signals}
        weights: {fit, urgency, intent, sector}  (sum should ≈ 1.0)
    """
    lead = dict(inputs.get("lead") or {})
    weights = dict(inputs.get("weights") or {})
    w_fit = float(weights.get("fit", 0.30))
    w_urgency = float(weights.get("urgency", 0.25))
    w_intent = float(weights.get("intent", 0.30))
    w_sector = float(weights.get("sector", 0.15))

    # Sub-scores (0..1) — replace with model if Anthropic key configured.
    signals = lead.get("signals") or {}
    fit = 0.0
    if lead.get("company_size") in {"medium", "large", "enterprise"}:
        fit += 0.5
    if lead.get("role", "").lower() in {"vp", "director", "head", "cto", "ceo", "cfo"}:
        fit += 0.5
    fit = min(fit, 1.0)

    urgency = float(signals.get("urgency", 0.5))
    intent = float(signals.get("intent", 0.5))

    sector_boost_map = {
        "real-estate": 1.0,
        "construction": 0.95,
        "financial-services": 0.9,
        "healthcare": 0.85,
        "hospitality": 0.85,
        "education": 0.8,
        "legal": 0.8,
        "food-and-beverage": 0.75,
    }
    sector = sector_boost_map.get(str(lead.get("industry") or "").lower(), 0.6)

    total = (
        w_fit * fit + w_urgency * urgency + w_intent * intent + w_sector * sector
    )
    return {
        "score": round(min(total, 1.0), 3),
        "components": {"fit": fit, "urgency": urgency, "intent": intent, "sector": sector},
        "weights_applied": {
            "fit": w_fit,
            "urgency": w_urgency,
            "intent": w_intent,
            "sector": w_sector,
        },
    }


# ─────────────────────── content_generator_ar ───────────────────────


@register("content_generator_ar")
async def _content_generator_ar(inputs: dict[str, Any]) -> dict[str, Any]:
    """Saudi-tone marketing copy.

    Inputs:
        product_name, hook, audience, length (short|medium|long), tone
    Output:
        copy: str, hashtags: list[str], call_to_action: str
    """
    product = str(inputs.get("product_name") or "Dealix")
    hook = str(inputs.get("hook") or "نمو B2B بدون فوضى.")
    audience = str(inputs.get("audience") or "فرق المبيعات السعوديّة")
    length = str(inputs.get("length") or "medium")
    tone = str(inputs.get("tone") or "professional")

    parts = [f"{hook}", f"موجّه لـ {audience}."]
    if length in {"medium", "long"}:
        parts.append(
            f"{product} يربط لك المراحل: التقاط lead، تأهيله بـ PDPL، "
            "كتابة عرض بالخليجي، متابعة WhatsApp، توقيع، إصدار فاتورة ZATCA."
        )
    if length == "long":
        parts.append(
            "النتيجة عمليّاً: أقصر دورة إغلاق، تكلفة اكتساب أقل، "
            "وامتثال PDPL مدمج بدل العقوبات."
        )
    copy = " ".join(parts)

    cta_by_tone = {
        "professional": "احجز ديمو الآن.",
        "playful": "خلّينا نعطيك الجولة 👀",
        "urgent": "تحدّيك: 14 يوم لإثبات القيمة.",
    }
    return {
        "copy": copy,
        "hashtags": ["#مبيعات_B2B", "#PDPL", "#رؤية2030", f"#{product.lower()}"],
        "call_to_action": cta_by_tone.get(tone, cta_by_tone["professional"]),
        "tone": tone,
        "length": length,
    }


# ───────────────────────── ar_en_translator ─────────────────────────

# A tiny glossary covering the Saudi commercial terms we see most.
_GLOSSARY_AR_EN: dict[str, str] = {
    "عرض سعر": "quotation",
    "فاتورة": "invoice",
    "ضريبة القيمة المضافة": "VAT",
    "سجل تجاري": "commercial registration",
    "موعد": "appointment",
    "اجتماع": "meeting",
    "متابعة": "follow-up",
    "عميل محتمل": "lead",
    "إغلاق صفقة": "deal close",
    "هيئة الزكاة والضريبة والجمارك": "ZATCA",
    "حماية البيانات الشخصية": "PDPL",
}
_GLOSSARY_EN_AR: dict[str, str] = {v: k for k, v in _GLOSSARY_AR_EN.items()}


@register("ar_en_translator")
async def _ar_en_translator(inputs: dict[str, Any]) -> dict[str, Any]:
    """Bidirectional Saudi-commercial-glossary aware translation.

    Inputs:
        text: str
        from: ar | en
        to: ar | en
    """
    text = str(inputs.get("text") or "")
    src = str(inputs.get("from") or "auto").lower()
    dst = str(inputs.get("to") or "en").lower()

    if src == "auto":
        # Crude detection: if any Arabic codepoint present, source is ar.
        src = "ar" if re.search(r"[؀-ۿ]", text) else "en"

    if src == dst:
        return {"translated": text, "from": src, "to": dst, "glossary_hits": []}

    out = text
    hits: list[str] = []
    glossary = _GLOSSARY_AR_EN if src == "ar" else _GLOSSARY_EN_AR
    for src_term, dst_term in glossary.items():
        if src_term in out:
            out = out.replace(src_term, dst_term)
            hits.append(src_term)

    # If no LLM key, return the glossary-substituted text + a note.
    if not os.getenv("ANTHROPIC_API_KEY"):
        return {
            "translated": out,
            "from": src,
            "to": dst,
            "glossary_hits": hits,
            "note": "glossary-only fallback (no LLM key)",
        }

    # Real translation path would call the LLM router here — left as a
    # follow-up so this handler stays import-side-effect-free.
    return {
        "translated": out,
        "from": src,
        "to": dst,
        "glossary_hits": hits,
        "note": "llm-route would run here if router is wired",
    }
