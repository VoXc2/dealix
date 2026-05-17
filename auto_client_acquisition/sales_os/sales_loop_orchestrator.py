"""Sales Loop Orchestrator — drives one lead end-to-end.

Loop:  lead -> score -> message draft -> founder approval -> conversation
            -> meeting -> scope -> invoice -> paid -> delivery -> proof pack.

This module ONLY stitches existing subsystems together. It owns no
business logic of its own:

* front half (intake/score/draft/approval) -> ``leadops_spine.run_pipeline``
* canonical stage machine + evidence rules -> ``revenue_pipeline`` pipeline
* every external-facing transition -> ``approval_center`` gate
* every transition -> ``auditability_os.record_event`` evidence
* invoice / payment -> ``payment_ops`` orchestrator
* scope document -> ``sales_os.proposal_renderer``
* proof pack -> ``proof_os`` ; reusable asset -> ``capital_os`` ; revenue -> ``value_os``

It NEVER sends anything externally and NEVER auto-confirms payment.
Autonomy level L3 (RECOMMEND): it drafts, advances internal stages, and
opens approval gates — a human resolves every external-facing action.
"""
from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.agent_os.agent_card import new_card
from auto_client_acquisition.agent_os.agent_registry import get_agent, register_agent
from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    approve as _approval_approve,
    get_default_approval_store,
    reject as _approval_reject,
)
from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    list_events,
    record_event,
)
from auto_client_acquisition.capital_os.asset_types import CapitalAssetType
from auto_client_acquisition.capital_os.capital_ledger import add_asset, list_assets
from auto_client_acquisition.leadops_spine.orchestrator import run_pipeline
from auto_client_acquisition.payment_ops.orchestrator import (
    confirm_payment,
    create_invoice_intent,
    kickoff_delivery,
    upload_manual_evidence,
)
from auto_client_acquisition.proof_os.proof_pack import (
    build_empty_proof_pack_v2,
    merge_proof_pack_v2,
)
from auto_client_acquisition.proof_os.proof_score import proof_pack_completeness_score
from auto_client_acquisition.revenue_pipeline.lead import Lead as RevenueLead
from auto_client_acquisition.revenue_pipeline.pipeline import get_default_pipeline
from auto_client_acquisition.revenue_pipeline.stage_policy import (
    PipelineStage,
    valid_transitions,
)
from auto_client_acquisition.value_os.value_ledger import add_event as value_add_event

AGENT_ID = "sales_loop_orchestrator"

_LEDGER_ENV = "DEALIX_SALES_LOOP_LEDGER_PATH"
_DEFAULT_LEDGER = "data/sales_loop_records.jsonl"

# Sources accepted by LeadOpsRecord.source (Literal). Anything else -> "manual".
_LEADOPS_SOURCES = frozenset(
    {"whatsapp", "form", "csv", "warm_intro", "google_places", "referral", "api", "manual"},
)

_ALLOWED_TOOLS = [
    "leadops_spine",
    "stage_policy",
    "approval_center",
    "audit_event",
    "payment_ops",
    "value_ledger",
    "capital_ledger",
    "booking_agent",
    "proposal_renderer",
]

# Extra inputs each target stage needs (surfaced by ``next_actions``).
_REQUIREMENTS: dict[str, list[str]] = {
    "commitment_received": ["commitment_evidence"],
    "payment_received": ["payment_evidence", "actual_amount_sar"],
}


class SalesLoopGateError(RuntimeError):
    """Raised when an open approval gate blocks the requested advance."""

    def __init__(self, approval_id: str, status: str | None) -> None:
        self.approval_id = approval_id
        self.status = status or "unknown"
        super().__init__(
            f"approval gate {approval_id} is {self.status}; "
            "resolve it before advancing the sales loop",
        )


class SalesLoopRecord(BaseModel):
    """Loop state envelope — placeholder-shaped, never carries PII."""

    model_config = ConfigDict(extra="forbid")

    loop_id: str
    customer_handle: str
    leadops_id: str | None = None
    revenue_lead_id: str | None = None
    stage: PipelineStage = "warm_intro_selected"
    source: str = "manual"
    sector: str = "tbd"
    region: str = "tbd"
    payment_id: str | None = None
    engagement_id: str | None = None
    booking_id: str | None = None
    booking_meta: dict[str, Any] | None = None
    proposal_markdown: str | None = None
    pending_approval_id: str | None = None
    history: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_registered() -> None:
    """Register the orchestrator's agent identity (non-negotiable #9)."""
    if get_agent(AGENT_ID) is not None:
        return
    try:
        register_agent(
            new_card(
                agent_id=AGENT_ID,
                name="Sales Loop Orchestrator",
                owner="founder",
                purpose=(
                    "Drive a lead end-to-end (lead -> score -> draft -> approval "
                    "-> conversation -> meeting -> scope -> invoice -> paid) by "
                    "sequencing existing agents and subsystems with stage "
                    "advancement, approval gates, and evidence logging."
                ),
                autonomy_level=AutonomyLevel.L3_RECOMMEND,
                allowed_tools=_ALLOWED_TOOLS,
                kill_switch_owner="founder",
                notes=(
                    "No-build orchestrator: stitches existing modules only. "
                    "Every external-facing transition opens an approval gate."
                ),
            ),
        )
    except ValueError:
        # Already registered by a concurrent caller — fine.
        pass


class SalesLoopOrchestrator:
    """Sequences existing modules into one governed lead-to-paid loop."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._records: dict[str, SalesLoopRecord] = {}

    # ── lifecycle ────────────────────────────────────────────────

    def start_loop(
        self,
        *,
        raw_payload: dict[str, Any],
        source: str = "manual",
        customer_handle: str,
    ) -> SalesLoopRecord:
        """Run the front half (leadops spine) and open the loop."""
        if not customer_handle or not customer_handle.strip():
            raise ValueError("customer_handle is required")
        _ensure_registered()

        loop_id = f"loop_{uuid.uuid4().hex[:10]}"
        leadops_source = source if source in _LEADOPS_SOURCES else "manual"
        leadops = run_pipeline(
            raw_payload=raw_payload,
            source=leadops_source,
            customer_handle=customer_handle,
        )

        sector = str(raw_payload.get("sector") or "tbd").strip() or "tbd"
        region = str(raw_payload.get("region") or "tbd").strip() or "tbd"

        # Mirror the lead into the revenue pipeline so the canonical stage
        # machine + evidence rules + /revenue-pipeline/summary stay accurate.
        pipeline = get_default_pipeline()
        lead = RevenueLead.make(slot_id=loop_id, sector=sector[:40], region=region)
        pipeline.add(lead)
        pipeline.advance(lead.id, "message_drafted")

        record = SalesLoopRecord(
            loop_id=loop_id,
            customer_handle=customer_handle,
            leadops_id=leadops.leadops_id,
            revenue_lead_id=lead.id,
            stage="message_drafted",
            source=source,
            sector=sector,
            region=region,
            pending_approval_id=None,
            history=[
                {
                    "stage": "message_drafted",
                    "at": _now().isoformat(),
                    "actor": AGENT_ID,
                    "note": f"leadops pipeline {leadops.leadops_id} "
                    f"(compliance={leadops.compliance_status})",
                },
            ],
        )

        record_event(
            customer_id=customer_handle,
            kind=AuditEventKind.AI_RUN,
            actor=AGENT_ID,
            engagement_id=loop_id,
            decision="lead_scored_and_drafted",
            policy_checked="leadops_compliance_gate",
            summary=f"sales loop {loop_id} started from leadops {leadops.leadops_id}",
            source_refs=[leadops.leadops_id],
        )

        # Front-half gate (#8): the first outbound message needs approval.
        # Prefer the spine's approval; otherwise open our own so the loop
        # is gated regardless of the spine's draft state.
        gate_id = leadops.approval_id
        if gate_id:
            record_event(
                customer_id=customer_handle,
                kind=AuditEventKind.APPROVAL,
                actor=AGENT_ID,
                engagement_id=loop_id,
                decision="draft_approval_opened",
                summary=f"outbound draft for loop {loop_id} awaiting founder approval",
                output_refs=[gate_id],
            )
        else:
            gate_id = self._open_gate(
                record,
                action_type="draft_email",
                summary_en="Approve the outbound first-touch message before it is sent.",
                summary_ar="الموافقة على رسالة التواصل الأولى قبل إرسالها.",
            )
        record = record.model_copy(update={"pending_approval_id": gate_id})

        self._save(record)
        return record

    async def advance(
        self,
        *,
        loop_id: str,
        target_stage: PipelineStage,
        actor: str,
        commitment_evidence: str = "",
        payment_evidence: str = "",
        actual_amount_sar: int | None = None,
        meeting_minutes: int = 30,
        invoice_method: str = "bank_transfer",
        reason: str = "",
    ) -> SalesLoopRecord:
        """Advance the loop one canonical stage, with gate + evidence."""
        record = self.get_loop(loop_id)
        if record is None:
            raise KeyError(f"unknown sales loop: {loop_id}")

        # ── gate check (non-negotiable #8) ──────────────────────
        if record.pending_approval_id:
            appr = get_default_approval_store().get(record.pending_approval_id)
            status = str(appr.status) if appr else None
            if status == "approved":
                record = record.model_copy(update={"pending_approval_id": None})
            else:
                raise SalesLoopGateError(record.pending_approval_id, status)

        # ── cheap pre-validation (avoid partial state) ──────────
        if target_stage == "payment_received":
            if len(payment_evidence.strip()) < 5:
                raise ValueError(
                    "payment_evidence must be a reference of at least 5 chars",
                )
            if not actual_amount_sar or actual_amount_sar <= 0:
                raise ValueError("actual_amount_sar must be > 0 for payment_received")

        # ── canonical stage transition (#stage machine + evidence) ──
        pipeline = get_default_pipeline()
        updated_lead = pipeline.advance(
            record.revenue_lead_id or "",
            target_stage,
            commitment_evidence=commitment_evidence,
            payment_evidence=payment_evidence,
            actual_amount_sar=actual_amount_sar,
        )
        new_stage: PipelineStage = updated_lead.stage

        updates: dict[str, Any] = {"stage": new_stage}
        new_gate: str | None = None

        # ── per-transition side effects ─────────────────────────
        if new_stage == "founder_sent_manually":
            self._evidence(
                record, AuditEventKind.OUTPUT_DELIVERED,
                "founder_sent_message_manually",
                "founder confirmed the outbound draft was sent manually",
            )
        elif new_stage == "replied":
            self._evidence(
                record, AuditEventKind.GOVERNANCE_DECISION, "prospect_replied",
                "inbound reply recorded; no external action taken",
            )
        elif new_stage == "diagnostic_requested":
            booking = await self._run_booking(record, meeting_minutes)
            updates["booking_id"] = booking.get("booking_id")
            updates["booking_meta"] = booking
            self._evidence(
                record, AuditEventKind.OUTPUT_DELIVERED, "meeting_booking_recorded",
                f"meeting booking via provider={booking.get('provider')}",
            )
            if booking.get("provider") in ("calendly", "google"):
                new_gate = self._open_gate(
                    record, action_type="follow_up_task",
                    summary_en="Approve sending the meeting invite/link to the prospect.",
                    summary_ar="الموافقة على إرسال رابط/دعوة الاجتماع للعميل المحتمل.",
                )
        elif new_stage == "diagnostic_delivered":
            diag = await self._run_diagnostic(record)
            self._evidence(
                record, AuditEventKind.AI_RUN, "diagnostic_prepared",
                f"diagnostic prepared via {diag.get('method')}",
            )
            self._evidence(
                record, AuditEventKind.OUTPUT_DELIVERED, "diagnostic_delivered",
                "diagnostic deliverable prepared for the prospect",
            )
            new_gate = self._open_gate(
                record, action_type="prepare_diagnostic",
                summary_en="Approve the diagnostic deliverable before it reaches the prospect.",
                summary_ar="الموافقة على مخرج التشخيص قبل وصوله للعميل المحتمل.",
            )
        elif new_stage == "pilot_offered":
            updates["proposal_markdown"] = self._render_scope(record)
            self._evidence(
                record, AuditEventKind.AI_RUN, "proposal_rendered",
                "scope/proposal rendered from sales_os proposal_renderer",
            )
            self._evidence(
                record, AuditEventKind.OUTPUT_DELIVERED, "proposal_offered",
                "scope/proposal prepared for the prospect",
            )
            new_gate = self._open_gate(
                record, action_type="draft_email",
                summary_en="Approve the scope/proposal document before it is sent.",
                summary_ar="الموافقة على وثيقة النطاق/العرض قبل إرسالها.",
            )
        elif new_stage == "commitment_received":
            self._evidence(
                record, AuditEventKind.GOVERNANCE_DECISION, "commitment_recorded",
                "written commitment recorded (verbal yes is not enough)",
                source_refs=[commitment_evidence],
            )
            new_gate = self._open_gate(
                record, action_type="payment_reminder",
                summary_en="Approve sending the invoice to the customer.",
                summary_ar="الموافقة على إرسال الفاتورة للعميل.",
            )
        elif new_stage == "payment_received":
            payment_id = self._run_payment(
                record, amount=int(actual_amount_sar or 0),
                evidence=payment_evidence.strip(), method=invoice_method,
                actor=actor,
            )
            updates["payment_id"] = payment_id
            value_add_event(
                customer_id=record.customer_handle,
                kind="sales_loop_payment",
                amount=float(actual_amount_sar or 0),
                tier="verified",
                source_ref=payment_evidence.strip(),
                notes=f"sales loop {loop_id} payment confirmed",
            )
            self._evidence(
                record, AuditEventKind.OUTPUT_DELIVERED, "payment_confirmed",
                f"payment confirmed by {actor}; revenue recorded in value ledger",
                source_refs=[payment_evidence.strip()],
                output_refs=[payment_id],
            )
        elif new_stage == "delivery_started":
            engagement_id = self._run_delivery_kickoff(record)
            updates["engagement_id"] = engagement_id
            self._evidence(
                record, AuditEventKind.OUTPUT_DELIVERED, "delivery_started",
                f"delivery kicked off (engagement {engagement_id})",
            )
        elif new_stage == "delivered":
            self._evidence(
                record, AuditEventKind.OUTPUT_DELIVERED, "delivery_completed",
                "engagement delivery completed",
            )
        elif new_stage == "proof_pack_delivered":
            engagement_id = record.engagement_id or loop_id
            self._assemble_proof_and_capital(record, engagement_id)
        elif new_stage == "upsell_offered":
            self._evidence(
                record, AuditEventKind.OUTPUT_DELIVERED, "upsell_offered",
                "next-best-offer (retainer) prepared for the customer",
            )
        elif new_stage == "closed_won":
            self._evidence(
                record, AuditEventKind.GOVERNANCE_DECISION, "closed_won",
                "sales loop closed won",
            )
        elif new_stage == "closed_lost":
            self._evidence(
                record, AuditEventKind.GOVERNANCE_DECISION, "closed_lost",
                f"sales loop closed lost: {reason or 'no reason given'}",
            )

        updates["pending_approval_id"] = new_gate
        updates["updated_at"] = _now()
        history = list(record.history)
        history.append(
            {
                "stage": new_stage,
                "at": _now().isoformat(),
                "actor": actor,
                "note": reason or "",
            },
        )
        updates["history"] = history
        record = record.model_copy(update=updates)
        self._save(record)
        return record

    def resolve_approval(
        self,
        *,
        loop_id: str,
        approval_id: str,
        decision: str,
        who: str,
        reason: str = "",
    ) -> SalesLoopRecord:
        """Approve/reject an approval and clear the loop gate when approved."""
        record = self.get_loop(loop_id)
        if record is None:
            raise KeyError(f"unknown sales loop: {loop_id}")
        if decision == "approve":
            appr = _approval_approve(approval_id, who)
        elif decision == "reject":
            appr = _approval_reject(approval_id, who, reason or "rejected by founder")
        else:
            raise ValueError("decision must be 'approve' or 'reject'")

        if (
            record.pending_approval_id == approval_id
            and str(appr.status) == "approved"
        ):
            record = record.model_copy(
                update={"pending_approval_id": None, "updated_at": _now()},
            )
            self._save(record)

        self._evidence(
            record, AuditEventKind.APPROVAL, f"approval_{decision}d",
            f"approval {approval_id} {decision}d by {who}",
            output_refs=[approval_id],
        )
        return record

    # ── reads ────────────────────────────────────────────────────

    def get_loop(self, loop_id: str) -> SalesLoopRecord | None:
        with self._lock:
            return self._records.get(loop_id)

    def list_loops(self, *, limit: int = 50) -> list[SalesLoopRecord]:
        with self._lock:
            rows = list(self._records.values())
        rows.sort(key=lambda r: r.created_at, reverse=True)
        return rows[: max(0, limit)]

    def next_actions(self, loop_id: str) -> dict[str, Any]:
        record = self.get_loop(loop_id)
        if record is None:
            raise KeyError(f"unknown sales loop: {loop_id}")
        transitions = sorted(valid_transitions(record.stage))
        return {
            "loop_id": loop_id,
            "current_stage": record.stage,
            "valid_transitions": transitions,
            "gate_open": bool(record.pending_approval_id),
            "pending_approval_id": record.pending_approval_id,
            "requirements": {t: _REQUIREMENTS.get(t, []) for t in transitions},
        }

    # ── side-effect helpers ──────────────────────────────────────

    async def _run_booking(
        self, record: SalesLoopRecord, meeting_minutes: int,
    ) -> dict[str, Any]:
        """Invoke the existing BookingAgent; degrade to manual on any error."""
        try:
            from auto_client_acquisition.agents.booking import BookingAgent

            result = await BookingAgent().run(
                lead=self._intake_lead(record), meeting_minutes=meeting_minutes,
            )
            return result.to_dict()
        except Exception as exc:  # noqa: BLE001 — orchestrator must stay headless
            return {
                "booking_id": f"bkg_manual_{record.loop_id}",
                "provider": "manual",
                "link": None,
                "scheduled_at": None,
                "meeting_minutes": meeting_minutes,
                "success": False,
                "reason": f"booking_unavailable:{type(exc).__name__}",
            }

    async def _run_diagnostic(self, record: SalesLoopRecord) -> dict[str, Any]:
        """Invoke the existing QualificationAgent; degrade gracefully."""
        try:
            from auto_client_acquisition.agents.qualification import QualificationAgent

            result = await QualificationAgent().run(lead=self._intake_lead(record))
            return {
                "method": "qualification_agent",
                "bant_score": result.bant_score,
                "questions": len(result.questions),
            }
        except Exception as exc:  # noqa: BLE001 — orchestrator must stay headless
            return {"method": f"recorded:{type(exc).__name__}"}

    def _render_scope(self, record: SalesLoopRecord) -> str:
        """Render the scope/proposal via the existing sales_os renderer."""
        from auto_client_acquisition.sales_os.proposal_renderer import (
            ProposalContext,
            render_proposal,
        )

        return render_proposal(
            ProposalContext(
                customer_name=record.customer_handle,
                customer_handle=record.customer_handle,
                sector=record.sector or "tbd",
                city=record.region or "tbd",
                engagement_id=record.loop_id,
            ),
        )

    def _run_payment(
        self,
        record: SalesLoopRecord,
        *,
        amount: int,
        evidence: str,
        method: str,
        actor: str,
    ) -> str:
        """invoice intent -> manual evidence -> founder confirmation."""
        method_norm = method if method in (
            "moyasar_test", "bank_transfer", "cash_in_person", "manual_other",
        ) else "bank_transfer"
        intent = create_invoice_intent(
            customer_handle=record.customer_handle,
            amount_sar=float(amount),
            method=method_norm,  # type: ignore[arg-type]
            service_session_id=record.loop_id,
        )
        uploaded, msg = upload_manual_evidence(
            payment_id=intent.payment_id, evidence_reference=evidence,
        )
        if uploaded is None:
            raise ValueError(f"payment evidence upload failed: {msg}")
        confirmed, msg = confirm_payment(
            payment_id=intent.payment_id, confirmed_by=actor,
        )
        if confirmed is None:
            raise ValueError(f"payment confirmation failed: {msg}")
        self._evidence(
            record, AuditEventKind.GOVERNANCE_DECISION, "invoice_intent_created",
            f"invoice intent {intent.invoice_intent_id} created (method={method_norm})",
            output_refs=[intent.payment_id],
        )
        return intent.payment_id

    def _run_delivery_kickoff(self, record: SalesLoopRecord) -> str:
        """Kick off delivery; the kickoff id becomes the engagement id."""
        if record.payment_id:
            rec, msg = kickoff_delivery(payment_id=record.payment_id)
            if rec is None:
                raise ValueError(f"delivery kickoff failed: {msg}")
            return rec.delivery_kickoff_id or record.loop_id
        return record.loop_id

    def _assemble_proof_and_capital(
        self, record: SalesLoopRecord, engagement_id: str,
    ) -> None:
        """Produce the Proof Pack (#10) and register a Capital Asset (#11)."""
        proof = merge_proof_pack_v2(
            build_empty_proof_pack_v2(),
            {
                "executive_summary": (
                    f"Sales loop {record.loop_id} completed end-to-end through "
                    "the governed lead-to-paid pipeline."
                ),
                "problem": (
                    "Lead-to-paid flow lacked a single governed orchestration "
                    "with evidence and approval gates at every transition."
                ),
                "work_completed": (
                    "Lead scored and drafted, founder-sent, reply recorded, "
                    "meeting booked, diagnostic delivered, scope offered, "
                    "commitment and payment confirmed, delivery kicked off."
                ),
                "outputs": (
                    f"Scope/proposal rendered; payment {record.payment_id}; "
                    f"engagement {engagement_id}."
                ),
                "governance_decisions": (
                    "Every external-facing transition routed through the "
                    "approval center before proceeding."
                ),
                "value_metrics": (
                    f"Verified revenue recorded in the value ledger for "
                    f"{record.customer_handle}."
                ),
                "recommended_next_step": (
                    "Offer the managed revenue ops retainer (upsell stage)."
                ),
                "capital_assets_created": (
                    "Reusable sales-loop proof example registered in the "
                    "capital ledger."
                ),
            },
        )
        score = proof_pack_completeness_score(proof)
        self._evidence(
            record, AuditEventKind.PROOF_PACK_ASSEMBLED,
            f"proof_pack_score_{score}",
            f"proof pack assembled for loop {record.loop_id} (score {score}/100)",
        )
        asset = add_asset(
            customer_id=record.customer_handle,
            engagement_id=engagement_id,
            asset_type=CapitalAssetType.PROOF_EXAMPLE,
            owner=record.customer_handle,
            asset_ref=record.loop_id,
            notes=f"sales loop {record.loop_id} proof example",
        )
        self._evidence(
            record, AuditEventKind.GOVERNANCE_DECISION, "capital_asset_registered",
            f"reusable capital asset {asset.asset_id} registered for "
            f"engagement {engagement_id}",
            output_refs=[asset.asset_id],
        )

    def _intake_lead(self, record: SalesLoopRecord) -> Any:
        """Build a PII-free intake.Lead for the headless back-half agents."""
        from auto_client_acquisition.agents.intake import Lead as IntakeLead
        from auto_client_acquisition.agents.intake import LeadSource

        src = record.source if record.source in {s.value for s in LeadSource} else "manual"
        return IntakeLead(
            id=record.revenue_lead_id or record.loop_id,
            source=LeadSource(src),
            sector=record.sector,
            region=record.region,
            locale="ar",
        )

    # ── gate + evidence + persistence ────────────────────────────

    def _open_gate(
        self,
        record: SalesLoopRecord,
        *,
        action_type: str,
        summary_en: str,
        summary_ar: str,
    ) -> str:
        """Open an approval-center gate; returns the new approval id."""
        req = ApprovalRequest(
            object_type="sales_loop",
            object_id=record.loop_id,
            action_type=action_type,
            action_mode="approval_required",
            channel="dashboard",
            summary_ar=summary_ar,
            summary_en=summary_en,
            risk_level="medium",
            customer_id=record.customer_handle,
            lead_id=record.revenue_lead_id,
            proof_impact=f"sales_loop:{record.loop_id}",
        )
        created = get_default_approval_store().create(req)
        self._evidence(
            record, AuditEventKind.APPROVAL, f"gate_opened:{action_type}",
            f"approval gate {created.approval_id} opened ({action_type})",
            output_refs=[created.approval_id],
        )
        return created.approval_id

    def _evidence(
        self,
        record: SalesLoopRecord,
        kind: AuditEventKind,
        decision: str,
        summary: str,
        *,
        source_refs: list[str] | None = None,
        output_refs: list[str] | None = None,
    ) -> None:
        record_event(
            customer_id=record.customer_handle,
            kind=kind,
            actor=AGENT_ID,
            engagement_id=record.loop_id,
            decision=decision,
            policy_checked="sales_loop_governance",
            summary=summary,
            source_refs=[r for r in (source_refs or []) if r],
            output_refs=[r for r in (output_refs or []) if r],
        )

    def _save(self, record: SalesLoopRecord) -> None:
        with self._lock:
            self._records[record.loop_id] = record
        self._persist(record)

    def _persist(self, record: SalesLoopRecord) -> None:
        path = _ledger_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(record.model_dump_json() + "\n")
        from auto_client_acquisition.persistence.operational_stream_mirror import (
            mirror_append,
        )

        mirror_append(
            stream_id="sales_loop_records_jsonl",
            payload=record.model_dump(mode="json"),
            event_id=record.loop_id,
        )

    def audit_trail(self, loop_id: str, *, limit: int = 200) -> list[dict[str, Any]]:
        """Evidence events recorded for this loop (filtered by engagement)."""
        record = self.get_loop(loop_id)
        if record is None:
            raise KeyError(f"unknown sales loop: {loop_id}")
        events = list_events(customer_id=record.customer_handle, limit=limit)
        return [e.to_dict() for e in events if e.engagement_id == loop_id]


def _ledger_path() -> Path:
    raw = os.environ.get(_LEDGER_ENV, _DEFAULT_LEDGER)
    p = Path(raw)
    if not p.is_absolute():
        p = Path(__file__).resolve().parent.parent.parent / p
    return p


_DEFAULT: SalesLoopOrchestrator | None = None


def get_default_sales_loop_orchestrator() -> SalesLoopOrchestrator:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = SalesLoopOrchestrator()
    return _DEFAULT


def clear_for_test() -> None:
    """Test-only — wipe in-memory loop records and truncate the ledger."""
    global _DEFAULT
    _DEFAULT = SalesLoopOrchestrator()
    path = _ledger_path()
    if path.exists():
        path.write_text("", encoding="utf-8")


__all__ = [
    "AGENT_ID",
    "SalesLoopGateError",
    "SalesLoopOrchestrator",
    "SalesLoopRecord",
    "clear_for_test",
    "get_default_sales_loop_orchestrator",
]
