"""Pure transition validation for the Commercial Evidence State Machine.

Canonical spec: docs/commercial/COMMERCIAL_EVIDENCE_STATE_MACHINE.md

No I/O. ``validate_transition`` is a pure function used by ``CommercialEngine``
and by the ``POST /api/v1/evidence/events`` endpoint (illegal transitions
return 422).
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.commercial_os.cel import STATE_TO_CEL


@dataclass(frozen=True)
class TransitionResult:
    """Outcome of a transition check."""

    ok: bool
    reason: str


# The legal transition graph from the CEL spec's transition table.
# ``None`` represents the (start) state, before any commercial event.
_LEGAL_TRANSITIONS: dict[str | None, frozenset[str]] = {
    None: frozenset({"prepared_not_sent"}),
    "prepared_not_sent": frozenset({"sent"}),
    "sent": frozenset({"replied_interested", "silent", "not_interested"}),
    "replied_interested": frozenset({"meeting_booked"}),
    "meeting_booked": frozenset({"used_in_meeting"}),
    "used_in_meeting": frozenset({"scope_requested", "pilot_intro_requested"}),
    "scope_requested": frozenset({"invoice_sent"}),
    "pilot_intro_requested": frozenset({"invoice_sent"}),
    "invoice_sent": frozenset({"invoice_paid"}),
    # Terminal-ish states have no onward transitions.
    "silent": frozenset(),
    "not_interested": frozenset(),
    "invoice_paid": frozenset(),
}


def validate_transition(
    current: str | None,
    next_state: str,
    *,
    founder_confirmed: bool = False,
    used_in_meeting: bool = False,
    scope_or_intro_requested: bool = False,
    invoice_paid: bool = False,
) -> TransitionResult:
    """Validate a single commercial state transition.

    Enforces the legal transition graph plus the five hard rules from the
    CEL spec.

    Args:
        current: the current commercial state, or ``None`` for (start).
        next_state: the proposed next commercial state.
        founder_confirmed: a founder explicitly approved the send.
        used_in_meeting: a Dealix artifact was used in a real meeting.
        scope_or_intro_requested: the prospect asked for a scope / intro.
        invoice_paid: payment was received and reconciled.

    Returns:
        ``TransitionResult(ok, reason)``.
    """
    if next_state not in STATE_TO_CEL:
        return TransitionResult(False, f"unknown_next_state:{next_state}")
    if current is not None and current not in STATE_TO_CEL:
        return TransitionResult(False, f"unknown_current_state:{current}")

    allowed = _LEGAL_TRANSITIONS.get(current, frozenset())
    if next_state not in allowed:
        return TransitionResult(
            False, f"illegal_transition:{current}->{next_state}"
        )

    # Rule 1 — no `sent` without founder approval.
    if next_state == "sent" and not founder_confirmed:
        return TransitionResult(False, "rule1_sent_requires_founder_confirmed")

    # Rule 2 — no CEL5 (`used_in_meeting`) without the artifact actually used.
    if next_state == "used_in_meeting" and not used_in_meeting:
        return TransitionResult(False, "rule2_cel5_requires_used_in_meeting")

    # Rule 3 — no CEL6 without a scope or intro request from the prospect.
    if next_state in ("scope_requested", "pilot_intro_requested") and (
        not scope_or_intro_requested
    ):
        return TransitionResult(False, "rule3_cel6_requires_scope_or_intro")

    # Rule 4 — no CEL7_confirmed (`invoice_paid`) without payment.
    if next_state == "invoice_paid" and not invoice_paid:
        return TransitionResult(False, "rule4_invoice_paid_requires_payment")

    return TransitionResult(True, "ok")


def is_revenue_recognized(state: str) -> bool:
    """Rule 5 — revenue is recognized only at ``CEL7_confirmed``.

    Reporting, the North Star count, and the value ledger read this, never
    ``CEL7_candidate``.
    """
    return STATE_TO_CEL.get(state) == "CEL7_confirmed"
