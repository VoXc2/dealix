"""V12.5.1 — Customer Company Portal.

Per Constitution Article 6 #2: customer-facing endpoint that returns
ONLY 8 customer-facing fields. NO internal module names, NO version
labels (V11/V12/V12.5), NO agent names, NO test artifacts.

The customer cares about the result, not the engineering.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import Field

router = APIRouter(prefix="/api/v1/customer-portal", tags=["customer-portal"])


# Outputs are deliberately minimal — 8 fields per Constitution.
# Customer-facing copy ONLY. No internal terminology.


def _start_diagnostic_link(customer_handle: str) -> dict[str, str]:
    return {
        "title_ar": "ابدأ التشخيص",
        "title_en": "Start Diagnostic",
        "description_ar": "أجب على 6 أسئلة وتسلّم تقرير صفحة واحدة خلال 24-48 ساعة.",
        "description_en": "Answer 6 questions; receive a 1-page diagnostic in 24-48 hours.",
        "next_step": "submit_intake",
    }


def _seven_day_plan(customer_handle: str) -> dict[str, Any]:
    return {
        "title_ar": "خطة 7 أيام",
        "title_en": "7-Day Plan",
        "days": [
            {"day": 1, "ar": "تحليل الفرص", "en": "Opportunities ranked"},
            {"day": 2, "ar": "صياغة الرسائل", "en": "Messages drafted"},
            {"day": 3, "ar": "إرسال يدوي معتمد", "en": "Approved manual sends"},
            {"day": 4, "ar": "خطة المتابعة", "en": "Follow-up calendar"},
            {"day": 5, "ar": "مذكّرة المخاطر", "en": "Risk note"},
            {"day": 6, "ar": "Proof Pack مبدئي", "en": "Initial Proof Pack"},
            {"day": 7, "ar": "مكالمة مراجعة", "en": "Review call"},
        ],
        "status": "available_after_diagnostic",
    }


def _messages_and_followups(customer_handle: str) -> dict[str, Any]:
    return {
        "title_ar": "رسائل ومتابعات",
        "title_en": "Messages & Follow-ups",
        "approved_drafts_count": 0,
        "pending_approval_count": 0,
        "note_ar": "كل رسالة تمر بموافقتك قبل الإرسال اليدوي.",
        "note_en": "Every message passes your approval before manual send.",
    }


def _support_tickets(customer_handle: str) -> dict[str, Any]:
    return {
        "title_ar": "تذاكر الدعم",
        "title_en": "Support Tickets",
        "open_count": 0,
        "p0_critical_count": 0,
        "note_ar": "لا تذاكر مفتوحة حالياً.",
        "note_en": "No open tickets at the moment.",
    }


def _deliverables(customer_handle: str) -> dict[str, Any]:
    return {
        "title_ar": "التسليمات",
        "title_en": "Deliverables",
        "ready": [],
        "in_progress": [],
        "waiting_for_inputs": [],
        "note_ar": "ستظهر التسليمات هنا فور بدء جلسة التسليم.",
        "note_en": "Deliverables appear here once a delivery session starts.",
    }


def _proof_pack(customer_handle: str) -> dict[str, Any]:
    return {
        "title_ar": "Proof Pack",
        "title_en": "Proof Pack",
        "events_count": 0,
        "audience": "internal_only",
        "approval_status": "approval_required",
        "note_ar": "يُحرَّر بعد اكتمال أوّل تجربة. لا أرقام مخترعة.",
        "note_en": "Generated after the first completed engagement. No invented numbers.",
    }


def _weekly_report(customer_handle: str) -> dict[str, Any]:
    return {
        "title_ar": "التقرير الأسبوعي",
        "title_en": "Weekly Report",
        "current_week": None,
        "note_ar": "يُسلَّم كل يوم اثنين بعد بداية التجربة.",
        "note_en": "Delivered every Monday after engagement starts.",
    }


def _next_decision(customer_handle: str) -> dict[str, str]:
    return {
        "title_ar": "القرار التالي",
        "title_en": "Next Decision",
        "action_ar": "ابدأ بتقديم بيانات التشخيص — 6 أسئلة فقط.",
        "action_en": "Start by submitting diagnostic intake — 6 questions only.",
    }


def _portal_payload(customer_handle: str) -> dict[str, Any]:
    """Compose the 8-field customer-facing payload.

    Hard rule (Constitution Article 6 #2): NO internal module names,
    NO version labels, NO agent names, NO test artifacts.
    """
    return {
        "customer_handle": customer_handle,
        "language_default": "ar",
        "sections": {
            "1_start_diagnostic": _start_diagnostic_link(customer_handle),
            "2_seven_day_plan": _seven_day_plan(customer_handle),
            "3_messages_and_followups": _messages_and_followups(customer_handle),
            "4_support_tickets": _support_tickets(customer_handle),
            "5_deliverables": _deliverables(customer_handle),
            "6_proof_pack": _proof_pack(customer_handle),
            "7_weekly_report": _weekly_report(customer_handle),
            "8_next_decision": _next_decision(customer_handle),
        },
        "promise_ar": (
            "كل خطوة بموافقتك. لا إرسال آلي. لا خصم آلي. لا ادّعاءات "
            "مضمونة. لا بيانات شخصيّة في السجلات."
        ),
        "promise_en": (
            "Every step with your approval. No automated sends. No "
            "automated charges. No guaranteed claims. No personal "
            "data in logs."
        ),
    }


@router.get("/{customer_handle}")
async def customer_portal(customer_handle: str) -> dict[str, Any]:
    """Customer-facing portal. 8 sections. No internal references.

    Read-only. 200 always. The customer sees outcomes, not engineering.
    """
    return _portal_payload(customer_handle or "Slot-A")


@router.get("/")
async def customer_portal_root() -> dict[str, Any]:
    """Default — placeholder Slot-A view (no real customer required)."""
    return _portal_payload("Slot-A")
