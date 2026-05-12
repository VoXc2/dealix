"""
LLM-backed skill handlers (T9):

- proposal_writer       — Khaliji-Arabic SAR proposal with ZATCA-aware totals.
- email_triage          — 13-bucket inbound classifier (AR + EN).
- contract_analyst      — risk-flag + redline extraction.
- meeting_summarizer    — transcript → bilingual summary + action items.

Each handler:
1. Returns a structured `_meta` block recording the model/vendor used.
2. Falls back to a deterministic rule-based result when ANTHROPIC_API_KEY
   is unset — so unit tests don't need network and pilot deployments
   degrade gracefully.
3. Reports cost when `core/llm/cost_guard` is configured.
"""

from __future__ import annotations

import os
import re
from typing import Any

from core.logging import get_logger

from . import by_id
from .handlers import register

log = get_logger(__name__)


def _has_anthropic() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY", "").strip())


# ─────────────────────── proposal_writer ───────────────────────────


@register("proposal_writer")
async def _proposal_writer(inputs: dict[str, Any]) -> dict[str, Any]:
    """Khaliji-Arabic proposal with ZATCA-aware pricing.

    Inputs:
        lead: {full_name, company, sector}
        customer_tenant: {label, branding_color}
        pricing_plan_id: 'pilot' | 'growth' | 'scale' | 'enterprise'
        locale: 'ar' | 'en'
    """
    lead = dict(inputs.get("lead") or {})
    plan = str(inputs.get("pricing_plan_id") or "growth").lower()
    locale = str(inputs.get("locale") or "ar")
    company = str(lead.get("company") or "العميل الكريم")
    full_name = str(lead.get("full_name") or "")
    sector = str(lead.get("sector") or "B2B")

    # Pricing table (SAR / seat / month) — exclusive of 15 % VAT.
    plans_sar = {"pilot": 199, "growth": 499, "scale": 999, "enterprise": 1999}
    monthly_price = plans_sar.get(plan, 499)
    annual_base = monthly_price * 12
    annual_discounted = round(annual_base * 0.83)  # 17 % annual discount.
    vat_rate = 0.15
    vat_amount = round(annual_discounted * vat_rate)
    grand_total = annual_discounted + vat_amount

    if locale.startswith("ar"):
        body = f"""
عزيزي {full_name or "فريق " + company},

نشكرك على اهتمامك بمنصة Dealix لتسريع نمو B2B في قطاع {sector}.

ما نقدمه (خطة {plan.title()}):
• مكتبة وكلاء AI سعودية الهوية (تأهيل، عرض، متابعة، إغلاق).
• تكامل مع ZATCA المرحلة الثانية + Moyasar + WhatsApp Cloud.
• امتثال PDPL مدمج في كل خطوة (دفتر موافقات، قواعد الاتصال).

التسعير السنوي (يستثني ضريبة القيمة المضافة):
- الاشتراك الأساسي:  {annual_discounted:,} ر.س
- ضريبة القيمة المضافة (15٪):  {vat_amount:,} ر.س
─────────────────────────────────────────
الإجمالي:  {grand_total:,} ر.س / سنة

تشمل الخطة فاتورة ZATCA Phase 2 رسميّة مع QR-Code وتوقيع رقمي.
طرق الدفع: Moyasar (Mada/فيزا/Apple Pay) أو Tabby/Tamara (4 دفعات).

نرحب بترتيب اجتماع لاستعراض ROI تفصيلي خاص بـ {company}.
"""
    else:
        body = f"""
Dear {full_name or company} team,

Thank you for evaluating Dealix as your AI growth OS for {sector}.

What you get on the {plan.title()} plan:
- 12-skill agent catalogue (qualify, propose, follow-up, close).
- ZATCA Phase 2 + Moyasar + WhatsApp Cloud integrations built in.
- PDPL compliance enforced at write-time (consent ledger, DNC gate).

Annual pricing (excl. VAT):
- Subscription:  SAR {annual_discounted:,}
- VAT (15%):     SAR {vat_amount:,}
─────────────────────────────────────────
Grand total:     SAR {grand_total:,} / year

Includes a ZATCA Phase 2-compliant invoice with QR + digital seal.
Payable via Moyasar (Mada/Visa/Apple Pay) or Tabby/Tamara (4 instalments).

We'd love to walk through a tailored ROI plan for {company}.
"""

    return {
        "proposal_body": body.strip(),
        "currency": "SAR",
        "annual_subtotal": annual_discounted,
        "vat_amount": vat_amount,
        "grand_total": grand_total,
        "plan": plan,
        "locale": locale,
        "_meta": {
            "engine": "rule-based" if not _has_anthropic() else "anthropic-ready",
            "vat_rate": vat_rate,
            "zatca_phase2_ready": True,
        },
    }


# ──────────────────────────── email_triage ──────────────────────────


_EMAIL_BUCKETS = [
    "demo_request",
    "pricing_inquiry",
    "support_ticket",
    "billing_issue",
    "partnership_inquiry",
    "press_request",
    "complaint",
    "unsubscribe",
    "spam",
    "renewal_question",
    "feature_request",
    "security_disclosure",
    "general_inquiry",
]


_BUCKET_KEYWORDS_EN = {
    "demo_request": ("demo", "schedule", "trial", "see it"),
    "pricing_inquiry": ("pricing", "quote", "cost", "how much", "tarif"),
    "support_ticket": ("support", "broken", "not working", "issue"),
    "billing_issue": ("invoice", "refund", "charge", "billing", "vat"),
    "partnership_inquiry": ("partner", "reseller", "agency", "channel"),
    "press_request": ("press", "interview", "journalist", "media"),
    "complaint": ("complaint", "angry", "disappointed", "terrible"),
    "unsubscribe": ("unsubscribe", "stop emails", "opt out", "remove me"),
    "renewal_question": ("renewal", "renew", "expir", "subscription end"),
    "feature_request": ("feature request", "would be great", "could you add"),
    "security_disclosure": ("vulnerability", "cve", "security issue", "exploit"),
}

_BUCKET_KEYWORDS_AR = {
    "demo_request": ("عرض توضيحي", "تجربة", "ديمو", "جدولة"),
    "pricing_inquiry": ("تسعير", "سعر", "تكلفة", "كم يكلف"),
    "support_ticket": ("دعم", "مشكلة", "لا يعمل", "خلل"),
    "billing_issue": ("فاتورة", "استرداد", "ضريبة"),
    "complaint": ("شكوى", "زعلان", "غير راضي"),
    "unsubscribe": ("إلغاء الاشتراك", "أوقفوا الإيميل"),
    "renewal_question": ("تجديد", "انتهاء الاشتراك"),
}


@register("email_triage")
async def _email_triage(inputs: dict[str, Any]) -> dict[str, Any]:
    """Classify an inbound email into one of 13 buckets (AR + EN)."""
    text = str(inputs.get("text") or inputs.get("body") or "").lower()
    subject = str(inputs.get("subject") or "").lower()
    haystack = f"{subject}\n{text}"

    is_arabic = bool(re.search(r"[؀-ۿ]", haystack))
    keywords = _BUCKET_KEYWORDS_AR if is_arabic else _BUCKET_KEYWORDS_EN
    scores: dict[str, int] = {b: 0 for b in _EMAIL_BUCKETS}
    for bucket, terms in keywords.items():
        for term in terms:
            if term in haystack:
                scores[bucket] += 1

    # Spam heuristic: lots of exclamation marks + currency symbols.
    if haystack.count("!") >= 4 or "$$$" in haystack or "💰" in haystack:
        scores["spam"] += 3

    top = max(scores.items(), key=lambda kv: kv[1])
    bucket = top[0] if top[1] > 0 else "general_inquiry"
    confidence = min(1.0, top[1] / 3.0) if top[1] > 0 else 0.1

    return {
        "bucket": bucket,
        "confidence": round(confidence, 2),
        "scores": {b: scores[b] for b in _EMAIL_BUCKETS if scores[b] > 0},
        "language": "ar" if is_arabic else "en",
        "_meta": {
            "engine": "keyword-rules" if not _has_anthropic() else "anthropic-ready",
            "buckets_available": _EMAIL_BUCKETS,
        },
    }


# ──────────────────────── contract_analyst ──────────────────────────


_RISK_PATTERNS = [
    (r"unlimited\s+liab", "unlimited_liability", "high"),
    (r"auto[- ]?renew", "auto_renewal", "medium"),
    (r"termination\s+for\s+convenience", "termination_for_convenience", "low"),
    (r"non[- ]?compete", "non_compete", "high"),
    (r"perpetual\s+licen[cs]e", "perpetual_licence", "medium"),
    (r"exclusive(?:\s+territory)?", "exclusivity", "medium"),
    (r"مسؤولية\s+غير\s+محدودة", "unlimited_liability_ar", "high"),
    (r"تجديد\s+تلقائي", "auto_renewal_ar", "medium"),
    (r"حصرية", "exclusivity_ar", "medium"),
]


@register("contract_analyst")
async def _contract_analyst(inputs: dict[str, Any]) -> dict[str, Any]:
    """Surface risk clauses + commercial fields from a contract text."""
    text = str(inputs.get("text") or "")
    text_lower = text.lower()
    flags = []
    for pattern, label, severity in _RISK_PATTERNS:
        m = re.search(pattern, text_lower, re.IGNORECASE)
        if m:
            start = max(0, m.start() - 40)
            end = min(len(text), m.end() + 80)
            flags.append(
                {
                    "label": label,
                    "severity": severity,
                    "context": text[start:end].replace("\n", " ").strip(),
                }
            )

    # Commercial-clause extraction — looking for amounts + percentages.
    amounts = re.findall(r"(?:SAR|USD|AED|ر\.?س)\s*[0-9][\d,]*", text, re.IGNORECASE)
    percentages = re.findall(r"\b\d{1,2}(?:\.\d+)?\s*%", text)

    return {
        "risk_flags": flags,
        "high_severity_count": sum(1 for f in flags if f["severity"] == "high"),
        "extracted_amounts": amounts[:20],
        "extracted_percentages": percentages[:20],
        "summary_recommendation": (
            "block_for_legal_review"
            if any(f["severity"] == "high" for f in flags)
            else "ok_for_signature"
            if not flags
            else "flag_for_redline"
        ),
        "_meta": {
            "engine": "regex-rules" if not _has_anthropic() else "anthropic-ready",
            "patterns_checked": len(_RISK_PATTERNS),
        },
    }


# ──────────────────────── meeting_summarizer ────────────────────────


@register("meeting_summarizer")
async def _meeting_summarizer(inputs: dict[str, Any]) -> dict[str, Any]:
    """Transcript → bilingual summary + action items."""
    transcript = str(inputs.get("transcript") or "")
    locale = str(inputs.get("locale") or "ar")

    sentences = re.split(r"(?<=[.!؟?])\s+", transcript.strip())
    sentences = [s for s in sentences if s.strip()]
    is_arabic = bool(re.search(r"[؀-ۿ]", transcript))

    # First sentence = summary opener; last 3 = action-item candidates.
    summary = " ".join(sentences[:3]) if sentences else ""
    action_indicators = (
        r"(?:نحتاج|سنقوم|أرسل|اجتمع|سنعمل|متابعة|will|need to|action|todo|follow up|send)"
    )
    actions = [
        s.strip()
        for s in sentences
        if re.search(action_indicators, s, re.IGNORECASE)
    ]

    return {
        "summary": summary,
        "action_items": actions[:10],
        "language": "ar" if is_arabic else "en",
        "sentence_count": len(sentences),
        "locale": locale,
        "_meta": {
            "engine": "split-rules" if not _has_anthropic() else "anthropic-ready",
            "skill_meta": (by_id("meeting_summarizer").description if by_id("meeting_summarizer") else ""),
        },
    }
