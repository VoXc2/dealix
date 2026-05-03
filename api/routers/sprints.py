"""
Sprints router — Phase 2 Delivery Engine.

The 7-Day Growth Proof Sprint API. One sprint per Pilot 499 SAR. Each
day-action emits matching Proof Events into the ledger and updates the
sprint's day_outputs_json so the Customer Workspace renders the
output without re-generating.

Endpoints:
    POST  /api/v1/sprints/start
        body: {customer_id, service_id?}
        Creates a SprintRecord. Snapshots the Service Contract.

    GET   /api/v1/sprints/{sprint_id}
        Returns full state.

    GET   /api/v1/sprints/by-customer/{customer_id}
        Returns the most recent sprint for a customer.

    POST  /api/v1/sprints/{sprint_id}/diagnostic/generate         (Day 1)
    POST  /api/v1/sprints/{sprint_id}/opportunities/generate      (Day 2)
    POST  /api/v1/sprints/{sprint_id}/messages/generate           (Day 3)
    POST  /api/v1/sprints/{sprint_id}/meeting-prep                (Day 4)
    GET   /api/v1/sprints/{sprint_id}/review                      (Day 5)
    POST  /api/v1/sprints/{sprint_id}/proof/draft                 (Day 6)
    POST  /api/v1/sprints/{sprint_id}/close-out                   (Day 7)

All generators are deterministic (no LLM). Customer Brain → output dict.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import desc, select

from auto_client_acquisition.delivery.sprint_templates import (
    generate_close_out,
    generate_diagnostic,
    generate_meeting_prep,
    generate_message_pack,
    generate_opportunity_pack,
    generate_pipeline_review,
    generate_proof_draft,
)
from auto_client_acquisition.revenue_company_os.proof_ledger import record as record_proof
from db.models import CustomerRecord, ProspectRecord, ProofEventRecord, SprintRecord
from db.session import get_session

router = APIRouter(prefix="/api/v1/sprints", tags=["sprints"])

log = logging.getLogger(__name__)


# Map sprint day → RWU emitted on generation
_DAY_RWU = {
    1: "diagnostic_delivered",
    2: "opportunity_created",  # 10 of these
    3: "draft_created",         # 6 of these
    4: "meeting_drafted",
    5: "target_ranked",
    6: "proof_generated",
    7: "proof_generated",
}


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _new_sprint_id() -> str:
    return f"spr_{uuid.uuid4().hex[:14]}"


def _serialize_sprint(s: SprintRecord) -> dict[str, Any]:
    return {
        "sprint_id": s.id,
        "customer_id": s.customer_id,
        "service_id": s.service_id,
        "current_day": s.current_day,
        "status": s.status,
        "started_at": s.started_at.isoformat() if s.started_at else None,
        "completed_at": s.completed_at.isoformat() if s.completed_at else None,
        "day_outputs": dict(s.day_outputs_json or {}),
        "contract_snapshot": dict(s.contract_snapshot_json or {}),
        "proof_pack_event_id": s.proof_pack_event_id,
    }


async def _load_customer_brain(session, customer_id: str) -> dict[str, Any]:
    cust = (await session.execute(
        select(CustomerRecord).where(CustomerRecord.id == customer_id)
    )).scalar_one_or_none()
    if cust is None:
        return {}
    return {
        "company_name": getattr(cust, "company_name", "") or "",
        "website": getattr(cust, "website", None),
        "sector": getattr(cust, "sector", None),
        "city": getattr(cust, "city", None),
        "offer_ar": getattr(cust, "offer_ar", None),
        "ideal_customer_ar": getattr(cust, "ideal_customer_ar", None),
        "average_deal_value_sar": float(getattr(cust, "average_deal_value_sar", 0) or 0),
        "approved_channels": list(getattr(cust, "approved_channels", []) or []),
        "blocked_channels": list(getattr(cust, "blocked_channels", []) or []),
        "tone_ar": getattr(cust, "tone_ar", "professional_saudi_arabic"),
        "forbidden_claims": list(getattr(cust, "forbidden_claims", []) or []),
    }


async def _emit_day_proof(session, sprint: SprintRecord, day: int, label_ar: str) -> str:
    """Emit a Proof Event for the day-action; idempotent on re-run."""
    unit_type = _DAY_RWU.get(day, "target_ranked")
    proof = await record_proof(
        session,
        unit_type=unit_type,
        customer_id=sprint.customer_id,
        actor="sprint_engine",
        approval_required=False,
        approved=True,
        risk_level="low",
        meta={
            "sprint_id": sprint.id,
            "day": day,
            "label_ar": label_ar,
        },
    )
    return proof.id


async def _load_or_404(session, sprint_id: str) -> SprintRecord:
    sprint = (await session.execute(
        select(SprintRecord).where(SprintRecord.id == sprint_id)
    )).scalar_one_or_none()
    if sprint is None:
        raise HTTPException(status_code=404, detail="sprint_not_found")
    return sprint


# ── Endpoints ─────────────────────────────────────────────────────


@router.post("/start")
async def start_sprint(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    customer_id = str(body.get("customer_id") or "").strip()
    if not customer_id:
        raise HTTPException(status_code=400, detail="customer_id_required")
    service_id = str(body.get("service_id") or "growth_starter").strip()

    # Snapshot the Service Contract
    from api.routers.services import SERVICE_CONTRACTS
    contract = SERVICE_CONTRACTS.get(service_id, {})
    if not contract:
        raise HTTPException(status_code=400, detail=f"unknown_service:{service_id}")

    async with get_session() as session:
        # Verify customer exists
        cust = (await session.execute(
            select(CustomerRecord).where(CustomerRecord.id == customer_id)
        )).scalar_one_or_none()
        if cust is None:
            raise HTTPException(status_code=404, detail="customer_not_found")

        sprint = SprintRecord(
            id=_new_sprint_id(),
            customer_id=customer_id,
            service_id=service_id,
            started_at=_now(),
            current_day=0,
            status="started",
            contract_snapshot_json=dict(contract),
            day_outputs_json={},
            actor=str(body.get("actor") or "founder"),
        )
        session.add(sprint)
        # Update customer's current_service_id pointer
        if cust:
            cust.current_service_id = service_id
        await session.commit()
        log.info("sprint_started sprint_id=%s customer_id=%s service_id=%s",
                 sprint.id, customer_id, service_id)
        return _serialize_sprint(sprint)


@router.get("/{sprint_id}")
async def get_sprint(sprint_id: str) -> dict[str, Any]:
    async with get_session() as session:
        sprint = await _load_or_404(session, sprint_id)
        return _serialize_sprint(sprint)


@router.get("/by-customer/{customer_id}")
async def get_sprint_by_customer(customer_id: str) -> dict[str, Any]:
    async with get_session() as session:
        sprint = (await session.execute(
            select(SprintRecord)
            .where(SprintRecord.customer_id == customer_id)
            .order_by(desc(SprintRecord.started_at))
            .limit(1)
        )).scalar_one_or_none()
        if sprint is None:
            raise HTTPException(status_code=404, detail="no_sprint_for_customer")
        return _serialize_sprint(sprint)


async def _generate_day(
    sprint_id: str,
    day: int,
    generator,
    *,
    label_ar: str,
    extra_args: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Common pipeline: load sprint → load brain → generate → persist → emit RWU."""
    async with get_session() as session:
        sprint = await _load_or_404(session, sprint_id)
        brain = await _load_customer_brain(session, sprint.customer_id)
        try:
            output = generator(brain, **(extra_args or {}))
        except TypeError:
            # Generator didn't accept extra_args
            output = generator(brain)

        outputs = dict(sprint.day_outputs_json or {})
        outputs[f"day_{day}"] = output
        sprint.day_outputs_json = outputs
        sprint.current_day = max(sprint.current_day, day)
        sprint.status = f"day_{day}"

        proof_id = await _emit_day_proof(session, sprint, day, label_ar)
        await session.commit()
        return {
            "sprint_id": sprint_id,
            "day": day,
            "output": output,
            "proof_event_id": proof_id,
            "status": sprint.status,
        }


@router.post("/{sprint_id}/diagnostic/generate")
async def day_1(sprint_id: str) -> dict[str, Any]:
    """Day 1 — Mini Diagnostic. Deterministic baseline + LLM polish on
    why_segment_ar / risk_to_avoid_ar with Brain context. Falls back to
    template on any failure."""
    from auto_client_acquisition.intelligence.smart_drafter import get_drafter

    async with get_session() as session:
        sprint = await _load_or_404(session, sprint_id)
        brain = await _load_customer_brain(session, sprint.customer_id)

        baseline = generate_diagnostic(brain)
        drafter = get_drafter()

        # LLM polish: enrich why_segment_ar with Brain context
        polish_prompt = (
            f"الشريحة المختارة: {baseline['best_segment_ar']}.\n"
            f"شركة العميل: {brain.get('company_name','—')} في {brain.get('city','—')}.\n"
            f"عرضهم: {brain.get('offer_ar','—')}.\n"
            f"اكتب جملة واحدة عربية محددة (ليست عامة) تشرح لماذا هذه "
            f"الشريحة الأنسب الآن — لا أكثر من ٢٠ كلمة، بنبرة سعودية محترمة. "
            f"ممنوع 'نضمن' أو 'guaranteed'."
        )
        r1 = await drafter._safe_run(
            "REASONING", polish_prompt,
            max_tokens=80, temperature=0.6,
            fallback=baseline.get("why_segment_ar", ""),
        )

        risk_prompt = (
            f"شركة في قطاع {brain.get('sector','—')} في {brain.get('city','—')}.\n"
            f"اذكر مخاطرة PDPL واحدة محددة يجب تجنبها هذا الأسبوع — ليست عامة. "
            f"≤ ٢٥ كلمة عربي."
        )
        r2 = await drafter._safe_run(
            "REASONING", risk_prompt,
            max_tokens=80, temperature=0.5,
            fallback=baseline.get("risk_to_avoid_ar", ""),
        )

        baseline["why_segment_ar"] = r1.text or baseline.get("why_segment_ar", "")
        baseline["risk_to_avoid_ar"] = r2.text or baseline.get("risk_to_avoid_ar", "")
        baseline["llm_enhanced"] = bool(r1.used_llm or r2.used_llm)
        baseline["llm_provider"] = r1.provider or r2.provider
        baseline["llm_safety_passed"] = r1.safety_passed and r2.safety_passed

        outputs = dict(sprint.day_outputs_json or {})
        outputs["day_1"] = baseline
        sprint.day_outputs_json = outputs
        sprint.current_day = max(sprint.current_day, 1)
        sprint.status = "day_1"
        proof_id = await _emit_day_proof(session, sprint, 1, "Mini Diagnostic (LLM-enhanced)")
        await session.commit()
        return {
            "sprint_id": sprint_id,
            "day": 1,
            "output": baseline,
            "proof_event_id": proof_id,
            "status": sprint.status,
        }


@router.post("/{sprint_id}/opportunities/generate")
async def day_2(sprint_id: str) -> dict[str, Any]:
    """Day 2 — Opportunity Pack. Each of the 10 opps gets a
    ChannelOrchestrator-recommended channel based on Brain + active gates,
    not a static template value."""
    from auto_client_acquisition.intelligence.channel_orchestrator import recommend
    from core.config.settings import get_settings

    s = get_settings()
    gates = {
        "whatsapp_allow_customer_send": bool(getattr(s, "whatsapp_allow_customer_send", False)),
        "whatsapp_allow_internal_send": bool(getattr(s, "whatsapp_allow_internal_send", False)),
    }

    async with get_session() as session:
        sprint = await _load_or_404(session, sprint_id)
        brain = await _load_customer_brain(session, sprint.customer_id)
        baseline = generate_opportunity_pack(brain)

        # For each opportunity, get a per-prospect channel recommendation.
        # Synthetic prospect = no consent yet (new opp), no last inbound.
        synthetic_prospect = {
            "consent_status": "none",
            "allowed_channels": [],
            "blocked_channels": [],
        }
        for opp in baseline.get("opportunities", []):
            recs = recommend(prospect=synthetic_prospect, brain=brain, gates=gates)
            best = next((r for r in recs if r.allowed), None)
            blocked = [
                {"channel": r.channel, "reason_ar": r.reason_ar}
                for r in recs if not r.allowed
            ][:3]
            opp["recommended_channel_ar"] = (
                best.channel if best else opp.get("recommended_channel_ar", "manual")
            )
            opp["channel_score"] = best.score if best else 0.0
            opp["channel_reason_ar"] = best.reason_ar if best else "—"
            opp["channel_blocked_reasons"] = blocked

        baseline["channel_orchestrator_active"] = True

        outputs = dict(sprint.day_outputs_json or {})
        outputs["day_2"] = baseline
        sprint.day_outputs_json = outputs
        sprint.current_day = max(sprint.current_day, 2)
        sprint.status = "day_2"
        proof_id = await _emit_day_proof(session, sprint, 2, "Opportunity Pack (channel-aware)")
        await session.commit()
        return {
            "sprint_id": sprint_id,
            "day": 2,
            "output": baseline,
            "proof_event_id": proof_id,
            "status": sprint.status,
        }


@router.post("/{sprint_id}/messages/generate")
async def day_3(sprint_id: str) -> dict[str, Any]:
    """Day 3 — Message Pack. Tries LLM-personalized drafts FIRST (using
    Company Brain + saudi-tone system prompt + assert_safe), falls back
    to deterministic templates per-message on any failure.

    Each message in the output carries `llm_used` and `provider` so the
    UI / audit log can show where the personalization came from."""
    from auto_client_acquisition.intelligence.smart_drafter import get_drafter

    async with get_session() as session:
        sprint = await _load_or_404(session, sprint_id)
        brain = await _load_customer_brain(session, sprint.customer_id)

        # Start with the deterministic baseline (always safe)
        baseline = generate_message_pack(brain)

        drafter = get_drafter()
        smart_messages: list[dict[str, Any]] = []
        llm_count = 0
        for i, template_text in enumerate(baseline["first_messages_ar"]):
            r = await drafter.draft_outreach_message(
                brain,
                prospect_hint=f"Prospect #{i+1} for {brain.get('company_name','—')}",
                fallback=template_text,
            )
            if r.used_llm:
                llm_count += 1
            smart_messages.append({
                "n": i + 1,
                "text": r.text,
                "llm_used": r.used_llm,
                "provider": r.provider,
                "fallback_reason": r.fallback_reason,
                "safety_passed": r.safety_passed,
                "approval_required": True,
            })

        # Replace the simple list with annotated dicts; also keep a
        # `text-only` array for backwards-compat consumers.
        baseline["first_messages_ar"] = [m["text"] for m in smart_messages]
        baseline["first_messages_annotated"] = smart_messages
        baseline["llm_personalized_count"] = llm_count
        baseline["fallback_count"] = len(smart_messages) - llm_count

        outputs = dict(sprint.day_outputs_json or {})
        outputs["day_3"] = baseline
        sprint.day_outputs_json = outputs
        sprint.current_day = max(sprint.current_day, 3)
        sprint.status = "day_3"
        proof_id = await _emit_day_proof(session, sprint, 3, "Message Pack (LLM-enhanced)")
        await session.commit()
        return {
            "sprint_id": sprint_id,
            "day": 3,
            "output": baseline,
            "proof_event_id": proof_id,
            "status": sprint.status,
        }


@router.post("/{sprint_id}/meeting-prep")
async def day_4(sprint_id: str) -> dict[str, Any]:
    """Day 4 — Meeting Prep. Script + agenda stay deterministic
    (operationally critical). Discovery questions get 1-2 Brain-aware
    items appended via SmartDrafter."""
    from auto_client_acquisition.intelligence.smart_drafter import get_drafter

    async with get_session() as session:
        sprint = await _load_or_404(session, sprint_id)
        brain = await _load_customer_brain(session, sprint.customer_id)
        baseline = generate_meeting_prep(brain)

        drafter = get_drafter()
        prompt = (
            f"الشركة: {brain.get('company_name','—')} في {brain.get('sector','—')}.\n"
            f"عرضهم: {brain.get('offer_ar','—')}.\n"
            f"العميل المثالي: {brain.get('ideal_customer_ar','—')}.\n\n"
            f"اقترح سؤالين فقط (سؤال واحد لكل سطر) لاجتماع discovery — "
            f"يكشفان pain حقيقي مرتبط بهذا العرض. ليست عامة. عربي. "
            f"ممنوع 'نضمن' أو وعود."
        )
        r = await drafter._safe_run(
            "REASONING", prompt, max_tokens=200, temperature=0.6,
            fallback="",
        )

        # Append the LLM questions if successful
        smart_questions: list[str] = []
        if r.used_llm and r.text:
            for line in r.text.split("\n"):
                line = line.strip().lstrip("- ").lstrip("•").strip()
                if line and "?" in line or line.endswith("؟"):
                    smart_questions.append(line)

        baseline["discovery_questions_ar"] = (
            list(baseline.get("discovery_questions_ar", [])) + smart_questions[:2]
        )
        baseline["llm_questions_added"] = len(smart_questions[:2])
        baseline["llm_provider"] = r.provider
        baseline["llm_safety_passed"] = r.safety_passed

        outputs = dict(sprint.day_outputs_json or {})
        outputs["day_4"] = baseline
        sprint.day_outputs_json = outputs
        sprint.current_day = max(sprint.current_day, 4)
        sprint.status = "day_4"
        proof_id = await _emit_day_proof(session, sprint, 4, "Meeting Prep (LLM-enhanced)")
        await session.commit()
        return {
            "sprint_id": sprint_id,
            "day": 4,
            "output": baseline,
            "proof_event_id": proof_id,
            "status": sprint.status,
        }


@router.get("/{sprint_id}/review")
async def day_5(sprint_id: str) -> dict[str, Any]:
    """Day 5 — Pipeline Review. Pulls customer's current prospects."""
    async with get_session() as session:
        sprint = await _load_or_404(session, sprint_id)
        brain = await _load_customer_brain(session, sprint.customer_id)
        # Prospects associated with this customer (advanced through to closed_won)
        # OR in active stages — for the demo we surface all customer's prospects.
        rows = list((await session.execute(
            select(ProspectRecord).where(ProspectRecord.customer_id == sprint.customer_id)
        )).scalars().all())
        prospects_data = [
            {
                "id": p.id,
                "company": p.company,
                "status": p.status,
                "last_reply_at": p.last_reply_at.isoformat() if p.last_reply_at else None,
                "blocked_channels": list(getattr(p, "blocked_channels", []) or []),
                "risk_reason": getattr(p, "risk_reason", None),
            }
            for p in rows
        ]
        output = generate_pipeline_review(brain, prospects_data=prospects_data)
        outputs = dict(sprint.day_outputs_json or {})
        outputs["day_5"] = output
        sprint.day_outputs_json = outputs
        sprint.current_day = max(sprint.current_day, 5)
        sprint.status = "day_5"
        proof_id = await _emit_day_proof(session, sprint, 5, "Pipeline Review")
        await session.commit()
        return {
            "sprint_id": sprint_id,
            "day": 5,
            "output": output,
            "proof_event_id": proof_id,
        }


@router.post("/{sprint_id}/proof/draft")
async def day_6(sprint_id: str) -> dict[str, Any]:
    """Day 6 — Proof Pack Draft. Aggregates customer's RWU counts."""
    async with get_session() as session:
        sprint = await _load_or_404(session, sprint_id)
        brain = await _load_customer_brain(session, sprint.customer_id)

        # Aggregate proof events for this customer
        events = list((await session.execute(
            select(ProofEventRecord).where(ProofEventRecord.customer_id == sprint.customer_id)
        )).scalars().all())
        counts: dict[str, int] = {}
        revenue_total = 0.0
        risks_blocked: list[dict[str, Any]] = []
        pending_approvals = 0
        for e in events:
            counts[e.unit_type] = counts.get(e.unit_type, 0) + 1
            if e.unit_type == "risk_blocked":
                risks_blocked.append({
                    "label_ar": e.label_ar,
                    "risk_level": e.risk_level,
                })
            if e.approval_required and not e.approved:
                pending_approvals += 1
            if not e.approval_required or e.approved:
                revenue_total += float(e.revenue_impact_sar or 0)
        counts["pending_approvals"] = pending_approvals

        output = generate_proof_draft(
            brain,
            counts=counts,
            risks_blocked=risks_blocked,
            revenue_impact_sar=revenue_total,
        )

        # LLM executive summary — fallback to deterministic 1-liner
        from auto_client_acquisition.intelligence.smart_drafter import get_drafter
        drafter = get_drafter()
        det_summary = (
            f"خلال ٧ أيام: {counts.get('opportunity_created',0)} فرصة، "
            f"{counts.get('draft_created',0)} مسودة، "
            f"{counts.get('risk_blocked',0)} مخاطرة محظورة، "
            f"أثر إيرادي تقديري {revenue_total:.0f} SAR."
        )
        summary_prompt = (
            f"اكتب فقرة واحدة (3-4 أسطر) كـ executive summary لـ Proof Pack.\n"
            f"الشركة: {brain.get('company_name','—')}.\n"
            f"وحدات أُنجزت: {counts.get('opportunity_created',0)} فرصة، "
            f"{counts.get('draft_created',0)} مسودة، "
            f"{counts.get('meeting_drafted',0)} اجتماع.\n"
            f"مخاطر تم منعها: {counts.get('risk_blocked',0)}.\n"
            f"أثر إيرادي تقديري: {revenue_total:.0f} SAR.\n"
            f"النبرة: محترفة سعودية. لا 'نضمن' ولا 'guaranteed'.\n"
            f"اذكر الخطوة التالية المنطقية في الجملة الأخيرة."
        )
        r = await drafter._safe_run(
            "SUMMARY", summary_prompt,
            max_tokens=300, temperature=0.5,
            fallback=det_summary,
        )
        output["executive_summary_ar"] = r.text or det_summary
        output["llm_enhanced"] = bool(r.used_llm)
        output["llm_provider"] = r.provider
        output["llm_safety_passed"] = r.safety_passed

        outputs = dict(sprint.day_outputs_json or {})
        outputs["day_6"] = output
        sprint.day_outputs_json = outputs
        sprint.current_day = max(sprint.current_day, 6)
        sprint.status = "day_6"
        proof_id = await _emit_day_proof(session, sprint, 6, "Proof Pack Draft (LLM-enhanced)")
        await session.commit()
        return {
            "sprint_id": sprint_id,
            "day": 6,
            "output": output,
            "proof_event_id": proof_id,
        }


@router.post("/{sprint_id}/close-out")
async def day_7(sprint_id: str, body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Day 7 — Final Proof Pack URL + Growth OS upsell offer."""
    async with get_session() as session:
        sprint = await _load_or_404(session, sprint_id)
        brain = await _load_customer_brain(session, sprint.customer_id)
        proof_draft = (sprint.day_outputs_json or {}).get("day_6")
        pack_url = (
            f"/api/v1/proof-ledger/customer/{sprint.customer_id}/pack.html"
        )
        output = generate_close_out(brain, proof_draft=proof_draft, pack_url=pack_url)
        outputs = dict(sprint.day_outputs_json or {})
        outputs["day_7"] = output
        sprint.day_outputs_json = outputs
        sprint.current_day = 7
        sprint.status = "completed"
        sprint.completed_at = _now()
        proof_id = await _emit_day_proof(session, sprint, 7, "Final Proof Pack delivered")
        sprint.proof_pack_event_id = proof_id
        await session.commit()
        log.info(
            "sprint_completed sprint_id=%s customer_id=%s",
            sprint_id, sprint.customer_id,
        )
        return {
            "sprint_id": sprint_id,
            "day": 7,
            "status": "completed",
            "output": output,
            "proof_event_id": proof_id,
        }
