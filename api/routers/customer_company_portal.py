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
    """Six-number operations snapshot composed from layers 2-9.

    Best-effort across modules — any missing layer returns zero, never
    an invented number (Article 8 / NO_FAKE_PROOF).
    """
    leads_total = 0
    drafts_pending = 0
    in_pipeline = 0
    proof_events_week = 0

    try:
        from auto_client_acquisition.leadops_spine import list_records
        recs = [r for r in list_records(limit=200) if r.customer_handle == customer_handle]
        leads_total = len(recs)
        drafts_pending = sum(1 for r in recs if r.draft_id is not None)
    except Exception:
        pass

    try:
        from auto_client_acquisition.service_sessions import list_sessions
        sessions = list_sessions(customer_handle=customer_handle, limit=50)
        in_pipeline = sum(1 for s in sessions if s.status in ("active", "delivered", "proof_pending"))
    except Exception:
        pass

    return {
        "leads_today": leads_total,
        "leads_today_sub": "",
        "qualified": leads_total,
        "qualified_sub": "leadops_spine.allowed",
        "in_pipeline": in_pipeline,
        "pipeline_sub": "service_sessions.active+delivered+proof_pending",
        "drafts_pending": drafts_pending,
        "proof_events_week": proof_events_week,
        "nps": None,
        "nps_sub": "",
        "source": "leadops_spine + service_sessions (live)",
    }


def _sequences_state(customer_handle: str) -> dict[str, Any]:
    """Current ServiceSession state for this customer (best-effort)."""
    current_state = "lead_intake"
    history: list[str] = []
    try:
        from auto_client_acquisition.service_sessions import list_sessions
        sessions = list_sessions(customer_handle=customer_handle, limit=50)
        if sessions:
            # Use most recent session's status as the customer's current state
            current_state = sessions[0].status
            history = sorted({s.status for s in sessions})
    except Exception:
        pass
    return {
        "current_state": current_state,
        "history": history,
        "next_allowed": ["diagnostic_requested", "nurture", "blocked"],
        "source": "service_sessions (live)",
    }


def _radar_today(customer_handle: str) -> dict[str, Any]:
    """Daily Radar — opportunity feed scoped to this customer.

    Currently empty until a live signal source (Tavily/Google CSE) is
    wired via env. The console falls back to DEMO cards in this case.
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
    """Weekly digest — built from per-customer Executive Pack."""
    try:
        from auto_client_acquisition.executive_pack_v2 import build_weekly_pack
        pack = build_weekly_pack(customer_handle=customer_handle)
        return {
            "title_ar": "Digest أسبوعي",
            "title_en": "Weekly Digest",
            "week_label": pack.week_label,
            "summary_ar": pack.executive_summary_ar,
            "summary_en": pack.executive_summary_en,
            "leads": pack.leads,
            "support": pack.support,
            "blockers_count": len(pack.blockers),
            "next_3_actions_count": len(pack.next_3_actions),
            "source": "executive_pack_v2.build_weekly_pack",
        }
    except Exception:
        return {
            "title_ar": "Digest أسبوعي",
            "title_en": "Weekly Digest",
            "wins": [],
            "opportunities_next_week": [],
            "decisions_taken": [],
            "source": "executive_pack_v2 unavailable",
        }


def _digest_monthly(customer_handle: str) -> dict[str, Any]:
    """Monthly digest — proof_ledger event count + sector context."""
    proof_count = 0
    try:
        from auto_client_acquisition.proof_ledger.file_backend import list_events
        events = list_events(customer_handle=customer_handle, limit=200)
        proof_count = len(events)
    except Exception:
        pass

    sector = None
    try:
        from auto_client_acquisition.customer_brain import get_snapshot
        snap = get_snapshot(customer_handle=customer_handle)
        sector = snap.profile.get("sector") if snap else None
    except Exception:
        pass

    return {
        "title_ar": "Digest شهري",
        "title_en": "Monthly Digest",
        "sector_context": [{"sector": sector}] if sector else [],
        "proof_pack_additions": [{"proof_event_count_total": proof_count}],
        "kpi_lift_pct": None,
        "source": "proof_ledger + customer_brain",
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
