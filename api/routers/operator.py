"""
Dealix Operator router — AI service consultant (chat surface).

Two endpoints back the landing/operator.html chat:

    POST /api/v1/operator/chat/message
        body: {"text": "...", "intent_hint?": "..."}
        Returns the recommended bundle + Arabic explanation + safety note.
        Pure deterministic intent classifier — no LLM call.

    POST /api/v1/operator/service/start
        body: {"bundle_id": "growth_starter", "company_name": "...", ...}
        Records a Diagnostic / Pilot intent; emits a public.demo-request-style
        record (re-uses existing pipeline). Always approval-first; never sends
        outbound on its own.
"""

from __future__ import annotations

import logging
import re
import uuid
from typing import Any

from fastapi import APIRouter, Body, HTTPException

from api.routers.services import CATALOG

log = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/operator", tags=["operator"])


# ── Intent → Bundle mapping ───────────────────────────────────────


# Each intent maps to:
#   bundle_id (or "BLOCKED" for unsafe asks)
#   reason_ar shown to the user
#   recommended_path (link)
INTENT_MAP: dict[str, dict[str, str]] = {
    "want_more_customers": {
        "bundle_id": "growth_starter",
        "reason_ar": (
            "أنسب لك Growth Starter — 10 فرص + رسائل عربية + Proof Pack بـ 499 ريال "
            "خلال 7 أيام."
        ),
        "path": "private-beta.html",
    },
    "has_list": {
        "bundle_id": "data_to_revenue",
        "reason_ar": (
            "أنسب لك Data to Revenue — تنظيف القائمة، فحص contactability، "
            "Top 50 targets + drafts عربية."
        ),
        "path": "services.html",
    },
    "want_partnerships": {
        "bundle_id": "partnership_growth",
        "reason_ar": (
            "أنسب لك Partnership Growth — partner shortlist + co-branded "
            "Proof Pack + revenue share tracker."
        ),
        "path": "agency-partner.html",
    },
    "want_daily_growth": {
        "bundle_id": "executive_growth_os",
        "reason_ar": (
            "أنسب لك Executive Growth OS — كروت قرارات يومية + approval queue + "
            "Proof Pack أسبوعي بـ 2,999 ريال/شهر."
        ),
        "path": "growth-os.html",
    },
    "agency_client": {
        "bundle_id": "partnership_growth",
        "reason_ar": "ابدأ Agency Partner Pilot على عميل واحد. نُسلّم Co-branded Proof Pack.",
        "path": "agency-partner.html",
    },
    "cold_whatsapp_request": {  # BLOCKED — refused intent (forbidden / disallowed)
        "bundle_id": "BLOCKED",
        "reason_ar": (
            "لا أقدر أساعدك في cold WhatsApp — يخالف PDPL وWhatsApp policies. "
            "البديل الآمن: Email + LinkedIn manual، أو احصل على opt-in واضح أولاً."
        ),
        "path": "trust-center.html",
    },
    "scraping_request": {  # BLOCKED — refused intent (forbidden / disallowed)
        "bundle_id": "BLOCKED",
        "reason_ar": (
            "لا نسحب البيانات من LinkedIn أو غيره — يخالف ToS. البديل الآمن: "
            "LinkedIn Lead Gen Forms، Google Maps API، أو enrichment مرخّص."
        ),
        "path": "trust-center.html",
    },
}


# Keyword → intent classifier. First match wins.
_INTENT_KEYWORDS: list[tuple[str, list[str]]] = [
    # Dangerous asks first so they always win over friendly mappings (BLOCKED / forbidden).
    ("cold_whatsapp_request", [  # BLOCKED — forbidden intent
        "واتساب بارد", "cold whatsapp", "cold wa", "بلاست واتساب", "blast whatsapp",
        "إرسال جماعي واتساب", "إرسال جماعي", "mass send", "mass whatsapp",
        "أرقام مشتراة", "قائمة مشتراة", "أرقام شريت", "purchased list",
        "purchased numbers", "list i bought",
        # Phrase patterns: "send WhatsApp to numbers/list (without consent)"
        "أرسل واتساب لأرقام", "ارسل واتساب لأرقام", "أرسل واتساب لقائمة",
        "ارسل واتساب لقائمة", "send whatsapp to numbers", "send whatsapp to list",
    ]),
    ("scraping_request", [  # BLOCKED — forbidden intent
        "scrape", "scraping", "نسحب البيانات", "نسحب بيانات", "auto-dm", "auto dm",
        "أتمتة linkedin", "linkedin automation", "auto connection",
        "نسحب linkedin", "scrape linkedin",
    ]),
    ("agency_client", [
        "وكالة", "agency", "عميلي", "my client", "أعمل لعميل",
    ]),
    ("has_list", [
        "عندي قائمة", "have a list", "csv", "excel", "sheet", "قاعدة بيانات",
    ]),
    ("want_partnerships", [
        "شراكات", "partnerships", "شريك", "partner",
    ]),
    ("want_daily_growth", [
        "تشغيل يومي", "daily", "يومي", "كروت قرارات", "executive", "command center",
        "growth os", "تقرير", "report", "proof pack", "proof", "يثبت", "اثبت",
        "إثبات", "اثبات",
    ]),
    ("want_more_customers", [
        "عملاء جدد", "عملاء", "leads", "زيادة المبيعات", "more customers",
        "ابغى عملاء", "اريد عملاء", "أريد عملاء",
    ]),
]


def classify_intent(text: str, hint: str | None = None) -> str:
    if hint and hint in INTENT_MAP:
        return hint
    if not text:
        return "want_more_customers"  # safe default
    haystack = text.lower()
    for intent, words in _INTENT_KEYWORDS:
        for w in words:
            pattern = r"\b" + re.escape(w.lower()) + r"\b" if all(c.isascii() for c in w) else re.escape(w.lower())
            if re.search(pattern, haystack):
                return intent
    return "want_more_customers"


def _bundle_summary(bundle_id: str) -> dict[str, Any] | None:
    for b in CATALOG:
        if b["id"] == bundle_id:
            return {
                "id": b["id"],
                "name_ar": b["name_ar"],
                "price_label": b["price_label"],
                "for_whom_ar": b["for_whom_ar"],
                "deliverables_ar": list(b["deliverables_ar"]),
                "sla_ar": b["sla_ar"],
                "safe_policy_ar": b["safe_policy_ar"],
                "cta_path": b["cta_path"],
            }
    return None


# ── Endpoints ─────────────────────────────────────────────────────


@router.post("/chat/message")
async def chat_message(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    text = str(body.get("text") or "").strip()
    hint = body.get("intent_hint")
    intent = classify_intent(text, hint=str(hint) if hint else None)
    mapping = INTENT_MAP.get(intent)
    if mapping is None:
        # Defensive — should never happen because all intents are mapped.
        raise HTTPException(status_code=500, detail="intent_unmapped")

    blocked = mapping["bundle_id"] == "BLOCKED"
    bundle = None if blocked else _bundle_summary(mapping["bundle_id"])
    safety_note = (
        mapping["reason_ar"] if blocked
        else "كل outbound يمر بموافقتك. لا cold WhatsApp، لا scraping، لا live charge."
    )

    # Detect low-confidence intent. classify_intent() defaults to
    # "want_more_customers" when nothing matches. If the user's text
    # didn't actually mention any "want_more_customers" keywords, we
    # treat it as ambiguous and ask a clarifying question via LLM.
    low_confidence = False
    clarify_text: str | None = None
    if intent == "want_more_customers" and not blocked and text:
        haystack = text.lower()
        # Was the match an actual want_more_customers keyword, or the default?
        wmc_keywords = next(
            (kws for k, kws in _INTENT_KEYWORDS if k == "want_more_customers"),
            [],
        )
        # ASCII keywords use word-boundary; accept any contains for non-ASCII
        match = any(
            (re.search(r"\b" + re.escape(w.lower()) + r"\b", haystack)
             if all(c.isascii() for c in w) else (w.lower() in haystack))
            for w in wmc_keywords
        )
        if not match:
            # Ambiguous — try LLM clarifying question
            low_confidence = True
            try:
                from auto_client_acquisition.intelligence.smart_drafter import get_drafter
                drafter = get_drafter()
                r = await drafter.clarify_intent(
                    text,
                    fallback="ساعدني أفهم أكثر: تريد عملاء جدد، أم تنظيف قائمة، أم شراكات، أم تشغيل يومي؟",
                )
                clarify_text = r.text
            except Exception as exc:  # noqa: BLE001
                log.info("operator_clarify_llm_unavailable err=%s", exc)
                clarify_text = "ساعدني أفهم أكثر: تريد عملاء جدد، أم تنظيف قائمة، أم شراكات، أم تشغيل يومي؟"

    response: dict[str, Any] = {
        "intent": intent,
        "blocked": blocked,
        "reason_ar": mapping["reason_ar"],
        "recommended_bundle": bundle,
        "safety_note_ar": safety_note,
        "next_path": mapping["path"],
        "approval_first": True,
        "anti_claim_ar": (
            "Dealix يجهّز ويُحضّر — لا يرسل قبل موافقتك." if not blocked else None
        ),
    }
    if low_confidence:
        response["low_confidence"] = True
        response["clarifying_question_ar"] = clarify_text
    return response


@router.post("/service/start")
async def service_start(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    bundle_id = str(body.get("bundle_id") or "").strip()
    if not bundle_id:
        raise HTTPException(status_code=400, detail="bundle_id_required")
    bundle = _bundle_summary(bundle_id)
    if bundle is None:
        raise HTTPException(status_code=404, detail="bundle_not_found")

    # Stub: record the intent (in a future PR this would persist a
    # ServiceSession row + create a kickoff card). Today, return an ack
    # with the next-step plan so the operator UI can confirm.
    session_id = f"svc_{uuid.uuid4().hex[:14]}"
    log.info("operator_service_start session=%s bundle=%s", session_id, bundle_id)
    return {
        "session_id": session_id,
        "bundle": bundle,
        "next_steps_ar": [
            "ستصلك رسالة تأكيد على البريد خلال دقائق.",
            "نطلب منك المدخلات الناقصة (intake) عبر نموذج آمن.",
            "نُجهّز خطة 7 أيام، ونطلب موافقتك قبل أي تواصل خارجي.",
        ],
        "approval_first": True,
    }
