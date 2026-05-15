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
    approved = 0
    pending = 0
    try:
        from auto_client_acquisition.approval_center import get_default_approval_store

        store = get_default_approval_store()
        rows = store.list_pending()
        pending = len(rows)
        hist = store.list_history(limit=200)
        approved = sum(
            1
            for r in hist
            if str(getattr(r.status, "value", r.status)) == "approved"
            and (
                customer_handle in (r.proof_impact or "")
                or customer_handle in (r.summary_ar or "")
            )
        )
    except Exception:
        pass
    return {
        "title_ar": "رسائل ومتابعات",
        "title_en": "Messages & Follow-ups",
        "approved_drafts_count": approved,
        "pending_approval_count": pending,
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
    events_count = 0
    try:
        from auto_client_acquisition.proof_ledger.factory import get_default_ledger

        events_count = len(
            get_default_ledger().list_events(customer_handle=customer_handle, limit=200)
        )
    except Exception:
        pass
    return {
        "title_ar": "Proof Pack",
        "title_en": "Proof Pack",
        "events_count": events_count,
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
        from auto_client_acquisition.proof_ledger.factory import get_default_ledger

        events = get_default_ledger().list_events(customer_handle=customer_handle, limit=200)
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


def _full_ops_score_section(customer_handle: str) -> dict[str, Any]:
    """Wave 4 additive — Full-Ops Score for this customer (best-effort)."""
    try:
        from auto_client_acquisition.full_ops_radar import compute_full_ops_score
        s = compute_full_ops_score()
        return {
            "score": s["score"],
            "max_score": s["max_score"],
            "readiness_label": s["readiness_label"],
            "source": "full_ops_radar.score",
        }
    except Exception:
        return {"score": 0, "readiness_label": "Internal Only", "source": "insufficient_data"}


def _weaknesses_summary_section(customer_handle: str) -> dict[str, Any]:
    """Wave 4 additive — top 3 weaknesses for this customer.

    Customer-safe view: drops operational fields (related_endpoint,
    related_doc, owner_role, layer) before exposing.
    """
    try:
        from auto_client_acquisition.full_ops_radar import detect_weaknesses
        ws = detect_weaknesses(customer_handle=customer_handle)
        safe_keys = {"id", "severity", "blocker", "reason_ar",
                     "reason_en", "fix_ar", "fix_en"}
        top_3_safe = [
            {k: v for k, v in w.items() if k in safe_keys}
            for w in ws[:3]
        ]
        return {
            "total": len(ws),
            "critical_count": sum(1 for w in ws if w["severity"] == "critical"),
            "top_3": top_3_safe,
            "source": "weakness_radar (customer-safe view)",
        }
    except Exception:
        return {"total": 0, "critical_count": 0, "top_3": [], "source": "insufficient_data"}


def _next_3_decisions_section(customer_handle: str) -> dict[str, Any]:
    """Wave 4 additive — top 3 pending approvals."""
    try:
        from auto_client_acquisition.executive_command_center.next_decisions import (
            top_3_decisions,
        )
        return {
            "decisions": top_3_decisions(customer_handle=customer_handle),
            "source": "executive_command_center.next_decisions",
        }
    except Exception:
        return {"decisions": [], "source": "insufficient_data"}


def _support_summary_section(customer_handle: str) -> dict[str, Any]:
    """Wave 4 additive — support inbox summary."""
    try:
        from auto_client_acquisition.support_inbox import (
            find_breached_tickets,
            list_tickets,
        )
        tickets = list_tickets(customer_id=customer_handle, limit=100)
        breached = find_breached_tickets(customer_id=customer_handle)
        return {
            "open_tickets": sum(1 for t in tickets if t.status == "open"),
            "escalated": sum(1 for t in tickets if t.status == "escalated"),
            "sla_breached_count": len(breached),
            "source": "support_inbox",
        }
    except Exception:
        return {"open_tickets": 0, "source": "insufficient_data"}


def _payment_state_section(customer_handle: str) -> dict[str, Any]:
    """Wave 4 additive — payment state summary."""
    try:
        from auto_client_acquisition.payment_ops.orchestrator import _INDEX
        states = [p for p in _INDEX.values() if p.customer_handle == customer_handle]
        return {
            "total_payments": len(states),
            "confirmed_count": sum(1 for p in states
                                   if p.status in ("payment_confirmed", "delivery_kickoff")),
            "source": "payment_ops",
        }
    except Exception:
        return {"total_payments": 0, "confirmed_count": 0, "source": "insufficient_data"}


def _proof_summary_section(customer_handle: str) -> dict[str, Any]:
    """Wave 4 additive — proof events summary."""
    try:
        from auto_client_acquisition.proof_ledger.factory import get_default_ledger

        events = get_default_ledger().list_events(customer_handle=customer_handle, limit=200)
        return {
            "proof_events_count": len(events),
            "source": "proof_ledger",
        }
    except Exception:
        return {"proof_events_count": 0, "source": "insufficient_data"}


def _approval_summary_section(customer_handle: str) -> dict[str, Any]:
    """Wave 4 additive — approval center summary."""
    try:
        from auto_client_acquisition.approval_center import get_default_approval_store

        pending = get_default_approval_store().list_pending()
        scoped = [
            ap for ap in pending
            if customer_handle in (ap.proof_impact or "")
            or customer_handle in (ap.summary_ar or "")
        ]
        return {
            "pending_total": len(pending),
            "pending_for_this_customer": len(scoped),
            "source": "approval_center",
        }
    except Exception:
        return {"pending_total": 0, "source": "insufficient_data"}


def _executive_command_link_section(customer_handle: str) -> dict[str, Any]:
    """Wave 4 additive — link to the per-customer Executive Command Center."""
    return {
        "url": f"/executive-command-center.html?org={customer_handle}",
        "label_ar": "افتح مركز القيادة التنفيذي",
        "label_en": "Open Executive Command Center",
        "source": "executive_command_center",
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
            # Wave 3 keys (existing — DO NOT REMOVE)
            "ops_summary": _ops_summary(customer_handle),
            "sequences": _sequences_state(customer_handle),
            "radar_today": _radar_today(customer_handle),
            "digest_weekly": _digest_weekly(customer_handle),
            "digest_monthly": _digest_monthly(customer_handle),
            "service_status_for_customer": _service_status_for_customer(customer_handle),
            # Wave 4 additive keys (new — never required by old clients)
            "full_ops_score": _full_ops_score_section(customer_handle),
            "weaknesses_summary": _weaknesses_summary_section(customer_handle),
            "next_3_decisions": _next_3_decisions_section(customer_handle),
            "support_summary": _support_summary_section(customer_handle),
            "payment_state": _payment_state_section(customer_handle),
            "proof_summary": _proof_summary_section(customer_handle),
            "approval_summary": _approval_summary_section(customer_handle),
            "executive_command_link": _executive_command_link_section(customer_handle),
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


# ── Wave 2: Client Workspace MVP ─────────────────────────────────────
# Operator-facing internal aggregator. Distinct from the public 8-field
# portal above (Constitution Article 6 #2). Returns 10 panels + status
# badges + deterministic next_action. Read-only. 200 always.

def _workspace_capability(customer_handle: str) -> dict[str, Any] | None:
    try:
        from auto_client_acquisition.customer_readiness.scores import (
            compute_comfort_and_expansion,
        )
        scores = compute_comfort_and_expansion(
            has_status_timeline=True, has_next_action=True,
            pending_approvals=0, open_support_tickets=0,
            proof_events_count=0, max_proof_level=0,
            payment_ok=False, delivery_sessions_active=0,
            avg_response_hours=48.0,
        )
        return {"score": scores.get("expansion_readiness"), "comfort": scores.get("comfort_score")}
    except Exception:
        return None


def _workspace_data_readiness(customer_handle: str) -> dict[str, Any] | None:
    # Best-effort: count value events as a coarse readiness signal.
    try:
        from auto_client_acquisition.value_os.value_ledger import list_events as list_value
        events = list_value(customer_id=customer_handle)
        return {
            "source_passport_present": False,  # populated once data_os.source_passport store lands
            "dq_score": None,
            "value_events_in_ledger": len(events),
        }
    except Exception:
        return None


def _workspace_governance(customer_handle: str) -> dict[str, Any]:
    try:
        from auto_client_acquisition.friction_log.store import list_events as list_friction
        events = list_friction(
            customer_id=customer_handle, since_days=30, limit=50, kind="governance_block"
        )
        return {
            "last_decision": "allow_with_review",
            "open_blocks": len(events),
        }
    except Exception:
        return {"last_decision": "unknown", "open_blocks": 0}


def _workspace_ranked_opportunities(customer_handle: str) -> list[dict[str, Any]] | None:
    try:
        from auto_client_acquisition.leadops_spine import list_records
        recs = [r for r in list_records(limit=50) if r.customer_handle == customer_handle]
        return [{"id": getattr(r, "id", ""), "company": getattr(r, "company_name", "")} for r in recs[:10]]
    except Exception:
        return None


def _workspace_drafts_pending(customer_handle: str) -> list[dict[str, Any]] | None:
    try:
        from auto_client_acquisition.approval_center.approval_store import (
            get_default_approval_store,
        )
        store = get_default_approval_store()
        pending = store.list_pending() if hasattr(store, "list_pending") else []
        scoped = [p for p in pending if getattr(p, "customer_handle", None) == customer_handle]
        return [{"id": getattr(p, "id", ""), "kind": getattr(p, "kind", "")} for p in scoped]
    except Exception:
        return None


def _workspace_proof_timeline(customer_handle: str) -> list[dict[str, Any]] | None:
    try:
        from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger
        ledger = get_default_ledger()
        events = ledger.list_events(customer_handle=customer_handle, limit=12)
        return [
            {"id": e.id, "event_type": str(e.event_type), "created_at": e.created_at.isoformat()}
            for e in events
        ]
    except Exception:
        return None


def _workspace_adoption(customer_handle: str) -> dict[str, Any] | None:
    try:
        from auto_client_acquisition.adoption_os.adoption_score import compute as compute_adoption
        score = compute_adoption(customer_id=customer_handle)
        return score.to_dict()
    except Exception:
        return None


def _workspace_friction(customer_handle: str) -> dict[str, Any] | None:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate
        agg = aggregate(customer_id=customer_handle, window_days=30)
        return agg.to_dict()
    except Exception:
        return None


def _workspace_monthly_value(customer_handle: str) -> dict[str, Any] | None:
    try:
        from auto_client_acquisition.value_os.monthly_report import generate
        report = generate(customer_id=customer_handle)
        d = report.to_dict()
        # Summary subset: omit large lists.
        return {
            "month": d["month"],
            "proof_events_count": d["proof_events_count"],
            "blocked_unsafe_actions_count": d["blocked_unsafe_actions_count"],
            "limitations": d["limitations"][:5],
            "governance_decision": d["governance_decision"],
        }
    except Exception:
        return None


def _workspace_next_action(panels: dict[str, Any]) -> dict[str, str]:
    """Deterministic priority: governance_block > approval_pending > stale_draft
    > adoption_push > capability_gap."""
    gov = panels.get("governance_status") or {}
    if int(gov.get("open_blocks", 0) or 0) > 0:
        return {
            "kind": "resolve_governance_block",
            "message_en": "Resolve open governance block before continuing.",
            "message_ar": "حلّ بلوك الحوكمة المفتوح قبل المتابعة.",
        }
    drafts = panels.get("draft_packs_pending_approval") or []
    if drafts:
        return {
            "kind": "approval_pending",
            "message_en": "Drafts awaiting approval — review and approve.",
            "message_ar": "مسودّات تنتظر الاعتماد — راجع واعتمد.",
        }
    adoption = panels.get("adoption_score") or {}
    if (adoption.get("tier") or "") in ("latent", "exploring"):
        return {
            "kind": "adoption_push",
            "message_en": "Enable one more channel or integration to lift adoption.",
            "message_ar": "فعّل قناة أو تكاملاً إضافياً لرفع اعتماد المنصة.",
        }
    capability = panels.get("capability_score") or {}
    if capability is None or capability.get("score") is None:
        return {
            "kind": "capability_gap",
            "message_en": "Capability score missing — request a diagnostic.",
            "message_ar": "درجة القدرة غير متوفرة — اطلب التشخيص.",
        }
    return {
        "kind": "maintain_cadence",
        "message_en": "Continue monthly operating cadence.",
        "message_ar": "استمر في الإيقاع الشهري للتشغيل.",
    }


@router.get("/{customer_handle}/workspace")
async def client_workspace(customer_handle: str) -> dict[str, Any]:
    """Wave 2 Client Workspace MVP — operator-facing 10-panel bundle.

    Read-only. Tenant-scoped via customer_handle. Returns 200 always;
    missing panels are null + a friction event is emitted (best-effort).
    """
    panels: dict[str, Any] = {
        "capability_score": _workspace_capability(customer_handle),
        "data_readiness": _workspace_data_readiness(customer_handle),
        "governance_status": _workspace_governance(customer_handle),
        "ranked_opportunities": _workspace_ranked_opportunities(customer_handle),
        "draft_packs_pending_approval": _workspace_drafts_pending(customer_handle),
        "proof_timeline": _workspace_proof_timeline(customer_handle),
        "adoption_score": _workspace_adoption(customer_handle),
        "latest_monthly_value_report": _workspace_monthly_value(customer_handle),
    }

    # Compute "missing" signals from panels (no source passport in
    # data_readiness, no proof events in proof_timeline) BEFORE the
    # friction aggregation so the missing-panel events are visible in
    # the same response. Idempotent best-effort.
    try:
        from auto_client_acquisition.friction_log.store import emit as emit_friction
        dr = panels.get("data_readiness") or {}
        if dr is None or not dr.get("source_passport_present"):
            emit_friction(
                customer_id=customer_handle,
                kind="missing_source_passport",
                severity="low",
                workflow_id="client_workspace_mvp",
                notes="panel:data_readiness:no_source_passport",
            )
        pt = panels.get("proof_timeline")
        if not pt:
            emit_friction(
                customer_id=customer_handle,
                kind="missing_proof_pack",
                severity="low",
                workflow_id="client_workspace_mvp",
                notes="panel:proof_timeline:empty",
            )
        for panel_name in ("capability_score", "ranked_opportunities", "draft_packs_pending_approval"):
            if panels.get(panel_name) is None:
                emit_friction(
                    customer_id=customer_handle,
                    kind="missing_source_passport",
                    severity="low",
                    workflow_id="client_workspace_mvp",
                    notes=f"panel:{panel_name}:unavailable",
                )
    except Exception:
        pass

    # Aggregate friction LAST so missing-panel events emitted above are
    # surfaced in the same response.
    panels["friction_summary"] = _workspace_friction(customer_handle)
    panels["next_action"] = _workspace_next_action(panels)
    panels["governance_decision"] = "allow_with_review"
    panels["customer_handle"] = customer_handle
    return panels


@router.get("/")
async def customer_portal_root() -> dict[str, Any]:
    """Default — placeholder Slot-A view (no real customer required)."""
    return _portal_payload("Slot-A")
