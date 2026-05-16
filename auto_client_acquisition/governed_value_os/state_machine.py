"""Governed value proof progression — the strict L2–L7 state machine.

This is the operating-backbone encoding of the "Full Ops" doctrine: the system
prepares, suggests, warns, records, verifies, classifies and drafts — the founder
approves every external action. The machine never sends or charges.

NOTE: the ``L2..L7`` labels here are the *governed value progression* labels. They
are a separate concept from ``proof_engine.evidence.EvidenceLevel`` (L0–L5), which
classifies a single proof event. This machine tracks a contact/engagement journey.

Progression and labels (doctrine §8):

    prepared_not_sent       L2
    sent                    L4
    replied_interested      L4
    meeting_booked          L4
    used_in_meeting         L5
    scope_requested         L6
    pilot_intro_requested   L6
    invoice_sent            L7_candidate
    invoice_paid            L7_confirmed

Hard rules enforced by :func:`validate_transition`:

    - no ``sent`` without ``founder_confirmed=True``
    - no ``used_in_meeting`` (L5) without a prior ``meeting_booked``
    - no ``scope_requested`` / ``pilot_intro_requested`` (L6) without an explicit
      scope or intro request
    - no ``invoice_paid`` (L7 confirmed) without a payment reference
    - revenue is never recognized before ``invoice_paid``
"""

from __future__ import annotations

from enum import Enum


class ProofState(str, Enum):
    PREPARED_NOT_SENT = "prepared_not_sent"
    SENT = "sent"
    REPLIED_INTERESTED = "replied_interested"
    MEETING_BOOKED = "meeting_booked"
    USED_IN_MEETING = "used_in_meeting"
    SCOPE_REQUESTED = "scope_requested"
    PILOT_INTRO_REQUESTED = "pilot_intro_requested"
    INVOICE_SENT = "invoice_sent"
    INVOICE_PAID = "invoice_paid"


PROOF_LEVEL_LABEL: dict[ProofState, str] = {
    ProofState.PREPARED_NOT_SENT: "L2",
    ProofState.SENT: "L4",
    ProofState.REPLIED_INTERESTED: "L4",
    ProofState.MEETING_BOOKED: "L4",
    ProofState.USED_IN_MEETING: "L5",
    ProofState.SCOPE_REQUESTED: "L6",
    ProofState.PILOT_INTRO_REQUESTED: "L6",
    ProofState.INVOICE_SENT: "L7_candidate",
    ProofState.INVOICE_PAID: "L7_confirmed",
}


ALLOWED_TRANSITIONS: dict[ProofState, frozenset[ProofState]] = {
    ProofState.PREPARED_NOT_SENT: frozenset({ProofState.SENT}),
    ProofState.SENT: frozenset(
        {ProofState.REPLIED_INTERESTED, ProofState.MEETING_BOOKED}
    ),
    ProofState.REPLIED_INTERESTED: frozenset({ProofState.MEETING_BOOKED}),
    ProofState.MEETING_BOOKED: frozenset({ProofState.USED_IN_MEETING}),
    ProofState.USED_IN_MEETING: frozenset(
        {ProofState.SCOPE_REQUESTED, ProofState.PILOT_INTRO_REQUESTED}
    ),
    ProofState.SCOPE_REQUESTED: frozenset(
        {ProofState.INVOICE_SENT, ProofState.PILOT_INTRO_REQUESTED}
    ),
    ProofState.PILOT_INTRO_REQUESTED: frozenset(
        {ProofState.INVOICE_SENT, ProofState.SCOPE_REQUESTED}
    ),
    ProofState.INVOICE_SENT: frozenset({ProofState.INVOICE_PAID}),
    ProofState.INVOICE_PAID: frozenset(),
}

_L6_STATES = frozenset({ProofState.SCOPE_REQUESTED, ProofState.PILOT_INTRO_REQUESTED})

_REASONS: dict[str, dict[str, str]] = {
    "illegal_transition": {
        "ar": "انتقال غير مسموح في آلة حالة الإثبات.",
        "en": "Transition not allowed in the proof state machine.",
    },
    "sent_requires_founder_confirmation": {
        "ar": "لا يُسمح بحالة (مُرسَل) بدون تأكيد المؤسس — لا إرسال تلقائي.",
        "en": "No 'sent' state without founder confirmation — no autonomous send.",
    },
    "l5_requires_meeting": {
        "ar": "لا يُسمح بمستوى L5 (استُخدم في اجتماع) قبل حجز اجتماع فعلي.",
        "en": "No L5 (used_in_meeting) before an actual booked meeting.",
    },
    "l6_requires_scope_or_intro_request": {
        "ar": "لا يُسمح بمستوى L6 بدون طلب نطاق أو طلب تعريف صريح من العميل.",
        "en": "No L6 without an explicit scope or intro request from the customer.",
    },
    "l7_confirmed_requires_payment": {
        "ar": "لا يُسمح بمستوى L7 المؤكد (مدفوع) بدون مرجع دفع.",
        "en": "No L7-confirmed (invoice_paid) without a payment reference.",
    },
}


class ProofTransitionError(ValueError):
    """Raised when a proposed transition breaches a doctrine guard."""

    def __init__(self, code: str) -> None:
        self.code = code
        reason = _REASONS.get(code, {"ar": code, "en": code})
        self.reason_ar = reason["ar"]
        self.reason_en = reason["en"]
        super().__init__(reason["en"])


def validate_transition(
    current: ProofState,
    target: ProofState,
    *,
    founder_confirmed: bool = False,
    scope_requested: bool = False,
    payment_ref: str = "",
) -> None:
    """Raise :class:`ProofTransitionError` if the transition breaches doctrine."""
    if target not in ALLOWED_TRANSITIONS.get(current, frozenset()):
        raise ProofTransitionError("illegal_transition")
    if target is ProofState.SENT and not founder_confirmed:
        raise ProofTransitionError("sent_requires_founder_confirmation")
    if target is ProofState.USED_IN_MEETING and current is not ProofState.MEETING_BOOKED:
        raise ProofTransitionError("l5_requires_meeting")
    if target in _L6_STATES and not scope_requested:
        raise ProofTransitionError("l6_requires_scope_or_intro_request")
    if target is ProofState.INVOICE_PAID and not payment_ref.strip():
        raise ProofTransitionError("l7_confirmed_requires_payment")


def revenue_recognized(state: ProofState) -> bool:
    """Revenue is recognized only once an invoice is paid (doctrine §8)."""
    return state is ProofState.INVOICE_PAID


def level_label(state: ProofState) -> str:
    """The governed-value progression label (L2..L7_confirmed) for a state."""
    return PROOF_LEVEL_LABEL[state]
