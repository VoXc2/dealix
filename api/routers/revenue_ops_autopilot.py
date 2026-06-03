"""Revenue + Customer Ops Autopilot HTTP surface — draft-first, approval-guarded."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from dealix.execution_assurance.health import compute_full_ops_health
from dealix.revenue_ops_autopilot.knowledge import search_kb
from dealix.revenue_ops_autopilot.orchestrator import get_default_orchestrator
from dealix.revenue_ops_autopilot.policies import (
    INVOICE_DRAFT_ALLOWED_LEAD_STAGES,
    stage_transition_allowed,
)
from dealix.revenue_ops_autopilot.proof_pack import build_proof_pack_draft
from dealix.revenue_ops_autopilot.schemas import (
    DiagnosticDeliveryRecord,
    EvidenceEvent,
    InvoiceDraftRecord,
    SupportTicketRecord,
    WarRoomOutreachStatus,
)
from dealix.revenue_ops_autopilot.scoring import compute_lead_score
from dealix.revenue_ops_autopilot.store import (
    AutopilotJSONStore,
    default_store_path,
    get_autopilot_store,
    uid,
)
from dealix.revenue_ops_autopilot.support_pipeline import analyze_support
from dealix.revenue_ops_autopilot.war_room import (
    CRITICAL_OUTREACH_EVENTS,
    build_daily_summary,
    filter_leads,
    normalize_lead,
    outreach_transition_allowed,
    sync_stage_from_war_room,
    war_room_row,
)


def append_evidence_event(
    *,
    event_type: str,
    summary: str,
    entity_type: str = "",
    entity_id: str = "",
) -> EvidenceEvent:
    ev = EvidenceEvent(
        id=uid("ev"),
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        summary=summary,
    )
    return get_autopilot_store().append_evidence(ev)


def _meetings_tile() -> dict[str, Any]:
    from dealix.revenue_ops_autopilot.crm_bridge import count_meetings_this_week_from_store
    from dealix.revenue_ops_autopilot.webhook_handlers import calendly_url

    count = count_meetings_this_week_from_store()
    return {
        "count": count,
        "booked_is_estimate": count == 0,
        "calendly_url": calendly_url(),
    }


# ── Split routers (same prefixes merge with existing public/sales routers) ──
router_public_addons = APIRouter(prefix="/api/v1/public", tags=["revenue-autopilot-public"])

router_sales_ops = APIRouter(
    prefix="/api/v1/sales",
    dependencies=[Depends(require_admin_key)],
    tags=["revenue-autopilot-sales"],
)
router_evidence = APIRouter(
    prefix="/api/v1/evidence",
    dependencies=[Depends(require_admin_key)],
    tags=["revenue-autopilot-evidence"],
)
router_support = APIRouter(
    prefix="/api/v1/support",
    dependencies=[Depends(require_admin_key)],
    tags=["revenue-autopilot-support"],
)
router_kb = APIRouter(
    prefix="/api/v1/knowledge",
    dependencies=[Depends(require_admin_key)],
    tags=["revenue-autopilot-knowledge"],
)
router_diag = APIRouter(
    prefix="/api/v1/diagnostics",
    dependencies=[Depends(require_admin_key)],
    tags=["revenue-autopilot-diagnostics"],
)
router_inv = APIRouter(
    prefix="/api/v1/invoices",
    dependencies=[Depends(require_admin_key)],
    tags=["revenue-autopilot-invoices"],
)
router_ops = APIRouter(
    prefix="/api/v1/ops-autopilot",
    dependencies=[Depends(require_admin_key)],
    tags=["revenue-autopilot-ops"],
)


# ── Models ─────────────────────────────────────────────────────────────


class RiskScorePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: str = ""
    company: str = ""
    industry: str = ""
    country: str = ""
    ai_usage: str = ""
    budget_range: str = ""
    urgency: str = ""
    pain: str = ""
    notes: str = ""
    source: str = ""


class PublicLeadPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    phone: str = ""
    company: str = ""
    role: str = ""
    industry: str = ""
    country: str = ""
    pain: str = ""
    ai_usage: str = ""
    budget_range: str = ""
    urgency: str = ""
    source: str = "dealix_diagnostic"
    consent_marketing: bool = False
    consent_proof_pack: bool = False
    hold_stage: bool = False


class BookingRequestPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = ""
    email: str = ""
    notes: str = ""
    preferred_channel: str = "email"


class PublicSupportPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(..., min_length=3)
    message: str = Field(..., min_length=1, max_length=4000)


class PartnerApplyPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    company: str = ""
    partner_type: str = Field(
        default="referral",
        description="referral | implementation | co_sell",
    )
    message: str = ""
    consent: bool = False


class EvidenceCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_type: str
    summary: str
    entity_type: str = ""
    entity_id: str = ""
    account_id: str | None = None


class InvoiceDraftPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lead_id: str | None = None
    tier: str = Field(..., pattern="^(starter|standard|executive)$")


class DiagnosticCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lead_id: str | None = None


class AdvanceStagePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_stage: str
    payment_proof_logged: bool = False
    meeting_evidence_logged: bool = False
    scope_evidence_logged: bool = False
    founder_proof_pack_reviewed: bool = False


class SupportActionsPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message_override: str = ""


class WarRoomCreatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1)
    company: str = ""
    email: str = ""
    phone: str = ""
    segment: str = "agency_partner"
    pain_hypothesis: str = ""
    offer_id: str = "agency_partner_pilot"
    proof_asset: str = ""
    next_action: str = ""
    next_action_due: str | None = None
    source: str = "war_room_manual"
    war_room_status: str = "not_contacted"


class WarRoomImportPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    use_default_csv: bool = True
    rows: list[dict[str, str]] = Field(default_factory=list)


class SocialMarkPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    week: int = Field(..., ge=1, le=4)
    day: int = Field(..., ge=0, le=6)
    status: str = Field(..., pattern="^(approved|published)$")


class WarRoomPatchPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    segment: str | None = None
    pain_hypothesis: str | None = None
    offer_id: str | None = None
    proof_asset: str | None = None
    next_action: str | None = None
    next_action_due: str | None = None
    war_room_status: str | None = None
    payment_proof_logged: bool = False
    sync_stage: bool = True


# ── Public ────────────────────────────────────────────────────────────


@router_public_addons.post("/risk-score")
async def public_risk_score(body: RiskScorePayload) -> dict[str, Any]:
    fields = body.model_dump()
    score, bd = compute_lead_score(fields)
    return {
        "score": score,
        "breakdown": bd,
        "governance_note_ar": "النتيجة تقدير تشغيلي داخلياً؛ لا تُعتبر تأهيلاً نهائياً بلا مراجعة بشرية.",
        "guardrails": {
            "no_auto_outbound": True,
            "approval_for_high_impact_send": True,
        },
    }


@router_public_addons.post("/leads")
async def public_capture_lead(body: PublicLeadPayload) -> dict[str, Any]:
    orch = get_default_orchestrator()
    lead = orch.capture_lead(body.model_dump())
    return {
        "lead_id": lead.id,
        "lead_score": lead.lead_score,
        "stage": lead.stage,
        "next_action_hint_ar": lead.next_action_hint_ar,
        "outreach_draft_snippet_ar": lead.outreach_draft_snippet_ar,
        "store_path_hint": str(default_store_path()),
        "policy": {"external_send_requires_approval": True},
    }


@router_public_addons.get("/proof-pack/sample")
async def public_proof_pack_sample(locale: Annotated[str, Query()] = "ar") -> dict[str, Any]:
    draft = build_proof_pack_draft(company="", locale=locale)
    return {
        "locale": locale,
        "title_ar": "عينة هيكل Proof Pack (داخلي غير عميل حقيقي)",
        "title_en": "Proof Pack structure sample (no client data)",
        "outline": [s["title_ar"] for s in draft["sections"]],
        "draft": draft,
        "disclaimer_ar": draft["disclaimer_ar"],
        "disclaimer_en": draft["disclaimer_en"],
        "governance": draft["governance"],
    }


@router_public_addons.post("/partner-apply")
async def public_partner_apply(body: PartnerApplyPayload) -> dict[str, Any]:
    if not body.consent:
        raise HTTPException(status_code=422, detail="consent_required")
    from dealix.revenue_ops_autopilot.affiliate_compliance import scan_affiliate_message

    scan = scan_affiliate_message(body.message or "", require_disclosure=False)
    if scan.blocked:
        raise HTTPException(
            status_code=422,
            detail={
                "reason": "affiliate_compliance_blocked",
                "risk_level": scan.risk_level,
                "reasons": scan.reasons,
                "policy_ar": scan.safe_summary_ar,
            },
        )
    orch = get_default_orchestrator()
    lead = orch.capture_lead(
        {
            "name": body.name,
            "email": body.email,
            "company": body.company,
            "pain": body.message or f"partner_apply:{body.partner_type}",
            "source": f"partner_apply:{body.partner_type}",
            "stage_hint": "partner",
            "consent_marketing": True,
        },
    )
    append_evidence_event(
        event_type="partner_application_received",
        summary=f"type={body.partner_type} lead={lead.id}",
        entity_type="funnel_lead",
        entity_id=lead.id,
    )
    return {
        "status": "queued_for_founder_review",
        "lead_id": lead.id,
        "stage": lead.stage,
        "policy_ar": "لا إرسال تلقائي — مراجعة يدوية خلال 2–3 أيام عمل.",
    }


@router_public_addons.post("/booking-request")
async def public_booking_request(body: BookingRequestPayload) -> dict[str, Any]:
    eid = uid("brk")
    summary = (
        f"طلب مراجعة Diagnostic — البريد:{body.email} "
        f"القناة:{body.preferred_channel} ملاحظات:{body.notes[:400]}"
    )
    append_evidence_event(
        event_type="booking_requested",
        summary=summary,
        entity_type="booking_request",
        entity_id=eid,
    )
    from dealix.revenue_ops_autopilot.webhook_handlers import calendly_url

    return {
        "status": "queued_for_founder_calendar",
        "booking_ref": eid,
        "calendly_url": calendly_url(),
        "cta_ar": "احجز مباشرة عبر Calendly — لا رسائل خارجية آلية.",
    }


@router_public_addons.post("/support")
async def public_support_ticket(body: PublicSupportPayload) -> dict[str, Any]:
    store = get_autopilot_store()
    sig = analyze_support(body.message)

    ticket = SupportTicketRecord(
        id=uid("tkt"),
        email=body.email,
        channel="public_web",
        message=body.message,
        intent=sig.intent,
        priority=sig.priority,
        risk_level=sig.risk_level,
        ai_summary_ar=f"تصنيف: {sig.intent} — أولوية {sig.priority}",
        suggested_response_ar=sig.suggested_response_ar,
        kb_source_ids=sig.kb_source_ids,
        approval_need=sig.approval_need,
        status="waiting_founder",
    )
    store.append_ticket(ticket)
    append_evidence_event(
        event_type="support_ticket_opened",
        summary=f"tkt={ticket.id} intent={sig.intent}",
        entity_type="support_ticket",
        entity_id=ticket.id,
    )
    reply_policy = (
        "داخلي مسودة فقط — بحاجة موافقة المؤسس قبل أي إرسال للعميل."
        if sig.approval_need != "none"
        else "منخفضة المخاطر لكن لا إرسال تلقائي في الإنتاج."
    )
    return {
        "ticket_id": ticket.id,
        "intent": sig.intent,
        "priority": sig.priority,
        "risk_level": sig.risk_level,
        "suggested_reply_draft_ar": sig.suggested_response_ar,
        "approval_need": sig.approval_need,
        "reply_policy_ar": reply_policy,
        "kb_article_ids": sig.kb_source_ids,
        "escalation_reason_ar": sig.escalation_reason_ar,
    }


@router_public_addons.get("/services")
async def public_services_catalog() -> dict[str, Any]:
    return {
        "primary_offer": {
            "id": "seven_day_governance_diagnostic",
            "label_ar": "تشخيص ٧ أيام — تشغيل إيراد وذكاء اصطناعي محكوم",
            "label_en": "7-Day Governed Revenue & AI Ops Diagnostic",
            "tiers_sar": {
                "starter": 4999,
                "standard": 9999,
                "executive": 15000,
            },
        },
        "after_diagnostic_motion_ar": [
            "Revenue Intelligence Sprint",
            "Governed Ops Retainer",
        ],
        "guardrails_ar": [
            "لا رسائل خارجية آلية",
            "لا ادعاءات إيراد بلا دليل",
            "لا نشر Case Study بلا موافقة",
        ],
    }


@router_public_addons.get("/knowledge/answer")
async def public_kb_answer(q: Annotated[str, Query(min_length=2, max_length=500)]) -> dict[str, Any]:
    hits = search_kb(q, limit=1)
    if not hits:
        return {
            "answer_ar": (
                "لا يوجد ردّ معتمد في قاعدة المعرفة الداخلية لهذا السؤال. "
                "سأصعّده للمراجعة اليدوية بدلاً من الاستنتاج خارج المصدر."
            ),
            "sources": [],
            "risk_level": "medium",
            "approval_note_ar": "لا إرسال تلقائي — مراجعة بشرية فقط إذا كان الرد خارج الموقع.",
        }
    _score, art = hits[0]
    rl = str(art.get("risk_level") or "low").lower()
    return {
        "answer_ar": str(art.get("answer_ar") or art.get("answer_en")),
        "answer_en": art.get("answer_en"),
        "sources": [{"id": art.get("id"), "slug": art.get("slug")}],
        "risk_level": rl,
        "forbidden_claims_ar": art.get("forbidden_claims_ar") or [],
    }


# ── Admin / ops ───────────────────────────────────────────────────────


@router_sales_ops.get("/pipeline")
async def sales_pipeline_snapshot() -> dict[str, Any]:
    store = get_autopilot_store()
    counts = store.pipeline_counts()
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "stages": counts,
        "governance_note": "Counts from local autopilot ledger — sync with CRM manually until integration ships.",
        "storage_path_default": str(default_store_path()),
    }


@router_ops.get("/leads")
async def ops_list_leads(limit: Annotated[int, Query(ge=1, le=500)] = 120) -> dict[str, Any]:
    rows = get_autopilot_store().list_leads(limit=limit)
    return {"count": len(rows), "items": [r.model_dump(mode="json") for r in rows]}


@router_ops.get("/leads/{lead_id}")
async def ops_lead_detail(lead_id: str) -> dict[str, Any]:
    lead = get_autopilot_store().get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="lead_not_found")
    return {"item": lead.model_dump(mode="json")}


@router_ops.post("/leads/{lead_id}/advance-stage")
async def ops_advance_stage(lead_id: str, body: AdvanceStagePayload) -> dict[str, Any]:
    store: AutopilotJSONStore = get_autopilot_store()
    lead = store.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="lead_not_found")
    tgt = body.target_stage
    ok, reason = stage_transition_allowed(
        lead.stage,  # type: ignore[arg-type]
        tgt,  # type: ignore[arg-type]
        has_meeting_evidence=body.meeting_evidence_logged,
        has_scope_evidence=body.scope_evidence_logged,
        has_payment_proof=body.payment_proof_logged,
        founder_reviewed_proof_pack=body.founder_proof_pack_reviewed,
    )
    if not ok:
        raise HTTPException(status_code=409, detail={"reason": reason, "current": lead.stage})
    prev = lead.stage
    nl = lead.model_copy(update={"stage": tgt, "updated_at": datetime.now(UTC)})  # type: ignore[arg-type]
    store.upsert_lead(nl)
    append_evidence_event(
        event_type="crm_stage_advanced",
        summary=f"{prev}→{tgt} ({reason})",
        entity_type="funnel_lead",
        entity_id=lead_id,
    )
    try:
        from dealix.revenue_ops_autopilot.crm_bridge import sync_lead_to_hubspot

        crm = sync_lead_to_hubspot(nl, store=store)
    except Exception:
        crm = {"synced": False}
    return {
        "ok": True,
        "lead": nl.model_dump(mode="json"),
        "transition_reason": reason,
        "hubspot": crm,
    }


@router_ops.get("/war-room")
async def ops_war_room_list(
    due_today: bool = Query(default=False),
    needs_follow_up: bool = Query(default=False),
    status_in: str | None = Query(default=None, description="Comma-separated war_room_status values"),
    top_n: int | None = Query(default=None, ge=1, le=200),
    limit: Annotated[int, Query(ge=1, le=500)] = 200,
) -> dict[str, Any]:
    store = get_autopilot_store()
    leads = store.list_leads(limit=limit)
    statuses = [s.strip() for s in (status_in or "").split(",") if s.strip()] or None
    filtered = filter_leads(
        leads,
        due_today=due_today,
        needs_follow_up=needs_follow_up,
        status_in=statuses,
        top_n=top_n,
    )
    return {
        "count": len(filtered),
        "items": [war_room_row(L) for L in filtered],
        "policy": {"external_send_requires_approval": True},
    }


@router_ops.get("/war-room/today-pack")
async def ops_war_room_today_pack() -> dict[str, Any]:
    import json

    from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts
    from dealix.commercial_ops.paths import WAR_ROOM_TODAY_JSON
    from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets
    from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets
    from dealix.revenue_ops_autopilot.war_room import filter_leads, war_room_row

    if WAR_ROOM_TODAY_JSON.is_file():
        try:
            pack = json.loads(WAR_ROOM_TODAY_JSON.read_text(encoding="utf-8"))
            pack = attach_outreach_drafts(pack)
        except json.JSONDecodeError:
            pool = select_daily_p0_targets(load_targets(), top_n=10)
            pack = attach_outreach_drafts(build_war_room_today(pool, top_n=10))
    else:
        pool = select_daily_p0_targets(load_targets(), top_n=10)
        pack = attach_outreach_drafts(build_war_room_today(pool, top_n=10))
    store = get_autopilot_store()
    leads = [normalize_lead(L) for L in store.list_leads(limit=600)]
    top_leads = filter_leads(leads, top_n=10)
    pack["store_top_leads"] = [war_room_row(L) for L in top_leads]
    pack["store_lead_count"] = len(leads)
    return pack


@router_ops.post("/war-room/import-targets")
async def ops_war_room_import_targets(body: WarRoomImportPayload) -> dict[str, Any]:
    from dealix.commercial_ops.war_room_import import import_default_csv, import_target_rows

    orch = get_default_orchestrator()
    if body.use_default_csv and not body.rows:
        result = import_default_csv(orch)
    else:
        result = import_target_rows(body.rows, orch)
    append_evidence_event(
        event_type="war_room_targets_imported",
        summary=f"imported={result.get('imported', 0)} skipped={result.get('skipped_duplicates', 0)}",
        entity_type="war_room",
        entity_id="import",
    )
    return result


@router_ops.get("/marketing/social-today")
async def ops_marketing_social_today() -> dict[str, Any]:
    from dealix.commercial_ops.social_queue import format_linkedin_draft, get_post_for_date

    post = get_post_for_date()
    if not post:
        return {"post": None, "linkedin_draft": "", "policy_ar": "لا منشور مجدول — أضف social_content_queue.yaml"}
    return {
        "post": post,
        "linkedin_draft": format_linkedin_draft(post),
        "policy_ar": "مسودة فقط — لا نشر LinkedIn آلي.",
    }


@router_ops.get("/marketing/objection-draft")
async def ops_marketing_objection_draft(slug: str = Query(..., min_length=2, max_length=80)) -> dict[str, Any]:
    """Template draft from objection_engine_registry.yaml (no LLM)."""
    import yaml  # type: ignore[import-untyped]

    path = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "commercial"
        / "operations"
        / "objection_engine_registry.yaml"
    )
    if not path.is_file():
        raise HTTPException(status_code=404, detail="objection_registry_missing")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for obj in raw.get("objections") or []:
        if not isinstance(obj, dict):
            continue
        if str(obj.get("id") or "") == slug or str(obj.get("content_asset_slug") or "") == slug:
            return {
                "slug": slug,
                "response_draft_ar": (obj.get("response_draft_ar") or "").strip(),
                "classify": obj.get("classify"),
                "faq_snippet_ar": obj.get("faq_snippet_ar"),
                "policy_ar": "مسودة فقط — لا إرسال آلي.",
            }
    raise HTTPException(status_code=404, detail="objection_not_found")


@router_ops.post("/marketing/social-today/mark")
async def ops_marketing_social_mark(body: SocialMarkPayload) -> dict[str, Any]:
    from dealix.commercial_ops.social_queue import mark_post_status

    mark_post_status(week=body.week, day=body.day, status=body.status)
    ev = "founder_post_published_manual" if body.status == "published" else "founder_post_prepared"
    append_evidence_event(
        event_type=ev,
        summary=f"week={body.week} day={body.day} status={body.status}",
        entity_type="social_post",
        entity_id=f"w{body.week}d{body.day}",
    )
    return {"ok": True, "evidence_event": ev}


@router_ops.post("/marketing/queue-approval")
async def ops_marketing_queue_approval() -> dict[str, Any]:
    """Queue today's social draft (or latest weekly pack) into Approval Center."""
    from auto_client_acquisition.approval_center import ApprovalRequest, get_default_approval_store
    from dealix.commercial_ops.social_queue import format_linkedin_draft, get_post_for_date

    post = get_post_for_date()
    body_text = format_linkedin_draft(post) if post else ""
    title = (post or {}).get("title_ar") or "مسودة LinkedIn"
    object_id = f"w{(post or {}).get('week', 0)}d{(post or {}).get('day', 0)}" if post else "social_today"

    if not body_text.strip():
        import json

        weekly = Path(__file__).resolve().parents[2] / "var" / "content_drafts"
        files = sorted(weekly.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True) if weekly.is_dir() else []
        if files:
            pack = json.loads(files[0].read_text(encoding="utf-8"))
            drafts = pack.get("drafts") or []
            if drafts:
                d0 = drafts[0]
                body_text = str(d0.get("body") or "")
                title = str(d0.get("title_ar") or title)
                object_id = str(d0.get("id") or object_id)

    if not body_text.strip():
        raise HTTPException(
            status_code=404,
            detail="no_social_draft — schedule social_content_queue.yaml or run generate_weekly_content_drafts",
        )

    req = ApprovalRequest(
        object_type="content_draft",
        object_id=object_id,
        action_type="linkedin_post_draft",
        action_mode="approval_required",
        channel="linkedin",
        summary_ar=title[:200],
        summary_en=f"LinkedIn draft {object_id}",
        risk_level="low",
        proof_impact="authority_content",
    )
    stored = get_default_approval_store().create(req)
    append_evidence_event(
        event_type="content_draft_queued_for_approval",
        summary=f"object_id={object_id}",
        entity_type="social_post",
        entity_id=object_id,
    )
    return {
        "ok": True,
        "approval_id": stored.approval_id,
        "policy_ar": "مسودة فقط — لا نشر LinkedIn آلي حتى الموافقة.",
    }


@router_ops.get("/sales/objections")
async def ops_sales_objections() -> dict[str, Any]:
    """Objection engine registry for founder copy-paste (governed)."""
    import yaml

    path = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "commercial"
        / "operations"
        / "objection_engine_registry.yaml"
    )
    if not path.is_file():
        raise HTTPException(status_code=404, detail="objection_registry_missing")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = [ob for ob in (data.get("objections") or []) if isinstance(ob, dict)]
    return {
        "count": len(items),
        "objections": items,
        "policy_ar": "ردود مسودة — خصّص قبل الإرسال · لا إرسال آلي.",
    }


@router_ops.get("/leads/{lead_id}/meeting-brief")
async def ops_lead_meeting_brief(lead_id: str, locale: str = "ar") -> dict[str, Any]:
    lead = get_autopilot_store().get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="lead_not_found")
    lead = normalize_lead(lead)
    demo_path = f"/{locale}/business-now#strategy"
    questions_ar = [
        "أين يضيع الإيراد بعد أول تواصل؟",
        "من يملك المتابعة اليوم (اسم/دور)؟",
        "هل CRM موثوق للـ AI أم فيه فجوات مصدر؟",
        "هل يوجد موافقة قبل أي إجراء خارجي؟",
        "ما أول workflow تريدون إثباته خلال ٧ أيام؟",
    ]
    from dealix.commercial_ops.objections import match_objections

    pain_blob = " ".join(
        filter(
            None,
            [lead.pain_hypothesis, lead.pain, lead.company, lead.segment, lead.industry],
        ),
    )
    objection_hints = match_objections(pain_blob, limit=4)
    if not objection_hints:
        objection_hints = match_objections("crm وكالة سعر", limit=3)

    return {
        "lead_id": lead_id,
        "company": lead.company,
        "segment": lead.segment,
        "pain_hypothesis": lead.pain_hypothesis or lead.pain,
        "discovery_questions_ar": questions_ar,
        "demo_path": demo_path,
        "recommended_offer": lead.offer_id or "seven_day_governance_diagnostic",
        "outreach_draft_ar": lead.outreach_draft_snippet_ar,
        "objection_hints": objection_hints,
        "policy_ar": "لا ضمان ROI · لا إرسال آلي · Diagnostic كمدخل.",
    }


@router_ops.get("/war-room/summary")
async def ops_war_room_summary() -> dict[str, Any]:
    store = get_autopilot_store()
    summary = build_daily_summary(store.list_leads(limit=600))
    from auto_client_acquisition.revenue_os.anti_waste import validate_pipeline_step

    violations = validate_pipeline_step(
        has_decision_passport=False,
        lead_source="cold_whatsapp",
        action_external=True,
        upsell_attempt=False,
        proof_event_count=0,
    )
    summary["anti_waste_guard"] = {
        "blocked_sample": len(violations) > 0,
        "codes": [v.code for v in violations],
    }
    return summary


@router_ops.post("/war-room", status_code=201)
async def ops_war_room_create(body: WarRoomCreatePayload) -> dict[str, Any]:
    orch = get_default_orchestrator()
    lead = orch.capture_lead(
        {
            "name": body.name,
            "email": body.email,
            "company": body.company,
            "phone": body.phone,
            "pain": body.pain_hypothesis,
            "source": body.source,
            "segment": body.segment,
            "offer_id": body.offer_id,
            "hold_stage": True,
        },
    )
    wr_status = body.war_room_status
    if wr_status not in {
        "not_contacted",
        "message_drafted",
        "approved_to_send",
        "sent_manual",
        "replied",
        "proof_pack_sent",
        "meeting_booked",
        "scope_requested",
        "invoice_sent",
        "paid",
        "delivery_started",
        "proof_pack_delivered",
        "upsell_candidate",
        "referral_requested",
        "closed_lost",
    }:
        raise HTTPException(status_code=422, detail="invalid_war_room_status")
    nl = normalize_lead(lead).model_copy(
        update={
            "war_room_status": wr_status,  # type: ignore[arg-type]
            "segment": body.segment,
            "pain_hypothesis": body.pain_hypothesis,
            "offer_id": body.offer_id,
            "proof_asset": body.proof_asset,
            "next_action": body.next_action or lead.next_action_hint_ar,
            "next_action_due": body.next_action_due,
            "stage": sync_stage_from_war_room(wr_status),  # type: ignore[arg-type]
            "updated_at": datetime.now(UTC),
        },
    )
    get_autopilot_store().upsert_lead(nl)
    append_evidence_event(
        event_type="war_room_target_created",
        summary=f"target={nl.company or nl.name} status={wr_status}",
        entity_type="funnel_lead",
        entity_id=nl.id,
    )
    return {"item": war_room_row(nl)}


@router_ops.patch("/war-room/{lead_id}")
async def ops_war_room_patch(lead_id: str, body: WarRoomPatchPayload) -> dict[str, Any]:
    store = get_autopilot_store()
    lead = store.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="lead_not_found")
    lead = normalize_lead(lead)
    prev_status: WarRoomOutreachStatus = lead.war_room_status
    updates: dict[str, Any] = {"updated_at": datetime.now(UTC)}

    for field in ("segment", "pain_hypothesis", "offer_id", "proof_asset", "next_action", "next_action_due"):
        val = getattr(body, field)
        if val is not None:
            updates[field] = val

    if body.war_room_status is not None:
        tgt = body.war_room_status
        ok, reason = outreach_transition_allowed(
            prev_status,
            tgt,  # type: ignore[arg-type]
            has_payment_proof=body.payment_proof_logged,
        )
        if not ok:
            raise HTTPException(
                status_code=409,
                detail={"reason": reason, "current": prev_status},
            )
        updates["war_room_status"] = tgt
        if body.sync_stage:
            updates["stage"] = sync_stage_from_war_room(tgt)  # type: ignore[arg-type]

    nl = lead.model_copy(update=updates)
    store.upsert_lead(nl)

    if body.war_room_status and body.war_room_status != prev_status:
        ev_type = CRITICAL_OUTREACH_EVENTS.get(body.war_room_status)  # type: ignore[call-overload]
        if ev_type:
            append_evidence_event(
                event_type=ev_type,
                summary=f"{prev_status}→{body.war_room_status}",
                entity_type="funnel_lead",
                entity_id=lead_id,
            )

    hubspot: dict[str, Any] = {}
    try:
        from dealix.revenue_ops_autopilot.crm_bridge import sync_lead_to_hubspot

        hubspot = sync_lead_to_hubspot(nl, store=store)
    except Exception:
        hubspot = {"synced": False}

    return {"item": war_room_row(nl), "hubspot": hubspot}


@router_ops.post("/war-room/{lead_id}/generate-outreach")
async def ops_war_room_generate_outreach(lead_id: str) -> dict[str, Any]:
    from dealix.revenue_ops_autopilot.outreach_templates import build_outreach_draft

    store = get_autopilot_store()
    lead = store.get_lead(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="lead_not_found")
    lead = normalize_lead(lead)
    draft = build_outreach_draft(
        company=lead.company,
        contact=lead.name,
        segment=lead.segment,
        pain=lead.pain_hypothesis or lead.pain,
    )
    prev = lead.war_room_status
    tgt: WarRoomOutreachStatus = "message_drafted"
    ok, reason = outreach_transition_allowed(prev, tgt)
    if not ok and prev != tgt:
        tgt = prev  # type: ignore[assignment]
    nl = lead.model_copy(
        update={
            "outreach_draft_snippet_ar": draft,
            "war_room_status": tgt,
            "updated_at": datetime.now(UTC),
        },
    )
    store.upsert_lead(nl)
    append_evidence_event(
        event_type="war_room_outreach_draft_generated",
        summary=f"lead={lead_id} segment={lead.segment}",
        entity_type="funnel_lead",
        entity_id=lead_id,
    )
    return {
        "draft_ar": draft,
        "item": war_room_row(nl),
        "transition_reason": reason,
        "policy_ar": "مسودة فقط — راجع مركز الموافقات قبل أي إرسال يدوي.",
    }


class ClientPackRequest(BaseModel):
    company: str | None = None
    lead_id: str | None = None
    write_disk: bool = True


@router_ops.post("/client-pack/generate")
async def ops_client_pack_generate(body: ClientPackRequest) -> dict[str, Any]:
    """Proposal + deck notes for one target — review and send manually only."""
    from dealix.commercial_ops.client_pack import build_client_pack, find_target_row

    row = find_target_row(company=body.company, lead_id=body.lead_id)
    if not row and body.lead_id:
        store = get_autopilot_store()
        lead = store.get_lead(body.lead_id)
        if lead:
            lead = normalize_lead(lead)
            row = {
                "company": lead.company,
                "contact": lead.name,
                "segment": lead.segment,
                "pain_hypothesis": lead.pain_hypothesis or lead.pain or "",
                "offer_id": lead.offer or "governed_diagnostic",
                "motion": "A",
                "channel": "email_warm",
            }
    if not row:
        raise HTTPException(status_code=404, detail="target_not_found")
    try:
        pack = build_client_pack(row=row, write_disk=body.write_disk)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    append_evidence_event(
        event_type="client_pack_generated",
        summary=f"company={pack.get('company')}",
        entity_type="target",
        entity_id=body.lead_id or body.company or "",
    )
    return pack


@router_ops.get("/founder/full-autonomous-ops")
async def ops_founder_full_autonomous_ops(
    top_n: int = 15,
    include_value_plan: bool = False,
    include_nested: bool = False,
) -> dict[str, Any]:
    """Unified autonomous ops snapshot — GTM, expansion, comprehensive, value plan."""
    from dealix.commercial_ops.full_ops_autopilot import build_full_autonomous_ops_snapshot

    n = max(1, min(top_n, 30))
    return build_full_autonomous_ops_snapshot(
        top_n=n,
        include_nested=include_nested,
        include_value_plan=include_value_plan,
    )


class FounderAutonomousRunBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    dry_run: bool = False
    top_n: int = Field(default=15, ge=1, le=30)
    run_optional_scripts: bool = True


@router_ops.post("/founder/full-autonomous-ops/run")
async def ops_founder_full_autonomous_ops_run(
    body: FounderAutonomousRunBody | None = None,
) -> dict[str, Any]:
    """Run governed morning core (War Room, packs, metrics). No external send."""
    from dealix.commercial_ops.full_ops_autopilot import (
        build_full_autonomous_ops_snapshot,
        run_morning_core,
    )

    req = body or FounderAutonomousRunBody()
    snap = build_full_autonomous_ops_snapshot(
        top_n=req.top_n,
        include_nested=False,
        include_value_plan=False,
    )
    if req.dry_run:
        snap["morning_run"] = {
            "verdict": "DRY_RUN",
            "policy_ar": "لم يُنفَّذ — أرسل dry_run=false للتشغيل.",
        }
    else:
        snap["morning_run"] = run_morning_core(
            top_n=req.top_n,
            run_optional_scripts=req.run_optional_scripts,
        )
    return snap


@router_ops.get("/founder/gtm-stack")
async def ops_founder_gtm_stack(top_n: int = 10) -> dict[str, Any]:
    """ABM wave 1, dual-track recommendation, TTV, proof stack refs."""
    from dealix.commercial_ops.founder_debrief import list_debriefs
    from dealix.commercial_ops.gtm_stack import build_gtm_stack_snapshot

    n = max(1, min(top_n, 30))
    snap = build_gtm_stack_snapshot(abm_top_n=n)
    snap["recent_debriefs"] = list_debriefs(limit=5)
    return snap


@router_ops.get("/founder/motions-pipeline")
async def ops_founder_motions_pipeline(top_n: int = 5) -> dict[str, Any]:
    """Motion A/B/C/D daily pipeline summary."""
    from dealix.commercial_ops.motion_pipelines import build_all_motions_summary

    n = max(1, min(top_n, 15))
    return build_all_motions_summary(top_n=n)


@router_ops.get("/founder/expansion-status")
async def ops_founder_expansion_status(top_n: int = 10) -> dict[str, Any]:
    """Targeting + social + ABM expansion snapshot (no invented revenue)."""
    from dealix.commercial_ops.expansion_status import build_expansion_status

    n = max(1, min(top_n, 25))
    return build_expansion_status(abm_top_n=n)


@router_ops.get("/founder/governed-autopilot")
async def ops_founder_governed_autopilot(motion_top_n: int = 5) -> dict[str, Any]:
    """Governed full-ops autopilot status — draft-only preparation, human send/pay gates."""
    from dealix.commercial_ops.governed_autopilot import build_governed_autopilot_status

    n = max(1, min(motion_top_n, 15))
    return build_governed_autopilot_status(motion_top_n=n)


@router_ops.get("/founder/autonomous-ops/status")
async def ops_founder_autonomous_ops_status(top_n: int = 10) -> dict[str, Any]:
    """Full governed autonomous ops — expansion, benchmark, last run (no external send)."""
    from dealix.commercial_ops.autonomous_ops import build_autonomous_ops_status

    n = max(1, min(top_n, 25))
    return build_autonomous_ops_status(abm_top_n=n)


class FounderEvidenceCsvAppend(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_type: str
    company: str = Field(min_length=1, max_length=200)
    notes: str = ""
    motion: str = "A"
    offer_id: str = "ten_lead_audit"
    source_channel: str = "manual"


@router_ops.post("/founder/evidence/csv-append")
async def ops_founder_evidence_csv_append(body: FounderEvidenceCsvAppend) -> dict[str, Any]:
    """Append one row to evidence_events_tracker.csv (governed types only)."""
    from dealix.commercial_ops.evidence_append import append_evidence_row

    try:
        row = append_evidence_row(
            event_type=body.event_type.strip(),
            company=body.company.strip(),
            notes=body.notes.strip(),
            motion=body.motion.strip(),
            offer_id=body.offer_id.strip(),
            source_channel=body.source_channel.strip(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"status": "ok", "row": row, "policy_ar": "لا إرسال خارجي — سجل أدلة فقط."}


@router_ops.get("/founder/comprehensive-plan")
async def ops_founder_comprehensive_plan() -> dict[str, Any]:
    """Weekly decision, MASTER phases 0–5, backlog summary, dogfooding."""
    from dealix.commercial_ops.founder_comprehensive_plan import build_comprehensive_status

    return build_comprehensive_status()


@router_ops.get("/founder/full-autopilot")
async def ops_founder_full_autopilot() -> dict[str, Any]:
    """Governed full autopilot — queue, verdict, PLS/stage bands (no external send)."""
    from dealix.commercial_ops.founder_full_autopilot import build_autopilot_snapshot

    return build_autopilot_snapshot()


@router_ops.get("/founder/value-plan")
async def ops_founder_value_plan(top_n: int = 5) -> dict[str, Any]:
    """Unified Value Plan snapshot — Motion A, evidence, first paid, weekly KPIs."""
    from dealix.commercial_ops.value_plan import build_value_plan_snapshot

    n = max(1, min(top_n, 20))
    return build_value_plan_snapshot(motion_top_n=n)


@router_ops.get("/founder/ceo-master-plan")
async def ops_founder_ceo_master_plan() -> dict[str, Any]:
    """CEO Master Plan — 6 workstreams + daily five metrics."""
    from dealix.commercial_ops.ceo_master_plan import build_ceo_master_plan_snapshot

    return build_ceo_master_plan_snapshot()


@router_ops.get("/founder/strongest-plan")
async def ops_founder_strongest_plan() -> dict[str, Any]:
    """Founder strongest plan checklist (134+ tasks) + wiring status."""
    from dealix.commercial_ops.founder_strongest_plan import strongest_plan_snapshot

    return strongest_plan_snapshot()


@router_ops.get("/founder/strongest-ops")
async def ops_founder_strongest_ops(
    mode: str = "morning",
    run_checks: bool = False,
) -> dict[str, Any]:
    """Autonomous strongest-plan ops snapshot — tasks today, verdict, comprehensive hooks."""
    from dealix.commercial_ops.founder_strongest_ops import (
        CadenceMode,
        build_strongest_ops_snapshot,
    )

    from typing import cast
    allowed: tuple[CadenceMode, ...] = ("morning", "evening", "weekly", "full")
    m: CadenceMode = cast(CadenceMode, mode) if mode in allowed else "morning"
    return build_strongest_ops_snapshot(mode=m, run_checks=run_checks)


class FounderStrongestOpsRunBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: str = Field(default="morning", description="morning|evening|weekly|full")
    run_checks: bool = False
    write_brief: bool = True


@router_ops.post("/founder/strongest-ops/run")
async def ops_founder_strongest_ops_run(
    body: FounderStrongestOpsRunBody | None = None,
) -> dict[str, Any]:
    """Run strongest-plan autonomous brief + checks (no external send)."""
    from dealix.commercial_ops.founder_strongest_ops import CadenceMode, run_strongest_ops

    from typing import cast
    req = body or FounderStrongestOpsRunBody()
    allowed: tuple[CadenceMode, ...] = ("morning", "evening", "weekly", "full")
    m: CadenceMode = cast(CadenceMode, req.mode) if req.mode in allowed else "morning"
    return run_strongest_ops(mode=m, run_checks=req.run_checks, write_brief=req.write_brief)


@router_ops.get("/founder/cockpit")
async def ops_founder_cockpit(
    top_n: int = 15,
    mode: str = "morning",
) -> dict[str, Any]:
    """Unified founder cockpit — benchmarks, strongest ops, full autonomous, backlog."""
    from dealix.commercial_ops.founder_cockpit import build_founder_cockpit

    n = max(1, min(top_n, 30))
    return build_founder_cockpit(top_n=n, strongest_ops_mode=mode)


class FounderCockpitRunBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    top_n: int = Field(default=15, ge=1, le=30)
    run_optional_scripts: bool = True


class FounderCockpitUnifiedBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    top_n: int = Field(default=15, ge=1, le=30)
    quick: bool = False
    run_optional_scripts: bool = True


@router_ops.post("/founder/cockpit/run-unified-day")
async def ops_founder_cockpit_run_unified_day(
    body: FounderCockpitUnifiedBody | None = None,
) -> dict[str, Any]:
    """Full unified founder day in-process + refreshed cockpit (no external send)."""
    from dealix.commercial_ops.founder_cockpit import run_cockpit_unified_day

    req = body or FounderCockpitUnifiedBody()
    return run_cockpit_unified_day(
        top_n=req.top_n,
        quick=req.quick,
        run_optional_scripts=req.run_optional_scripts,
    )


@router_ops.post("/founder/cockpit/run-morning")
async def ops_founder_cockpit_run_morning(
    body: FounderCockpitRunBody | None = None,
) -> dict[str, Any]:
    """Run governed morning core + return refreshed cockpit (no external send)."""
    from dealix.commercial_ops.founder_cockpit import run_cockpit_morning

    req = body or FounderCockpitRunBody()
    return run_cockpit_morning(
        top_n=req.top_n,
        run_optional_scripts=req.run_optional_scripts,
    )


@router_ops.post("/founder/cockpit/run-evening")
async def ops_founder_cockpit_run_evening(
    body: FounderCockpitRunBody | None = None,
) -> dict[str, Any]:
    """Evening cadence — evidence reminder + strongest ops evening brief."""
    from dealix.commercial_ops.founder_cockpit import run_cockpit_evening

    req = body or FounderCockpitRunBody()
    return run_cockpit_evening(top_n=req.top_n)


@router_ops.post("/founder/cockpit/run-weekly")
async def ops_founder_cockpit_run_weekly(
    body: FounderCockpitRunBody | None = None,
) -> dict[str, Any]:
    """Weekly cadence — scorecard + strongest ops weekly brief."""
    from dealix.commercial_ops.founder_cockpit import run_cockpit_weekly

    req = body or FounderCockpitRunBody()
    return run_cockpit_weekly(
        top_n=req.top_n,
        run_optional_scripts=req.run_optional_scripts,
    )


class CompleteAutonomousDayBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    weekly: bool = False
    evening: bool = False
    skip_commercial_day: bool = False
    use_unified_in_process: bool = True
    top_n: int = Field(default=15, ge=1, le=30)


@router_ops.get("/founder/complete-autonomous-day")
async def ops_founder_complete_autonomous_day_plan(
    weekly: bool = False,
    evening: bool = False,
    skip_commercial_day: bool = False,
) -> dict[str, Any]:
    """Dry-run plan + research comparison for complete autonomous day."""
    from dealix.commercial_ops.complete_autonomous_day import build_complete_autonomous_plan

    return build_complete_autonomous_plan(
        weekly=weekly,
        evening=evening,
        skip_commercial_day=skip_commercial_day,
    )


@router_ops.post("/founder/complete-autonomous-day/run")
async def ops_founder_complete_autonomous_day_run(
    body: CompleteAutonomousDayBody | None = None,
) -> dict[str, Any]:
    """Run maximum governed autonomous day (no external send)."""
    from dealix.commercial_ops.founder_cockpit import run_cockpit_complete_autonomous_day

    req = body or CompleteAutonomousDayBody()
    return run_cockpit_complete_autonomous_day(
        top_n=req.top_n,
        weekly=req.weekly,
        evening=req.evening,
        skip_commercial_day=req.skip_commercial_day,
        use_unified_in_process=req.use_unified_in_process,
    )


@router_ops.get("/founder/commercial-value-map")
async def ops_founder_commercial_value_map(
    top_n: int = 5,
    include_value_plan: bool = True,
) -> dict[str, Any]:
    """Commercial value map — status, doc catalog, optional unified value_plan."""
    from dealix.commercial_ops.value_map_status import build_commercial_value_map

    n = max(1, min(top_n, 20))
    return build_commercial_value_map(
        include_value_plan=include_value_plan,
        motion_top_n=n,
    )


@router_ops.get("/founder/daily-pack")
async def ops_founder_daily_pack() -> dict[str, Any]:
    """Today's governed founder pack — checklist, KPI status, social snippet."""
    from dealix.commercial_ops.daily_pack import pack_status, write_daily_pack_index
    from dealix.commercial_ops.digest import build_commercial_digest
    from dealix.commercial_ops.founder_full_autopilot import build_autopilot_snapshot
    from dealix.commercial_ops.full_ops_autopilot import build_full_autonomous_ops_snapshot
    from dealix.commercial_ops.kpi_snapshot import load_kpi_commercial_status
    from dealix.commercial_ops.social_queue import format_linkedin_draft, get_post_for_date
    from dealix.commercial_ops.strategy_refs import strategy_links_flat
    from dealix.commercial_ops.value_plan import build_value_plan_snapshot

    digest = build_commercial_digest(skip_no_build=True)
    value_plan = build_value_plan_snapshot(motion_top_n=5)
    full_autonomous = build_full_autonomous_ops_snapshot(
        top_n=5,
        include_nested=False,
        include_value_plan=False,
    )
    kpi = load_kpi_commercial_status()
    social = get_post_for_date()
    try:
        pack_path = write_daily_pack_index()
        pack_index_path = str(pack_path.relative_to(Path(__file__).resolve().parents[2]))
    except ValueError:
        pack_index_path = str(pack_path)

    checklist_ar = [
        "راجع /ops/founder و /ops/war-room",
        "انسخ مسودة LinkedIn من /ops/marketing",
        "وافق على مسودات Gmail في /approvals",
        "سجّل حدثاً في evidence_events_tracker.csv",
        "10 لمسات موافَق عليها (لا cold WhatsApp)",
    ]
    if kpi.get("pending_count", 0) > 0:
        checklist_ar.insert(0, f"KPI: {kpi.get('hint_ar') or 'أكمل import من CRM'}")
    fp_verdict = (value_plan.get("first_paid_diagnostic") or {}).get("verdict")
    if fp_verdict == "PIPELINE_OPEN":
        checklist_ar.append("بوابة القيمة: أغلق أول Diagnostic مدفوع + Proof (Motion A)")

    autopilot = build_autopilot_snapshot()
    ap_verdict = autopilot.get("verdict") or {}
    for item in (autopilot.get("queue") or [])[:3]:
        title = item.get("title_ar")
        if title and title not in checklist_ar:
            checklist_ar.append(title)

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "pack_status": pack_status(),
        "pack_index_path": pack_index_path,
        "value_plan": value_plan,
        "kpi_commercial": kpi,
        "evidence": digest.get("evidence"),
        "social_post_due_today": social,
        "linkedin_draft_preview": format_linkedin_draft(social)[:500] if social else "",
        "today_focus_ar": digest.get("today_focus_ar") or [],
        "checklist_ar": checklist_ar,
        "gtm_stack": value_plan.get("gtm_stack") or {},
        "links": {
            "ops_founder": "/ar/ops/founder",
            "ops_marketing": "/ar/ops/marketing",
            "ops_war_room": "/ar/ops/war-room",
            "approvals": "/ar/approvals",
            "master_plan": "docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md",
            "gtm_playbook": "docs/commercial/GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md",
            **strategy_links_flat(),
        },
        "policy_ar": "حزمة يومية — إرسال خارجي بموافقة يدوية فقط.",
        "full_autopilot": {
            "verdict": ap_verdict,
            "queue": autopilot.get("queue"),
            "customer_stage": autopilot.get("customer_stage"),
            "pls_readiness": autopilot.get("pls_readiness"),
        },
        "comprehensive_plan_doc": "docs/ops/FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md",
        "full_autonomous_ops": {
            "automation_readiness": full_autonomous.get("automation_readiness"),
            "founder_only_actions_ar": full_autonomous.get("founder_only_actions_ar"),
            "research_alignment": full_autonomous.get("research_alignment"),
            "commands": full_autonomous.get("commands"),
        },
    }


@router_ops.get("/founder-dashboard")
async def ops_founder_dashboard() -> dict[str, Any]:
    from dealix.commercial_ops.founder_dashboard import build_sovereign_gtm_slice

    store = get_autopilot_store()
    leads = store.list_leads(limit=600)
    tix = store.list_tickets(limit=200)
    now = datetime.now(UTC).date()
    leads_today = sum(1 for L in leads if L.created_at.date() == now)
    qualified_a = sum(1 for L in leads if L.stage == "qualified_A")
    open_tickets = sum(1 for t in tix if t.status in {"new", "open", "waiting_founder"})
    escalated = sum(1 for t in tix if t.approval_need == "blocked_escalation")

    proof_pack_req = sum(1 for L in leads if bool(L.consent_proof_pack))

    pending_approval_ct = 0
    try:
        from auto_client_acquisition.approval_center import get_default_approval_store

        pending_approval_ct = len(get_default_approval_store().list_pending())
    except Exception:
        pending_approval_ct = -1

    gtm = build_sovereign_gtm_slice()
    ev_week = gtm.get("evidence_events_week") or {}

    from dealix.commercial_ops.founder_comprehensive_plan import build_comprehensive_status
    from dealix.commercial_ops.value_plan import build_value_plan_snapshot

    value_plan = build_value_plan_snapshot(motion_top_n=5)
    comprehensive = build_comprehensive_status()
    from dealix.commercial_ops.ceo_master_plan import build_ceo_master_plan_snapshot

    ceo_master = build_ceo_master_plan_snapshot()
    weekly = comprehensive.get("weekly_one_decision") or {}
    master_phase = comprehensive.get("master_execution_phase") or {}
    backlog = comprehensive.get("max_ops_backlog") or {}

    warnings: list[str] = []
    if len(leads) < 10:
        warnings.append("Pipeline ledger shows fewer than ten leads — sharpen ICP and proof funnel.")
    if int(ev_week.get("today_total") or 0) < 1:
        warnings.append("سجّل حدث أدلة واحد اليوم في evidence_events_tracker.csv")
    for w in (value_plan.get("warnings_ar") or [])[:3]:
        if w not in warnings:
            warnings.append(w)

    quotas = gtm.get("war_room_daily_quotas") or {}
    focus = [
        "Control Tower + War Room: أعلى 10 أهداف (Motion A وكالة أولاً).",
        f"أهداف اليوم: {quotas.get('approved_touches', 10)} لمسة · {quotas.get('follow_ups', 5)} متابعة · {quotas.get('partner_conversations', 1)} شريك.",
        "منشور LinkedIn: مسودة جاهزة — راجع SOAEN ثم انشر يدوياً.",
        "راجع مركز الموافقات قبل أي رسائل خارجية.",
        "راجع الطلبات عالية الخطورة في دعم العملاء أولاً.",
    ]

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "north_star_placeholder": {"metric": "paid_diagnostics_count", "is_estimate": True},
        "tiles": {
            "new_leads_today": leads_today,
            "qualified_a": qualified_a,
            "proof_pack_consent_signals": proof_pack_req,
            "evidence_events_today": ev_week.get("today_total", 0),
            "evidence_events_week": ev_week.get("week_total", 0),
            "meetings_this_week": _meetings_tile(),
            "support_open": open_tickets,
            "support_escalated_high_risk": escalated,
            "pending_approvals": pending_approval_ct,
        },
        "no_build_warnings": warnings,
        "today_focus_ar": focus,
        "sovereign_gtm": gtm,
        "value_plan": {
            "north_star": value_plan.get("north_star"),
            "first_paid_verdict": (value_plan.get("first_paid_diagnostic") or {}).get("verdict"),
            "evidence_today": (value_plan.get("evidence") or {}).get("today_total", 0),
        },
        "comprehensive_plan": {
            "weekly_one_decision": {
                "verdict": weekly.get("verdict"),
                "week_id": weekly.get("week_id"),
                "one_decision": (weekly.get("latest") or {}).get("one_decision"),
                "supports_phase": (weekly.get("latest") or {}).get("supports_phase"),
                "stop_list": (weekly.get("latest") or {}).get("stop_list") or [],
                "latest_path": weekly.get("latest_path"),
            },
            "master_execution_phase": master_phase,
            "phase_0_1_gate": {
                "verdict": (comprehensive.get("phase_0_1_gate") or {}).get("verdict"),
                "no_build_until_closed": (comprehensive.get("phase_0_1_gate") or {}).get(
                    "no_build_until_closed"
                ),
                "blockers_ar": (comprehensive.get("phase_0_1_gate") or {}).get("blockers_ar")
                or [],
            },
            "max_ops_backlog": {
                "verdict": backlog.get("verdict"),
                "percent_done": backlog.get("percent_done"),
                "done": backlog.get("done"),
                "total": backlog.get("total"),
                "doc": backlog.get("doc"),
            },
            "dogfooding": comprehensive.get("dogfooding"),
            "ceo_master_plan": {
                "overall_verdict": ceo_master.get("overall_verdict"),
                "daily_five_metrics": ceo_master.get("daily_five_metrics"),
                "p0_revenue_close": ceo_master.get("p0_revenue_close"),
                "p0_production_trust": ceo_master.get("p0_production_trust"),
                "p0_ceo_decision": ceo_master.get("p0_ceo_decision"),
                "p0_gtm_blitz": ceo_master.get("p0_gtm_blitz"),
                "p1_trust_pack": ceo_master.get("p1_trust_pack"),
                "p2_repeatability": ceo_master.get("p2_repeatability"),
            },
        },
        "links": {
            "approvals_console": "/ar/approvals",
            "sales_ops": "/ar/ops/sales",
            "master_plan": "/docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md",
            "sample_proof_pack": gtm.get("sample_proof_pack_path"),
        },
        "storage_hint": str(default_store_path()),
        "is_estimate_counts": False,
        "policy_ar": "نظامي بالكامل — الإرسال الخارجي بموافقة يدوية فقط (لا cold WhatsApp / لا LinkedIn آلي).",
    }


@router_ops.get("/full-ops-health")
async def ops_full_ops_health() -> dict[str, Any]:
    """Founder Assurance — KPI slice + YAML registry version."""

    blob = compute_full_ops_health()
    blob["policy_en"] = (
        "This endpoint is deterministic — unknown KPIs remain null until external signals integrate."
    )
    return blob


class TargetingImportPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    csv_text: str = Field(..., min_length=10, max_length=500_000)
    replace: bool = True


@router_ops.get("/targeting/pool")
async def ops_targeting_pool() -> dict[str, Any]:
    from collections import Counter

    from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV, REPO_ROOT
    from dealix.commercial_ops.targeting_csv import load_targets

    rows = load_targets(AGENCY_TARGETS_CSV)
    by_segment: Counter[str] = Counter()
    by_status: Counter[str] = Counter()
    for r in rows:
        by_segment[(r.get("segment") or "unknown").strip()] += 1
        by_status[(r.get("status") or "not_contacted").strip().lower()] += 1
    return {
        "total": len(rows),
        "csv_path": str(AGENCY_TARGETS_CSV.relative_to(REPO_ROOT)),
        "by_segment": dict(by_segment),
        "by_status": dict(by_status),
        "policy_ar": "استهداف من CSV بذرة — لا scraping.",
    }


@router_ops.get("/targeting/p0-today")
async def ops_targeting_p0_today(
    top_n: Annotated[int, Query(ge=1, le=30)] = 10,
) -> dict[str, Any]:
    from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets

    items = select_daily_p0_targets(top_n=top_n)
    return {
        "count": len(items),
        "items": items,
        "top_n": top_n,
        "policy_ar": "P0 اليوم — دوران ٣ أيام cooldown.",
    }


@router_ops.get("/targeting/today")
async def ops_targeting_today(
    top_n: Annotated[int, Query(ge=1, le=30)] = 5,
) -> dict[str, Any]:
    import yaml

    from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV, ICP_AGENCY_YAML, REPO_ROOT
    from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets

    icp: dict[str, Any] = {}
    icp_path = REPO_ROOT / "dealix" / "config" / "icp_primary.yaml"
    if icp_path.is_file():
        icp = yaml.safe_load(icp_path.read_text(encoding="utf-8")) or {}
    elif ICP_AGENCY_YAML.is_file():
        icp = yaml.safe_load(ICP_AGENCY_YAML.read_text(encoding="utf-8")) or {}

    from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts
    from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets

    pool = select_daily_p0_targets(load_targets(), top_n=top_n)
    payload = attach_outreach_drafts(build_war_room_today(pool, top_n=top_n))
    payload["icp_primary"] = {
        "positioning_ar": icp.get("positioning_ar"),
        "primary_offer_id": icp.get("primary_offer_id"),
        "segments": [s.get("id") for s in (icp.get("segments") or [])[:6] if isinstance(s, dict)],
    }
    payload["csv_path"] = str(AGENCY_TARGETS_CSV.relative_to(REPO_ROOT))
    return payload


@router_ops.post("/targeting/import")
async def ops_targeting_import(body: TargetingImportPayload) -> dict[str, Any]:
    import csv
    import io

    from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV, REPO_ROOT
    from dealix.commercial_ops.targeting_csv import (
        TARGET_FIELDS,
        build_war_room_today,
        load_targets,
    )

    reader = csv.DictReader(io.StringIO(body.csv_text.strip()))
    if not reader.fieldnames:
        raise HTTPException(status_code=422, detail="csv_missing_header")
    rows = [dict(r) for r in reader]
    if len(rows) > 500:
        raise HTTPException(status_code=422, detail="csv_too_many_rows_max_500")

    path = AGENCY_TARGETS_CSV
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(reader.fieldnames)
    for f in TARGET_FIELDS:
        if f not in fieldnames:
            fieldnames.append(f)

    if not body.replace and path.is_file():
        existing = load_targets(path)
        seen = {(r.get("company") or "").strip().lower() for r in existing}
        merged = list(existing)
        for row in rows:
            key = (row.get("company") or "").strip().lower()
            if key and key not in seen:
                merged.append(row)
                seen.add(key)
        rows = merged

    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    append_evidence_event(
        event_type="targeting_csv_imported",
        summary=f"rows={len(rows)} path={path.name}",
        entity_type="targeting",
        entity_id="agency_accounts",
    )
    preview = build_war_room_today(load_targets(path), top_n=5)
    return {
        "imported_rows": len(rows),
        "path": str(path.relative_to(REPO_ROOT)),
        "today_preview": preview,
    }


@router_ops.post("/ingest/replay-postgres")
async def ops_replay_postgres_leads(
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    sources: str | None = Query(
        default=None,
        description="Comma-separated sources filter, e.g. google_ads,meta_lead_ads",
    ),
) -> dict[str, Any]:
    """Replay recent Postgres leads into autopilot ledger (idempotent)."""

    from sqlalchemy import select

    from db.models import LeadRecord
    from db.session import async_session_factory
    from dealix.revenue_ops_autopilot.external_ingest import ingest_lead_record_model

    src_filter: set[str] | None = None
    if sources:
        src_filter = {s.strip() for s in sources.split(",") if s.strip()}

    bridged: list[str] = []
    skipped: list[str] = []
    errors: list[dict[str, str]] = []

    try:
        async with async_session_factory()() as session:
            q = select(LeadRecord).order_by(LeadRecord.created_at.desc()).limit(limit)
            rows = (await session.execute(q)).scalars().all()
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"reason": "postgres_unavailable", "error": str(exc)[:200]},
        ) from exc

    for row in rows:
        if src_filter and row.source not in src_filter:
            skipped.append(row.id)
            continue
        try:
            lead = ingest_lead_record_model(row)
            bridged.append(lead.id)
        except Exception as exc:
            errors.append({"pg_id": row.id, "error": str(exc)[:120]})

    return {
        "requested_limit": limit,
        "postgres_rows_seen": len(rows),
        "bridged_autopilot_ids": bridged,
        "skipped_source_filter": skipped,
        "errors": errors,
    }


@router_evidence.post("/events")
async def evidence_create(body: EvidenceCreatePayload) -> dict[str, Any]:
    ev = EvidenceEvent(
        id=uid("ev"),
        event_type=body.event_type,
        summary=body.summary,
        entity_type=body.entity_type,
        entity_id=body.entity_id,
        account_id=body.account_id,
    )
    get_autopilot_store().append_evidence(ev)
    return {"saved": True, "item": ev.model_dump(mode="json")}


@router_evidence.get("/events")
async def evidence_list(limit: Annotated[int, Query(ge=1, le=400)] = 80) -> dict[str, Any]:
    rows = get_autopilot_store().list_evidence(limit=limit)
    return {"count": len(rows), "items": [r.model_dump(mode="json") for r in rows]}


@router_support.get("/tickets")
async def support_list(limit: Annotated[int, Query(ge=1, le=400)] = 80) -> dict[str, Any]:
    rows = get_autopilot_store().list_tickets(limit=limit)
    return {"count": len(rows), "items": [r.model_dump(mode="json") for r in rows]}

@router_support.post("/tickets/{ticket_id}/classify")
async def support_reclassify(ticket_id: str, body: SupportActionsPayload) -> dict[str, Any]:
    store = get_autopilot_store()
    row = None
    for row in store.list_tickets(limit=1000):
        if row.id == ticket_id:
            break
    else:
        raise HTTPException(status_code=404, detail="ticket_not_found")
    assert row is not None
    text = body.message_override or row.message
    sig = analyze_support(text)
    upd = row.model_copy(
        update={
            "intent": sig.intent,
            "priority": sig.priority,
            "risk_level": sig.risk_level,
            "suggested_response_ar": sig.suggested_response_ar,
            "kb_source_ids": sig.kb_source_ids,
            "approval_need": sig.approval_need,
            "updated_at": datetime.now(UTC),
        },
    )
    store.upsert_ticket(upd)
    return {"item": upd.model_dump(mode="json")}


@router_support.post("/tickets/{ticket_id}/draft-response")
async def support_draft(ticket_id: str) -> dict[str, Any]:
    for row in get_autopilot_store().list_tickets(limit=1000):
        if row.id == ticket_id:
            sig = analyze_support(row.message)
            return {
                "draft_ar": sig.suggested_response_ar,
                "risk_level": sig.risk_level,
                "intent": sig.intent,
                "policy_ar": (
                    "لا إرسال تلقائي — انسخ المسودة من مركز الموافقات قبل الرد خارجياً.",
                ),
            }
    raise HTTPException(status_code=404, detail="ticket_not_found")


@router_kb.get("/search")
async def kb_search_endpoint(q: str, limit: int = Query(default=8, ge=1, le=40)) -> dict[str, Any]:
    hits = search_kb(q, limit=limit)
    arts = [{"score": float(s), "article": art} for s, art in hits]
    return {"count": len(arts), "items": arts}


@router_diag.post("/", status_code=201)
async def diagnostic_create(body: DiagnosticCreatePayload) -> dict[str, Any]:
    rec = DiagnosticDeliveryRecord(
        id=uid("dia"),
        lead_id=body.lead_id,
        stage="intake",
        onboarding_checklist=[
            "تأكيد نطاق التشخيص وخط الأساس المعتمد",
            "توثيق حدود الموافقة ومستويات الأدلة",
            "تجميع نقاط قرار تجريبية (Top 3 decisions)",
            "جدولة المراجعة مع المؤسس قبل أي مخرجة خارجية نهائية",
        ],
        proof_pack_outline_ar="مسودة هيكل الدليل — تخصيص بحسب عميلكم بعد الموافقة فقط.",
    )
    store = get_autopilot_store()
    store.append_diagnostic(rec)
    append_evidence_event(
        event_type="diagnostic_engagement_opened",
        summary=f"id={rec.id}",
        entity_type="diagnostic",
        entity_id=rec.id,
    )
    return {"item": rec.model_dump(mode="json")}


@router_diag.get("/{diag_id}")
async def diagnostic_detail(diag_id: str) -> dict[str, Any]:
    hit = get_autopilot_store().get_diagnostic(diag_id)
    if not hit:
        raise HTTPException(status_code=404, detail="diagnostic_not_found")
    return {"item": hit.model_dump(mode="json")}


@router_diag.post("/{diag_id}/generate-proof-pack")
async def diagnostic_generate_proof_pack(diag_id: str) -> dict[str, Any]:
    store = get_autopilot_store()
    hit = store.get_diagnostic(diag_id)
    if not hit:
        raise HTTPException(status_code=404, detail="diagnostic_not_found")
    company = ""
    if hit.lead_id:
        lead = store.get_lead(hit.lead_id)
        if lead:
            company = lead.company
    draft = build_proof_pack_draft(company=company, locale="ar")
    append_evidence_event(
        event_type="proof_pack_draft_generated",
        summary=f"diag={diag_id}",
        entity_type="diagnostic",
        entity_id=diag_id,
    )
    return {
        "diagnostic_id": diag_id,
        "proof_pack_draft": draft,
        "policy_ar": "لا إرسال نهائي للعميل بلا مراجعة المؤسس.",
    }


_TIER_AMOUNT = {"starter": 4999.0, "standard": 9999.0, "executive": 15000.0}


@router_inv.post("/draft")
async def invoice_create_draft(body: InvoiceDraftPayload) -> dict[str, Any]:
    if body.lead_id:
        lead_bind = get_autopilot_store().get_lead(body.lead_id)
        if not lead_bind:
            raise HTTPException(status_code=404, detail="lead_not_found")
        if lead_bind.stage not in INVOICE_DRAFT_ALLOWED_LEAD_STAGES:
            raise HTTPException(
                status_code=422,
                detail={
                    "reason": "invoice_draft_blocked_until_scope_sent",
                    "current_stage": lead_bind.stage,
                    "allowed_lead_stages": sorted(INVOICE_DRAFT_ALLOWED_LEAD_STAGES),
                },
            )
    amt = _TIER_AMOUNT[body.tier]  # type: ignore[index]
    inv = InvoiceDraftRecord(
        id=uid("inv"),
        lead_id=body.lead_id,
        tier=body.tier,  # type: ignore[arg-type]
        amount_sar=amt,
        line_items_ar=[
            "تشخيص ٧ أيام — تشغيل إيراد وذكاء اصطناعي محكوم",
            "مخرجات مسودة + مراجعة حوكمة قبل التسليم النهائي",
        ],
        status="approval_required",
    )
    get_autopilot_store().append_invoice_draft(inv)
    try:
        from auto_client_acquisition.approval_center import get_default_approval_store
        from auto_client_acquisition.approval_center.schemas import ApprovalRequest

        get_default_approval_store().create(
            ApprovalRequest(
                object_type="invoice_draft",
                object_id=inv.id,
                action_type="payment_reminder",
                action_mode="approval_required",
                channel="finance_manual",
                summary_ar="مسودة فاتورة بحاجة موافقة قبل إرسال أي رابط دفع.",
                summary_en="Invoice draft requires founder approval before payment link.",
                risk_level="high",
                proof_impact="commercial_close_guarded",
            ),
        )
    except Exception:
        pass

    append_evidence_event(
        event_type="invoice_draft_created",
        summary=f"id={inv.id} tier={body.tier} amount_sar={amt}",
        entity_type="invoice_draft",
        entity_id=inv.id,
    )
    return {"item": inv.model_dump(mode="json")}


def _marketing_router() -> APIRouter:
    from api.routers.marketing_ops import router_marketing

    return router_marketing


AUTOPILOT_ROUTERS: list[APIRouter] = [
    router_public_addons,
    router_sales_ops,
    router_evidence,
    router_support,
    router_kb,
    router_diag,
    router_inv,
    router_ops,
    _marketing_router(),
]
