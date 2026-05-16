"""Governed engagement state machine for Revenue Ops.

Doctrine flow (linear, no skips, no auto-advance past `draft` without an
explicit founder approval):

    draft            — internal artifact, not visible externally
    approved         — founder approved (gate for any external action)
    sent             — delivered to client (manually or via authorized channel)
    used_in_meeting  — L5: artifact used in a client meeting
    scope_requested  — L6: client requested a sprint/retainer scope
    invoice_sent     — L7 candidate: invoice draft issued
    invoice_paid     — L7 confirmed: invoice paid

Rules enforced:
- No transition may skip a state.
- `draft → sent` is forbidden — approval is mandatory before any send.
- `invoice_paid` is terminal.
- A rejection returns an item from `approved`-pending back to `draft`.
"""

from __future__ import annotations

ENGAGEMENT_STATES: tuple[str, ...] = (
    "draft",
    "approved",
    "sent",
    "used_in_meeting",
    "scope_requested",
    "invoice_sent",
    "invoice_paid",
)

# Linear forward transitions + the single allowed rollback (reject → draft).
VALID_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"approved"}),
    "approved": frozenset({"sent", "draft"}),  # draft = rejection rollback
    "sent": frozenset({"used_in_meeting"}),
    "used_in_meeting": frozenset({"scope_requested"}),
    "scope_requested": frozenset({"invoice_sent"}),
    "invoice_sent": frozenset({"invoice_paid"}),
    "invoice_paid": frozenset(),  # terminal
}


class EngagementStateError(ValueError):
    """Raised on an invalid engagement state transition."""


def next_states(current: str) -> frozenset[str]:
    """Return the set of states reachable from ``current``."""
    if current not in VALID_TRANSITIONS:
        raise EngagementStateError(f"unknown engagement state: {current}")
    return VALID_TRANSITIONS[current]


def validate_transition(current: str, target: str) -> None:
    """Raise :class:`EngagementStateError` if ``current → target`` is illegal.

    Notably forbids ``draft → sent`` (no send without approval) and any skip.
    """
    if current not in VALID_TRANSITIONS:
        raise EngagementStateError(f"unknown current state: {current}")
    if target not in ENGAGEMENT_STATES:
        raise EngagementStateError(f"unknown target state: {target}")
    allowed = VALID_TRANSITIONS[current]
    if target not in allowed:
        raise EngagementStateError(
            f"illegal transition {current} → {target}; "
            f"allowed from {current}: {sorted(allowed) or '[terminal]'}"
        )
