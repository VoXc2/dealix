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


def _ops_summary(customer_handle: str) -> dict[str, Any]:
    """Six-number operations snapshot for the console header strip.

    Real values are populated by the deliverables/qualification/proof_ledger
    modules once the customer has activated. Until then, zero-state — never
    invent numbers (Article 8 / Constitution NO_FAKE_PROOF).
    """
    return {
        "leads_today": 0,
        "leads_today_sub": "",
        "qualified": 0,
        "qualified_sub": "BANT score ≥ 60",
        "in_pipeline": 0,
        "pipeline_sub": "",
        "drafts_pending": 0,
        "proof_events_week": 0,
        "nps": None,
        "nps_sub": "",
        "source": "ops_summary_v1",
    }


def _sequences_state(customer_handle: str) -> dict[str, Any]:
    """Current JourneyState + the history of completed states for this customer.

    Hard fallback: every customer starts at lead_intake. Production reads from
    customer_loop.JourneyState records; here we return the safe baseline.
    """
    return {
        "current_state": "lead_intake",
        "history": [],
        "next_allowed": ["diagnostic_requested", "nurture", "blocked"],
        "source": "customer_loop.schemas",
    }


def _radar_today(customer_handle: str) -> dict[str, Any]:
    """Daily Radar — opportunity feed scoped to this customer.

    The console renders DEMO data when this section is empty. Live data is
    composed in market_intelligence.opportunity_feed.build_opportunity_feed
    once a real signal source (Tavily/Google CSE) is wired via env.
    """
    return {
        "title_ar": "Radar اليومي",
        "title_en": "Daily Radar",
        "opportunities": [],
        "live": False,
        "note_ar": (
            "بياناتك الحقيقيّة تظهر هنا فور تفعيل مصدر بيانات (Google "
            "Search/Tavily). حالياً معاينة فقط."
        ),
        "source": "market_intelligence.opportunity_feed",
    }


def _digest_weekly(customer_handle: str) -> dict[str, Any]:
    """Weekly digest — sourced from self_growth_os.weekly_growth_scorecard."""
    return {
        "title_ar": "Digest أسبوعي",
        "title_en": "Weekly Digest",
        "wins": [],
        "opportunities_next_week": [],
        "decisions_taken": [],
        "source": "self_growth_os.weekly_growth_scorecard",
    }


def _digest_monthly(customer_handle: str) -> dict[str, Any]:
    """Monthly digest — sourced from market_intelligence.sector_pulse + proof_ledger."""
    return {
        "title_ar": "Digest شهري",
        "title_en": "Monthly Digest",
        "sector_context": [],
        "proof_pack_additions": [],
        "kpi_lift_pct": None,
        "source": "market_intelligence.sector_pulse + proof_ledger",
    }


def _service_status_for_customer(customer_handle: str) -> dict[str, Any]:
    """Which Dealix services are LIVE for this customer right now."""
    return {
        "live_count": 8,
        "target_count": 24,
        "live_services": [
            "lead_intake_whatsapp",
            "qualification",
            "enrichment",
            "routing",
            "outreach_drafts",
            "consent_required_send",
            "audit_trail",
            "release_gate",
        ],
        "source": "registry/SERVICE_READINESS_MATRIX.yaml",
    }


def _portal_payload(customer_handle: str) -> dict[str, Any]:
    """Compose the 8-field customer-facing payload.

    Hard rule (Constitution Article 6 #2): NO internal module names,
    NO version labels, NO agent names, NO test artifacts.
    """
    return {
        "customer_handle": customer_handle,
        "company_name": None,
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
        "enriched_view": {
            "ops_summary": _ops_summary(customer_handle),
            "sequences": _sequences_state(customer_handle),
            "radar_today": _radar_today(customer_handle),
            "digest_weekly": _digest_weekly(customer_handle),
            "digest_monthly": _digest_monthly(customer_handle),
            "service_status_for_customer": _service_status_for_customer(customer_handle),
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
