"""Customer-journey state machine."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.customer_loop.schemas import (
    ALLOWED_TRANSITIONS,
    JourneyAdvanceRequest,
    JourneyAdvanceResult,
    JourneyState,
    JourneyTransition,
)

# Per-state checklist of NEXT actions. Each item is bilingual.
# Actions describe what a HUMAN should do — they are not run
# automatically. No external sends, no charges, no scraping.
_NEXT_ACTIONS_AR: dict[JourneyState, list[str]] = {
    JourneyState.LEAD_INTAKE: [
        "افتح الإشعار في بريد المؤسس واقرأ بيانات العميل.",
        "صنّف القطاع والـICP بسرعة (≤2 دقيقة).",
        "أعدّ سؤال Diagnostic مخصّصاً لقطاع العميل.",
    ],
    JourneyState.DIAGNOSTIC_REQUESTED: [
        "احجز موعد Diagnostic 30 دقيقة (لا إرسال آلي).",
        "حضّر قالب الـ Diagnostic من matrix YAML.",
        "أرسل بريد تأكيد يدوي للعميل بعد المراجعة.",
    ],
    JourneyState.DIAGNOSTIC_SENT: [
        "تابَع رد العميل خلال 48 ساعة (مرّة فقط، لا spam).",
        "إذا اهتمّ، انتقل لـ Pilot offer مع 499 ريال.",
        "وثّق التقييم في docs/proof-events/<slug>.json.",
    ],
    JourneyState.PILOT_OFFERED: [
        "انشئ فاتورة Moyasar test_mode عبر scripts/dealix_invoice.py.",
        "أرسل رابط الفاتورة يدوياً للعميل.",
        "اكتب تذكير للمتابعة بعد 72 ساعة.",
    ],
    JourneyState.PAYMENT_PENDING: [
        "راقب لوحة Moyasar للدفع — لا تخصم آلياً.",
        "إذا اخترتم commitment مكتوب بدلاً من دفع، احفظ توقيعه نصياً.",
        "ابدأ تجهيز جلسة التسليم الأولى لكسب الزخم.",
    ],
    JourneyState.PAID_OR_COMMITTED: [
        "افتح ServiceSession للعميل — Top 5 services واحدة بناء على القطاع.",
        "أرسل خطّة 7 أيام للعميل (مسوّدة، تحتاج موافقتك).",
        "أنشئ ProofEvent: invoice_paid_or_committed.",
    ],
    JourneyState.IN_DELIVERY: [
        "نفّذ مهام التسليم اليومية يدوياً (10 فرص، مسوّدات عربية، خطّة متابعة).",
        "كل مسوّدة تمرّ بـ ApprovalGate قبل أيّ إرسال خارجي.",
        "سجّل ProofEvent عند كل خطوة مكتملة.",
    ],
    JourneyState.PROOF_PACK_READY: [
        "اجمع الـ ProofEvents في pack عبر POST /api/v1/self-growth/proof-pack/assemble.",
        "اطلب موافقة العميل على نشر اسمه (consent_for_publication).",
        "حضّر Markdown نهائي للمراجعة.",
    ],
    JourneyState.PROOF_PACK_SENT: [
        "أرسل Pack يدوياً (بريد/WhatsApp بعد opt-in).",
        "اطلب توقيع رضا من العميل.",
        "حدّد موعد جلسة upsell خلال أسبوعين.",
    ],
    JourneyState.UPSELL_RECOMMENDED: [
        "اقترح Executive Growth OS بـ 2,999 ريال/شهر.",
        "أو Partnership Growth إذا كان العميل وكالة.",
        "إذا رفض، انتقل لـ Nurture لمدّة 30 يوم.",
    ],
    JourneyState.NURTURE: [
        "ضع العميل في قائمة المتابعة ربع سنوية.",
        "لا spam — تواصل واحد كل 90 يوم بمحتوى ذو قيمة.",
        "احترم خيار Opt-out إذا طلبه.",
    ],
    JourneyState.BLOCKED: [
        "افتح ticket في Issues يوضّح سبب الحظر.",
        "لا تتخطّى السبب — أصلح الجذر قبل المتابعة.",
        "وثّق الحادثة في docs/V5_OS_SCOPE.md إذا كانت سياسة.",
    ],
}

_NEXT_ACTIONS_EN: dict[JourneyState, list[str]] = {
    JourneyState.LEAD_INTAKE: [
        "Open the founder-inbox alert and read the customer's payload.",
        "Quickly classify sector + ICP fit (≤2 min).",
        "Prepare a sector-specific Diagnostic question.",
    ],
    JourneyState.DIAGNOSTIC_REQUESTED: [
        "Book a 30-min Diagnostic call (no automated send).",
        "Prepare the Diagnostic template from the YAML matrix.",
        "Send a manual confirmation email after review.",
    ],
    JourneyState.DIAGNOSTIC_SENT: [
        "Follow up once within 48h (single touch, never spam).",
        "If interested, advance to Pilot offer at 499 SAR.",
        "Record the assessment in docs/proof-events/<slug>.json.",
    ],
    JourneyState.PILOT_OFFERED: [
        "Create a Moyasar test-mode invoice via scripts/dealix_invoice.py.",
        "Send the hosted-payment URL manually.",
        "Set a 72h follow-up reminder.",
    ],
    JourneyState.PAYMENT_PENDING: [
        "Watch the Moyasar dashboard — no auto-charge.",
        "If they signed a written commitment instead, archive it.",
        "Start preparing the first delivery session to build momentum.",
    ],
    JourneyState.PAID_OR_COMMITTED: [
        "Open a ServiceSession (one of Top 5 by sector).",
        "Send the 7-day plan to the customer (draft; needs your approval).",
        "Create ProofEvent: invoice_paid_or_committed.",
    ],
    JourneyState.IN_DELIVERY: [
        "Execute daily delivery tasks manually (10 opps, Arabic drafts, follow-up).",
        "Every draft passes ApprovalGate before external send.",
        "Log a ProofEvent for each completed step.",
    ],
    JourneyState.PROOF_PACK_READY: [
        "Assemble events via POST /api/v1/self-growth/proof-pack/assemble.",
        "Ask the customer for publication consent.",
        "Prepare final markdown for review.",
    ],
    JourneyState.PROOF_PACK_SENT: [
        "Send the pack manually (email / WhatsApp after opt-in).",
        "Request a satisfaction sign-off.",
        "Schedule an upsell call within 2 weeks.",
    ],
    JourneyState.UPSELL_RECOMMENDED: [
        "Offer Executive Growth OS at 2,999 SAR/month.",
        "Or Partnership Growth if the customer is an agency.",
        "If declined, move to Nurture for 30 days.",
    ],
    JourneyState.NURTURE: [
        "Add the customer to the quarterly nurture list.",
        "No spam — one valuable touch every 90 days.",
        "Respect opt-out if requested.",
    ],
    JourneyState.BLOCKED: [
        "Open an issue describing the block reason.",
        "Never bypass — fix the root cause first.",
        "Document the policy in docs/V5_OS_SCOPE.md if structural.",
    ],
}

# States where the action involves contacting the customer, so an
# explicit approval is mandatory before execution.
_APPROVAL_REQUIRED_STATES: set[JourneyState] = {
    JourneyState.DIAGNOSTIC_REQUESTED,
    JourneyState.DIAGNOSTIC_SENT,
    JourneyState.PILOT_OFFERED,
    JourneyState.PROOF_PACK_SENT,
    JourneyState.UPSELL_RECOMMENDED,
}

# States where logging a ProofEvent is recommended so the founder's
# weekly Proof Pack can pull from a real audit trail.
_PROOF_EVENT_STATES: set[JourneyState] = {
    JourneyState.PAID_OR_COMMITTED,
    JourneyState.IN_DELIVERY,
    JourneyState.PROOF_PACK_READY,
    JourneyState.PROOF_PACK_SENT,
}

_BASE_SAFETY_NOTES = [
    "no_cold_outreach",
    "no_scraping",
    "no_linkedin_automation",
    "approval_required_for_external_send",
]


def list_states() -> dict[str, Any]:
    """Catalog of all states + each state's allowed transitions."""
    states: list[dict[str, Any]] = []
    for state in JourneyState:
        targets = sorted(t.value for t in ALLOWED_TRANSITIONS.get(state, set()))
        states.append({
            "state": state.value,
            "next_actions_ar": _NEXT_ACTIONS_AR.get(state, []),
            "next_actions_en": _NEXT_ACTIONS_EN.get(state, []),
            "allowed_transitions": targets,
            "approval_required_to_enter": state in _APPROVAL_REQUIRED_STATES,
            "proof_event_recommended": state in _PROOF_EVENT_STATES,
        })
    return {
        "states_total": len(states),
        "states": states,
    }


def next_actions_for_state(state: JourneyState) -> dict[str, Any]:
    """Return the bilingual checklist for a single state."""
    return {
        "state": state.value,
        "next_actions_ar": list(_NEXT_ACTIONS_AR.get(state, [])),
        "next_actions_en": list(_NEXT_ACTIONS_EN.get(state, [])),
        "approval_required": state in _APPROVAL_REQUIRED_STATES,
        "proof_event_recommended": state in _PROOF_EVENT_STATES,
    }


def advance(req: JourneyAdvanceRequest) -> JourneyAdvanceResult:
    """Execute one journey transition.

    Validates that the requested transition is in
    ``ALLOWED_TRANSITIONS``. Rejects anything else with an honest
    rejection reason — never silently skip a stage.
    """
    src = JourneyState(req.current_state)
    tgt = JourneyState(req.target_state)
    allowed = ALLOWED_TRANSITIONS.get(src, set())

    if tgt not in allowed:
        return JourneyAdvanceResult(
            accepted=False,
            from_state=src,
            to_state=None,
            rejection_reason=(
                f"transition {src.value} → {tgt.value} not allowed; "
                f"valid targets: {sorted(t.value for t in allowed) or '[none — terminal]'}"
            ),
            approval_required=True,
            safety_notes=list(_BASE_SAFETY_NOTES),
        )

    return JourneyAdvanceResult(
        accepted=True,
        from_state=src,
        to_state=tgt,
        next_actions_ar=list(_NEXT_ACTIONS_AR.get(tgt, [])),
        next_actions_en=list(_NEXT_ACTIONS_EN.get(tgt, [])),
        approval_required=tgt in _APPROVAL_REQUIRED_STATES,
        proof_event_recommended=tgt in _PROOF_EVENT_STATES,
        safety_notes=list(_BASE_SAFETY_NOTES),
    )


def transitions_from(state: JourneyState) -> list[JourneyTransition]:
    """List of allowed transitions from a state, ready for UI."""
    out: list[JourneyTransition] = []
    for tgt in sorted(ALLOWED_TRANSITIONS.get(state, set()), key=lambda s: s.value):
        out.append(JourneyTransition(
            target=tgt,
            label_ar=_NEXT_ACTIONS_AR.get(tgt, [""])[0] if _NEXT_ACTIONS_AR.get(tgt) else tgt.value,
            label_en=_NEXT_ACTIONS_EN.get(tgt, [""])[0] if _NEXT_ACTIONS_EN.get(tgt) else tgt.value,
            requires_approval=tgt in _APPROVAL_REQUIRED_STATES,
        ))
    return out
