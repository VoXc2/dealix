"""Revenue Ops Machine — the six ops handlers.

Each handler takes a :class:`FunnelContext` plus a payload, advances the funnel
through the single :func:`advance` chokepoint (via ``ctx.transition_to``), and
returns a :class:`HandlerResult` describing the new state, the drafts to queue,
and the proof events to record.

Handlers do NO database I/O and NEVER send anything. The router persists the
context, gates+queues the drafts, and records the proof events.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.proof_ledger.schemas import ProofEvent, ProofEventType
from auto_client_acquisition.revenue_ops_machine.abcd_scorer import (
    abcd_to_funnel_state,
    recommend_offer,
    score_form,
)
from auto_client_acquisition.revenue_ops_machine.context import FunnelContext
from auto_client_acquisition.revenue_ops_machine.drafts import DraftSpec
from auto_client_acquisition.revenue_ops_machine.funnel_state import (
    FunnelState,
    RevenueOpsMachineError,
)


@dataclass
class HandlerResult:
    """The output of an ops handler — what the router must persist."""

    next_state: FunnelState
    drafts: list[DraftSpec] = field(default_factory=list)
    proof_events: list[ProofEvent] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _proof(
    ctx: FunnelContext,
    event_type: ProofEventType,
    summary_en: str,
    summary_ar: str,
    *,
    risk_level: str = "low",
) -> ProofEvent:
    return ProofEvent(
        event_type=event_type,
        summary_en=summary_en,
        summary_ar=summary_ar,
        evidence_source="revenue_ops_machine",
        risk_level=risk_level,
        payload={"lead_id": ctx.lead_id, "funnel_state": str(ctx.funnel_state)},
    )


# ── 1. Lead Capture Ops ──────────────────────────────────────────────────────
def lead_capture_ops(ctx: FunnelContext, form: dict[str, Any]) -> HandlerResult:
    """Form submission -> scored lead, recommended offer, founder + follow-up drafts."""
    result = score_form(form)
    ctx.abcd_score = result.score
    ctx.abcd_grade = result.grade
    ctx.abcd_signals = result.signals.to_dict()
    ctx.recommended_offer_id = recommend_offer(result.grade)

    ctx.transition_to(FunnelState.lead_captured)

    company = str(form.get("company") or form.get("company_name") or "a new lead")
    drafts = [
        DraftSpec(
            kind="founder_notification",
            channel="internal",
            message=(
                f"New lead captured: {company}. "
                f"A/B/C/D grade {result.grade} (score {result.score}). "
                f"Recommended offer: {ctx.recommended_offer_id}. "
                "Review and approve the follow-up draft."
            ),
        ),
        DraftSpec(
            kind="follow_up",
            channel="email",
            message=(
                f"Thank you for your interest in the Dealix governed revenue "
                f"diagnostic. Based on what you shared about {company}, we can "
                "map where revenue workflows, data quality, and AI usage create "
                "risk or missed value. Reply to book a short diagnostic review."
            ),
        ),
    ]
    proof_events = [
        _proof(
            ctx,
            ProofEventType.LEAD_INTAKE,
            f"Lead captured and scored grade {result.grade}.",
            f"تم استلام العميل المحتمل وتصنيفه ضمن الفئة {result.grade}.",
        )
    ]
    return HandlerResult(
        ctx.funnel_state,
        drafts,
        proof_events,
        notes=[f"grade={result.grade}", f"score={result.score}"],
    )


# ── 2. Qualification Ops ─────────────────────────────────────────────────────
def qualification_ops(ctx: FunnelContext) -> HandlerResult:
    """Route a captured lead to qualified_A / qualified_B / nurture by A/B/C/D grade."""
    if not ctx.abcd_grade:
        raise RevenueOpsMachineError("lead has no A/B/C/D grade; run lead capture first")
    target = abcd_to_funnel_state(ctx.abcd_grade)
    ctx.transition_to(target)

    drafts = [
        DraftSpec(
            kind="qualification_summary",
            channel="internal",
            message=(
                f"Lead qualified as {ctx.funnel_state} "
                f"(grade {ctx.abcd_grade}). Recommended offer: "
                f"{ctx.recommended_offer_id}."
            ),
        )
    ]
    return HandlerResult(ctx.funnel_state, drafts, [], notes=[f"qualified={ctx.funnel_state}"])


# ── 3. Booking Ops ───────────────────────────────────────────────────────────
def booking_ops(ctx: FunnelContext, step: str) -> HandlerResult:
    """``step="book"`` -> meeting_booked (+ booking link & brief drafts);
    ``step="done"`` -> meeting_done."""
    step = (step or "").strip().lower()
    if step == "book":
        ctx.transition_to(FunnelState.meeting_booked)
        drafts = [
            DraftSpec(
                kind="booking_link",
                channel="email",
                message=(
                    "Here is a link to book a 20-minute diagnostic review at a "
                    "time that suits you. We will walk through one revenue "
                    "workflow and where it can be made more governed."
                ),
            ),
            DraftSpec(
                kind="meeting_brief",
                channel="internal",
                message=(
                    f"Meeting brief — grade {ctx.abcd_grade} lead. "
                    f"Recommended offer {ctx.recommended_offer_id}. "
                    "Cover: workflow, CRM/source clarity, AI usage, approval "
                    "process, then demo and diagnostic next step."
                ),
            ),
        ]
        return HandlerResult(ctx.funnel_state, drafts, [])
    if step == "done":
        ctx.transition_to(FunnelState.meeting_done)
        return HandlerResult(ctx.funnel_state, [], [], notes=["meeting completed"])
    raise RevenueOpsMachineError(f"unknown booking step: {step!r} (use book|done)")


# ── 4. Sales Call Ops ────────────────────────────────────────────────────────
def sales_call_ops(ctx: FunnelContext) -> HandlerResult:
    """After the call: move meeting_done -> scope_requested with a discovery brief."""
    ctx.transition_to(FunnelState.scope_requested)
    drafts = [
        DraftSpec(
            kind="discovery_prep",
            channel="internal",
            message=(
                "Discovery recap: open the problem, map one workflow, check "
                "CRM/source clarity, AI usage and approval boundaries, then "
                "agree the diagnostic scope as the next step."
            ),
        )
    ]
    return HandlerResult(ctx.funnel_state, drafts, [], notes=["scope requested"])


# ── 5. Scope + Invoice Ops ───────────────────────────────────────────────────
def scope_invoice_ops(ctx: FunnelContext, step: str) -> HandlerResult:
    """``step`` is ``scope`` -> ``invoice`` -> ``paid``. The funnel graph and the
    milestone guard both forbid an invoice before a scope."""
    step = (step or "").strip().lower()
    if step == "scope":
        ctx.transition_to(FunnelState.scope_sent)
        drafts = [
            DraftSpec(
                kind="scope_doc",
                channel="email",
                message=(
                    "Attached is the proposed scope for the governed revenue "
                    "diagnostic: workflow map, source/approval risk notes, top "
                    "decisions, and a Proof Pack. Estimated outcomes are not "
                    "guaranteed."
                ),
            )
        ]
        return HandlerResult(ctx.funnel_state, drafts, [])
    if step == "invoice":
        ctx.transition_to(FunnelState.invoice_sent)
        drafts = [
            DraftSpec(
                kind="invoice",
                channel="email",
                message=(
                    "Attached is the invoice for the agreed diagnostic scope. "
                    "Payment is handled via a secure external payment link."
                ),
            ),
            DraftSpec(
                kind="payment_link",
                channel="email",
                message=(
                    "Secure payment link for the agreed diagnostic. Delivery "
                    "begins once payment is confirmed."
                ),
            ),
        ]
        proof_events = [
            _proof(
                ctx,
                ProofEventType.INVOICE_PREPARED,
                "Invoice draft prepared for the agreed scope.",
                "تم تجهيز مسودة الفاتورة للنطاق المتفق عليه.",
            )
        ]
        return HandlerResult(ctx.funnel_state, drafts, proof_events)
    if step == "paid":
        ctx.transition_to(FunnelState.invoice_paid)
        drafts = [
            DraftSpec(
                kind="onboarding_form",
                channel="email",
                message=(
                    "Thank you — payment confirmed. Please complete the short "
                    "onboarding form so we can begin the diagnostic."
                ),
            )
        ]
        proof_events = [
            _proof(
                ctx,
                ProofEventType.PAYMENT_CONFIRMED,
                "Payment confirmed; delivery may begin.",
                "تم تأكيد الدفع؛ يمكن بدء التسليم.",
            )
        ]
        return HandlerResult(ctx.funnel_state, drafts, proof_events)
    raise RevenueOpsMachineError(f"unknown scope/invoice step: {step!r} (use scope|invoice|paid)")


# ── 6. Delivery + Proof Ops ──────────────────────────────────────────────────
def delivery_proof_ops(ctx: FunnelContext, step: str) -> HandlerResult:
    """``step`` is ``start`` -> ``proof`` -> ``upsell`` -> ``retainer``."""
    step = (step or "").strip().lower()
    if step == "start":
        ctx.transition_to(FunnelState.delivery_started)
        drafts = [
            DraftSpec(
                kind="delivery_kickoff",
                channel="email",
                message=(
                    "Delivery has started. We will share findings and an "
                    "initial Proof Pack at the review call."
                ),
            )
        ]
        proof_events = [
            _proof(
                ctx,
                ProofEventType.DELIVERY_STARTED,
                "Diagnostic delivery started.",
                "تم بدء تسليم التشخيص.",
            )
        ]
        return HandlerResult(ctx.funnel_state, drafts, proof_events)
    if step == "proof":
        ctx.transition_to(FunnelState.proof_pack_sent)
        drafts = [
            DraftSpec(
                kind="proof_pack_delivery",
                channel="email",
                message=(
                    "Your Proof Pack is ready: workflow map, source and "
                    "approval risks, revenue leakage points, and the top three "
                    "decisions. Let us review it together."
                ),
            )
        ]
        proof_events = [
            _proof(
                ctx,
                ProofEventType.PROOF_PACK_ASSEMBLED,
                "Proof Pack assembled.",
                "تم تجميع حزمة الإثبات.",
            ),
            _proof(
                ctx,
                ProofEventType.PROOF_PACK_SENT,
                "Proof Pack draft queued for founder approval.",
                "تم وضع مسودة حزمة الإثبات في قائمة الموافقة.",
            ),
        ]
        return HandlerResult(ctx.funnel_state, drafts, proof_events)
    if step == "upsell":
        ctx.transition_to(FunnelState.upsell_sprint)
        drafts = [
            DraftSpec(
                kind="upsell",
                channel="email",
                message=(
                    "Based on the Proof Pack, one workflow is worth a focused "
                    "sprint. Here is a draft scope for that next step."
                ),
            )
        ]
        proof_events = [
            _proof(
                ctx,
                ProofEventType.UPSELL_RECOMMENDED,
                "Sprint upsell recommended from Proof Pack findings.",
                "تمت التوصية بترقية إلى Sprint بناءً على نتائج حزمة الإثبات.",
            )
        ]
        return HandlerResult(ctx.funnel_state, drafts, proof_events)
    if step == "retainer":
        ctx.transition_to(FunnelState.retainer_candidate)
        drafts = [
            DraftSpec(
                kind="retainer_proposal",
                channel="email",
                message=(
                    "Following the sprint, here is a draft proposal for an "
                    "ongoing governed revenue ops retainer."
                ),
            )
        ]
        return HandlerResult(ctx.funnel_state, drafts, [], notes=["retainer candidate"])
    raise RevenueOpsMachineError(
        f"unknown delivery/proof step: {step!r} (use start|proof|upsell|retainer)"
    )


__all__ = [
    "HandlerResult",
    "lead_capture_ops",
    "qualification_ops",
    "booking_ops",
    "sales_call_ops",
    "scope_invoice_ops",
    "delivery_proof_ops",
]
