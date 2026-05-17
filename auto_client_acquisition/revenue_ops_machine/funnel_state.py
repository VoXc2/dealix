"""Revenue Ops Machine — the 16-state sales funnel state machine.

This is the canonical funnel for the online sales machine. It is purely
additive: the legacy 12-stage deal machine in ``api/routers/full_os.py`` is
never modified — a one-way bridge (:data:`LEGACY_STAGE_BRIDGE`) maps funnel
states onto legacy deal stages for any downstream consumer that still reads
``DealRecord.stage``.

Two layers of safety:
  * :data:`TRANSITIONS` — the allowed transition graph.
  * :data:`MILESTONE_GUARDS` — defense-in-depth ordering invariants checked
    against the funnel context history, so an accidental graph edit can never
    let an invoice precede a scope (etc.).
"""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - typing only
    from auto_client_acquisition.revenue_ops_machine.context import FunnelContext


class RevenueOpsMachineError(Exception):
    """Base error for the Revenue Ops Machine."""


class IllegalTransition(RevenueOpsMachineError):
    """Raised when a funnel transition violates the graph or an ordering rule."""


class FunnelState(StrEnum):
    visitor = "visitor"
    lead_captured = "lead_captured"
    qualified_A = "qualified_A"
    qualified_B = "qualified_B"
    nurture = "nurture"
    meeting_booked = "meeting_booked"
    meeting_done = "meeting_done"
    scope_requested = "scope_requested"
    scope_sent = "scope_sent"
    invoice_sent = "invoice_sent"
    invoice_paid = "invoice_paid"
    delivery_started = "delivery_started"
    proof_pack_sent = "proof_pack_sent"
    upsell_sprint = "upsell_sprint"
    retainer_candidate = "retainer_candidate"
    closed_lost = "closed_lost"


# Success terminal: retainer_candidate. Recoverable terminal: closed_lost.
TERMINAL_STATES: frozenset[FunnelState] = frozenset({FunnelState.retainer_candidate})

# Allowed transitions (forward + key sideways moves). closed_lost is reachable
# from every non-terminal state and is added programmatically below.
_BASE_TRANSITIONS: dict[FunnelState, set[FunnelState]] = {
    FunnelState.visitor: {FunnelState.lead_captured},
    FunnelState.lead_captured: {
        FunnelState.qualified_A,
        FunnelState.qualified_B,
        FunnelState.nurture,
    },
    FunnelState.qualified_A: {FunnelState.meeting_booked, FunnelState.nurture},
    FunnelState.qualified_B: {FunnelState.meeting_booked, FunnelState.nurture},
    FunnelState.nurture: {
        FunnelState.qualified_A,
        FunnelState.qualified_B,
        FunnelState.meeting_booked,
    },
    FunnelState.meeting_booked: {FunnelState.meeting_done, FunnelState.nurture},
    FunnelState.meeting_done: {FunnelState.scope_requested, FunnelState.nurture},
    FunnelState.scope_requested: {FunnelState.scope_sent},
    FunnelState.scope_sent: {FunnelState.invoice_sent},
    FunnelState.invoice_sent: {FunnelState.invoice_paid},
    FunnelState.invoice_paid: {FunnelState.delivery_started},
    FunnelState.delivery_started: {FunnelState.proof_pack_sent},
    FunnelState.proof_pack_sent: {
        FunnelState.upsell_sprint,
        FunnelState.retainer_candidate,
    },
    FunnelState.upsell_sprint: {FunnelState.retainer_candidate},
    FunnelState.retainer_candidate: set(),
    FunnelState.closed_lost: {FunnelState.nurture},  # revival path
}

TRANSITIONS: dict[FunnelState, frozenset[FunnelState]] = {
    state: frozenset(
        targets
        | (
            {FunnelState.closed_lost}
            if state not in TERMINAL_STATES and state is not FunnelState.closed_lost
            else set()
        )
    )
    for state, targets in _BASE_TRANSITIONS.items()
}

# Defense-in-depth ordering invariants: entering ``target`` requires the funnel
# to have already reached the milestone state. Maps target -> required state.
MILESTONE_GUARDS: dict[FunnelState, FunnelState] = {
    FunnelState.invoice_sent: FunnelState.scope_sent,
    FunnelState.delivery_started: FunnelState.invoice_paid,
    FunnelState.proof_pack_sent: FunnelState.delivery_started,
    FunnelState.upsell_sprint: FunnelState.proof_pack_sent,
}

# Hard rules, in plain language, for the /states endpoint and operator docs.
HARD_RULES: tuple[str, ...] = (
    "no invoice_sent before scope_sent",
    "no delivery_started before invoice_paid",
    "no proof_pack_sent before delivery_started",
    "no upsell_sprint before proof_pack_sent",
    "no case study before written approval (case_study_approved flag)",
)


def can_transition(
    current: FunnelState,
    target: FunnelState,
    ctx: "FunnelContext | None" = None,
) -> tuple[bool, str]:
    """Return ``(allowed, reason)``. Pure — no I/O.

    ``reason`` is empty when allowed, otherwise a human-readable rejection.
    """
    current = FunnelState(current)
    target = FunnelState(target)
    if current == target:
        return False, f"already in state {target}"
    if target not in TRANSITIONS.get(current, frozenset()):
        return False, f"transition {current} -> {target} is not in the graph"
    required = MILESTONE_GUARDS.get(target)
    if required is not None:
        reached = ctx is not None and ctx.has_reached(required)
        # The only graph path into a guarded state is from its milestone, so
        # current == required also satisfies the invariant.
        if not reached and current != required:
            return False, f"{target} requires milestone {required} first"
    return True, ""


def advance(
    current: FunnelState,
    target: FunnelState,
    ctx: "FunnelContext | None" = None,
) -> FunnelState:
    """Validate a transition and return ``target``, or raise IllegalTransition.

    This is the single chokepoint every ops handler calls before changing
    funnel state.
    """
    allowed, reason = can_transition(current, target, ctx)
    if not allowed:
        raise IllegalTransition(reason)
    return FunnelState(target)


# ── One-way bridge to the legacy 12-stage deal machine (full_os.py) ──────────
LEGACY_STAGE_BRIDGE: dict[FunnelState, str] = {
    FunnelState.visitor: "new_lead",
    FunnelState.lead_captured: "new_lead",
    FunnelState.qualified_A: "qualified",
    FunnelState.qualified_B: "qualified",
    FunnelState.nurture: "nurturing",
    FunnelState.meeting_booked: "meeting_booked",
    FunnelState.meeting_done: "meeting_done",
    FunnelState.scope_requested: "proposal_sent",
    FunnelState.scope_sent: "proposal_sent",
    FunnelState.invoice_sent: "payment_requested",
    FunnelState.invoice_paid: "payment_requested",
    FunnelState.delivery_started: "pilot_active",
    FunnelState.proof_pack_sent: "pilot_active",
    FunnelState.upsell_sprint: "pilot_active",
    FunnelState.retainer_candidate: "closed_won",
    FunnelState.closed_lost: "closed_lost",
}

# Best-effort reverse map (one representative funnel state per legacy stage).
FROM_LEGACY: dict[str, FunnelState] = {
    "new_lead": FunnelState.lead_captured,
    "qualifying": FunnelState.lead_captured,
    "qualified": FunnelState.qualified_A,
    "nurturing": FunnelState.nurture,
    "meeting_booked": FunnelState.meeting_booked,
    "meeting_done": FunnelState.meeting_done,
    "proposal_sent": FunnelState.scope_sent,
    "negotiating": FunnelState.scope_sent,
    "payment_requested": FunnelState.invoice_sent,
    "pilot_active": FunnelState.delivery_started,
    "closed_won": FunnelState.retainer_candidate,
    "closed_lost": FunnelState.closed_lost,
    "opted_out": FunnelState.closed_lost,
}


def legacy_stage(state: FunnelState) -> str:
    """Map a funnel state to the legacy deal stage for downstream consumers."""
    return LEGACY_STAGE_BRIDGE[FunnelState(state)]


__all__ = [
    "FunnelState",
    "RevenueOpsMachineError",
    "IllegalTransition",
    "TRANSITIONS",
    "MILESTONE_GUARDS",
    "HARD_RULES",
    "TERMINAL_STATES",
    "LEGACY_STAGE_BRIDGE",
    "FROM_LEGACY",
    "can_transition",
    "advance",
    "legacy_stage",
]
