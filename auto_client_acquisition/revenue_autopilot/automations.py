"""Revenue Autopilot — the 10 automation hooks.

Each automation:
  - mutates the engagement's funnel stage (where the stage changes),
  - logs an append-only EvidenceEvent,
  - produces DRAFTS only — it never executes an external send,
  - routes every external / sensitive action through the Approval
    Command Center (``approval_center.create_approval``).

Three governance tiers (founder doctrine):
  - Autopilot         → internal, fully automated.
  - Copilot           → produces a draft / recommendation.
  - Founder Approval  → queued in the approval center, never auto-executed.

Doctrine: docs/REVENUE_AUTOPILOT.md §6.
"""
from __future__ import annotations

from collections.abc import Callable

from auto_client_acquisition.approval_center import create_approval
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.revenue_autopilot.funnel import (
    FunnelStage,
    advance_stage,
)
from auto_client_acquisition.revenue_autopilot.lead_scorer import (
    LeadScore,
    score_lead,
)
from auto_client_acquisition.revenue_autopilot.records import (
    AutomationResult,
    AutopilotEngagement,
    DraftRef,
    EvidenceEvent,
    StageTransition,
)


def _recommend_tier(score: LeadScore | None) -> str:
    """Recommend a diagnostic price tier from the lead score (deterministic)."""
    points = score.points if score else 0
    if points >= 16:
        return "diagnostic_executive_15000"
    if points >= 12:
        return "diagnostic_standard_9999"
    return "diagnostic_starter_4999"


class _Run:
    """Accumulates what one automation run produced."""

    def __init__(self, engagement: AutopilotEngagement, automation: str) -> None:
        self.eng = engagement
        self.automation = automation
        self.stage_before: FunnelStage = engagement.current_stage
        self.draft_ids: list[str] = []
        self.approval_ids: list[str] = []
        self.event_ids: list[str] = []

    def advance(self, target: FunnelStage) -> None:
        """Move the funnel forward — raises ValueError on an illegal hop."""
        new_stage = advance_stage(self.eng.current_stage, target)
        self.eng.stage_history.append(StageTransition(
            from_stage=self.eng.current_stage,
            to_stage=new_stage,
            automation=self.automation,
        ))
        self.eng.current_stage = new_stage

    def log(self, kind: str, payload: dict | None = None) -> None:
        """Append an evidence event."""
        event = EvidenceEvent(
            engagement_id=self.eng.engagement_id,
            kind=kind,
            payload=payload or {},
        )
        self.eng.evidence_events.append(event)
        self.event_ids.append(event.event_id)

    def draft(
        self,
        *,
        action_type: str,
        summary_en: str,
        summary_ar: str,
        queue_approval: bool,
        action_mode: str = "draft_only",
    ) -> DraftRef:
        """Produce a draft; optionally queue it for founder approval."""
        ref = DraftRef(
            action_type=action_type,
            action_mode=action_mode,
            summary_en=summary_en,
            summary_ar=summary_ar,
        )
        if queue_approval:
            approval = create_approval(ApprovalRequest(
                object_type="autopilot_engagement",
                object_id=self.eng.engagement_id,
                action_type=action_type,
                action_mode=action_mode,
                summary_en=summary_en,
                summary_ar=summary_ar,
            ))
            ref.approval_id = approval.approval_id
            self.eng.approval_ids.append(approval.approval_id)
            self.approval_ids.append(approval.approval_id)
        self.eng.drafts.append(ref)
        self.draft_ids.append(ref.draft_id)
        return ref

    def result(self, notes_en: str, notes_ar: str) -> AutomationResult:
        return AutomationResult(
            automation=self.automation,
            engagement_id=self.eng.engagement_id,
            stage_before=self.stage_before,
            stage_after=self.eng.current_stage,
            draft_ids=self.draft_ids,
            approval_ids=self.approval_ids,
            evidence_event_ids=self.event_ids,
            notes_en=notes_en,
            notes_ar=notes_ar,
        )


# ── Automation 1 — Lead Capture ───────────────────────────────────────
def automation_1_lead_capture(
    engagement: AutopilotEngagement, payload: dict
) -> AutomationResult:
    """Score the lead, assign a funnel tier, draft a first response."""
    run = _Run(engagement, "lead_capture")
    score = score_lead(engagement.signals)
    engagement.lead_score = score
    run.advance(score.tier)
    run.log("form_submitted", {"points": score.points, "tier": score.tier})
    run.draft(
        action_type="draft_email",
        action_mode="approval_required",
        summary_en="First-response email draft for the new lead.",
        summary_ar="مسودة رد أول على العميل المحتمل الجديد.",
        queue_approval=True,
    )
    return run.result(
        notes_en=f"Lead scored {score.points} → {score.tier}.",
        notes_ar=f"تم تقييم العميل بـ{score.points} نقطة → {score.tier}.",
    )


# ── Automation 2 — Qualified Lead ─────────────────────────────────────
def automation_2_qualified_lead(
    engagement: AutopilotEngagement, payload: dict
) -> AutomationResult:
    """Draft a booking email + meeting brief for a qualified_A lead."""
    if engagement.current_stage != "qualified_A":
        raise ValueError("automation 'qualified_lead' requires stage qualified_A")
    run = _Run(engagement, "qualified_lead")
    run.log("qualified_lead_actioned")
    run.draft(
        action_type="draft_email",
        action_mode="approval_required",
        summary_en="Personalized booking-link email for the qualified lead.",
        summary_ar="بريد دعوة لحجز موعد مخصّص للعميل المؤهَّل.",
        queue_approval=True,
    )
    run.draft(
        action_type="prepare_diagnostic",
        summary_en="Internal meeting brief for the founder.",
        summary_ar="ملخص داخلي للاجتماع للمؤسس.",
        queue_approval=False,
    )
    return run.result(
        notes_en="Booking email queued for approval; meeting brief drafted.",
        notes_ar="تم وضع بريد الحجز في قائمة الموافقة وإعداد ملخص الاجتماع.",
    )


# ── Automation 3 — Proof Pack Request ─────────────────────────────────
def automation_3_proof_pack_request(
    engagement: AutopilotEngagement, payload: dict
) -> AutomationResult:
    """Log a proof-pack request and schedule a 2-day follow-up."""
    run = _Run(engagement, "proof_pack_request")
    run.log("proof_pack_requested")
    run.draft(
        action_type="follow_up_task",
        action_mode="approval_required",
        summary_en="Follow-up task scheduled 2 days after the proof-pack request.",
        summary_ar="مهمة متابعة بعد يومين من طلب حزمة الإثبات.",
        queue_approval=True,
    )
    return run.result(
        notes_en="Proof-pack request logged; 2-day follow-up queued.",
        notes_ar="تم تسجيل طلب حزمة الإثبات وجدولة متابعة بعد يومين.",
    )


# ── Automation 4 — Meeting Booked ─────────────────────────────────────
def automation_4_meeting_booked(
    engagement: AutopilotEngagement, payload: dict
) -> AutomationResult:
    """Advance to meeting_booked; draft a pre-call brief + discovery questions."""
    run = _Run(engagement, "meeting_booked")
    run.advance("meeting_booked")
    run.log("meeting_booked")
    run.draft(
        action_type="prepare_diagnostic",
        summary_en="Pre-call brief and 5 discovery questions (internal).",
        summary_ar="ملخص ما قبل المكالمة و٥ أسئلة استكشافية (داخلي).",
        queue_approval=False,
    )
    return run.result(
        notes_en="Meeting booked; pre-call brief drafted.",
        notes_ar="تم حجز الاجتماع وإعداد ملخص ما قبل المكالمة.",
    )


# ── Automation 5 — Meeting Done ───────────────────────────────────────
def automation_5_meeting_done(
    engagement: AutopilotEngagement, payload: dict
) -> AutomationResult:
    """Mark the meeting done; route to scope_requested or nurture."""
    run = _Run(engagement, "meeting_done")
    run.advance("meeting_done")
    scope_requested = bool(payload.get("scope_requested", False))
    run.log("meeting_done", {"scope_requested": scope_requested})
    if scope_requested:
        run.advance("scope_requested")
        notes_en = "Meeting done; scope requested."
        notes_ar = "انتهى الاجتماع وطُلب نطاق العمل."
    else:
        run.advance("nurture")
        notes_en = "Meeting done; no scope — moved to nurture."
        notes_ar = "انتهى الاجتماع دون نطاق — نُقل إلى التنشئة."
    return run.result(notes_en=notes_en, notes_ar=notes_ar)


# ── Automation 6 — Scope Requested ────────────────────────────────────
def automation_6_scope_requested(
    engagement: AutopilotEngagement, payload: dict
) -> AutomationResult:
    """Draft the scope doc + invoice, recommend a tier, queue for approval."""
    if engagement.current_stage != "scope_requested":
        raise ValueError("automation 'scope_requested' requires stage scope_requested")
    run = _Run(engagement, "scope_requested")
    tier = _recommend_tier(engagement.lead_score)
    engagement.tier_recommendation = tier
    run.advance("scope_sent")
    run.log("scope_requested", {"tier_recommendation": tier})
    run.draft(
        action_type="draft_email",
        action_mode="approval_required",
        summary_en="Scope document draft to send to the customer.",
        summary_ar="مسودة وثيقة نطاق العمل لإرسالها للعميل.",
        queue_approval=True,
    )
    run.draft(
        action_type="payment_reminder",
        action_mode="approval_required",
        summary_en=f"Invoice draft for recommended tier '{tier}'.",
        summary_ar=f"مسودة فاتورة للباقة الموصى بها '{tier}'.",
        queue_approval=True,
    )
    return run.result(
        notes_en=f"Scope + invoice drafted; recommended tier {tier}.",
        notes_ar=f"أُعدّت مسودة النطاق والفاتورة؛ الباقة الموصى بها {tier}.",
    )


# ── Automation 7 — Invoice Paid ───────────────────────────────────────
def automation_7_invoice_paid(
    engagement: AutopilotEngagement, payload: dict
) -> AutomationResult:
    """Record a confirmed payment; open delivery + onboarding."""
    if engagement.current_stage != "invoice_sent":
        raise ValueError("automation 'invoice_paid' requires stage invoice_sent")
    run = _Run(engagement, "invoice_paid")
    run.advance("invoice_paid")
    run.log("invoice_paid", {"payment_evidence": payload.get("payment_evidence", "")})
    run.draft(
        action_type="draft_email",
        action_mode="approval_required",
        summary_en="Onboarding form email to send to the customer.",
        summary_ar="بريد نموذج التهيئة لإرساله للعميل.",
        queue_approval=True,
    )
    run.draft(
        action_type="delivery_task",
        summary_en="Delivery folder + diagnostic checklist created (internal).",
        summary_ar="إنشاء مجلد التسليم وقائمة التشخيص (داخلي).",
        queue_approval=False,
    )
    return run.result(
        notes_en="Payment recorded; delivery opened; onboarding queued.",
        notes_ar="سُجّل الدفع وفُتح التسليم وأُدرج التهيئة للموافقة.",
    )


# ── Automation 8 — Delivery ───────────────────────────────────────────
def automation_8_delivery(
    engagement: AutopilotEngagement, payload: dict
) -> AutomationResult:
    """Start delivery; draft the diagnostic workplan + proof pack."""
    if engagement.current_stage != "invoice_paid":
        raise ValueError("automation 'delivery' requires stage invoice_paid")
    run = _Run(engagement, "delivery")
    run.advance("delivery_started")
    run.log("delivery_started")
    run.draft(
        action_type="prepare_diagnostic",
        summary_en="Diagnostic workplan draft (internal).",
        summary_ar="مسودة خطة عمل التشخيص (داخلي).",
        queue_approval=False,
    )
    run.draft(
        action_type="proof_request",
        summary_en="Proof Pack draft — internal, not yet sent.",
        summary_ar="مسودة حزمة الإثبات — داخلية ولم تُرسل بعد.",
        queue_approval=False,
    )
    return run.result(
        notes_en="Delivery started; workplan + proof pack drafted.",
        notes_ar="بدأ التسليم وأُعدّت خطة العمل وحزمة الإثبات.",
    )


# ── Automation 9 — Proof Pack Sent ────────────────────────────────────
def automation_9_proof_pack_sent(
    engagement: AutopilotEngagement, payload: dict
) -> AutomationResult:
    """Record the founder-approved proof pack; draft an upsell recommendation."""
    if engagement.current_stage != "delivery_started":
        raise ValueError("automation 'proof_pack_sent' requires stage delivery_started")
    run = _Run(engagement, "proof_pack_sent")
    run.advance("proof_pack_sent")
    run.log("proof_pack_sent")
    run.draft(
        action_type="draft_email",
        action_mode="approved_manual",
        summary_en="Final Proof Pack send — founder-approved, recorded for audit.",
        summary_ar="إرسال حزمة الإثبات النهائية — بموافقة المؤسس، مُسجّل للتدقيق.",
        queue_approval=False,
    )
    run.draft(
        action_type="upsell_recommendation",
        summary_en="Next-best-offer recommendation (internal).",
        summary_ar="توصية بأفضل عرض تالٍ (داخلي).",
        queue_approval=False,
    )
    run.draft(
        action_type="follow_up_task",
        action_mode="approval_required",
        summary_en="Follow-up task 3 days after the proof pack.",
        summary_ar="مهمة متابعة بعد ٣ أيام من حزمة الإثبات.",
        queue_approval=True,
    )
    return run.result(
        notes_en="Proof pack sent; upsell recommendation drafted.",
        notes_ar="أُرسلت حزمة الإثبات وأُعدّت توصية الترقية.",
    )


# ── Automation 10 — Retainer / Sprint Upsell ──────────────────────────
def automation_10_retainer_sprint_upsell(
    engagement: AutopilotEngagement, payload: dict
) -> AutomationResult:
    """Draft the Sprint + Retainer proposals; queue them for approval."""
    if engagement.current_stage != "proof_pack_sent":
        raise ValueError(
            "automation 'retainer_sprint_upsell' requires stage proof_pack_sent"
        )
    run = _Run(engagement, "retainer_sprint_upsell")
    target: FunnelStage = payload.get("target", "sprint_candidate")
    if target not in ("sprint_candidate", "retainer_candidate"):
        raise ValueError("target must be sprint_candidate or retainer_candidate")
    run.advance(target)
    run.log("upsell_generated", {"target": target})
    run.draft(
        action_type="upsell_recommendation",
        action_mode="approval_required",
        summary_en="Revenue Intelligence Sprint proposal draft.",
        summary_ar="مسودة عرض سبرنت ذكاء الإيراد.",
        queue_approval=True,
    )
    run.draft(
        action_type="upsell_recommendation",
        action_mode="approval_required",
        summary_en="Governed Ops Retainer proposal draft.",
        summary_ar="مسودة عرض اشتراك العمليات المحكومة.",
        queue_approval=True,
    )
    return run.result(
        notes_en=f"Upsell proposals drafted; moved to {target}.",
        notes_ar=f"أُعدّت عروض الترقية؛ نُقل إلى {target}.",
    )


# Dispatch table for automations 2-10 (automation 1 runs at lead capture).
AUTOMATIONS: dict[str, Callable[[AutopilotEngagement, dict], AutomationResult]] = {
    "qualified_lead": automation_2_qualified_lead,
    "proof_pack_request": automation_3_proof_pack_request,
    "meeting_booked": automation_4_meeting_booked,
    "meeting_done": automation_5_meeting_done,
    "scope_requested": automation_6_scope_requested,
    "invoice_paid": automation_7_invoice_paid,
    "delivery": automation_8_delivery,
    "proof_pack_sent": automation_9_proof_pack_sent,
    "retainer_sprint_upsell": automation_10_retainer_sprint_upsell,
}


__all__ = [
    "AUTOMATIONS",
    "automation_1_lead_capture",
    "automation_2_qualified_lead",
    "automation_3_proof_pack_request",
    "automation_4_meeting_booked",
    "automation_5_meeting_done",
    "automation_6_scope_requested",
    "automation_7_invoice_paid",
    "automation_8_delivery",
    "automation_9_proof_pack_sent",
    "automation_10_retainer_sprint_upsell",
]
