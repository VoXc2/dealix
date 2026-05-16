"""Commercial Evidence Level (CEL) — states and levels.

Canonical spec: docs/commercial/COMMERCIAL_EVIDENCE_STATE_MACHINE.md

CEL is an axis orthogonal to the proof / autonomy axis (L0-L5). It answers
"how far has this commercial engagement progressed, and what evidence proves
it?" Every commercial level is written with the ``CEL`` prefix to avoid
collision with the proof axis.
"""

from __future__ import annotations

from typing import Literal, get_args

# ── The commercial evidence levels ──────────────────────────────────
CommercialEvidenceLevel = Literal[
    "CEL2",            # outreach drafted and staged, nothing sent
    "CEL4",            # founder-approved message sent / reply / meeting booked
    "CEL5",            # a Dealix artifact was used in a real meeting
    "CEL6",            # prospect asked for a scope / pilot / intro
    "CEL7_candidate",  # an invoice has been issued
    "CEL7_confirmed",  # payment received and reconciled
]

# ── The named commercial states ─────────────────────────────────────
CommercialState = Literal[
    "prepared_not_sent",
    "sent",
    "replied_interested",
    "meeting_booked",
    "used_in_meeting",
    "scope_requested",
    "pilot_intro_requested",
    "invoice_sent",
    "invoice_paid",
    # Reply terminals — recorded outcomes of a `sent` engagement
    "silent",
    "not_interested",
]

# ── State -> CEL mapping ────────────────────────────────────────────
STATE_TO_CEL: dict[str, str] = {
    "prepared_not_sent": "CEL2",
    "sent": "CEL4",
    "replied_interested": "CEL4",
    "silent": "CEL4",
    "not_interested": "CEL4",
    "meeting_booked": "CEL4",
    "used_in_meeting": "CEL5",
    "scope_requested": "CEL6",
    "pilot_intro_requested": "CEL6",
    "invoice_sent": "CEL7_candidate",
    "invoice_paid": "CEL7_confirmed",
}

# States that classify the outcome of a `sent` engagement.
REPLY_TERMINAL_STATES: frozenset[str] = frozenset(
    {"replied_interested", "silent", "not_interested"}
)

# Flat tuples derived from the Literals — handy for runtime membership checks.
CEL_LEVELS: tuple[str, ...] = tuple(get_args(CommercialEvidenceLevel))
COMMERCIAL_STATES: tuple[str, ...] = tuple(get_args(CommercialState))


def cel_for_state(state: str) -> str:
    """Return the CEL level string for a commercial state.

    Raises ``ValueError`` for an unknown state.
    """
    if state not in STATE_TO_CEL:
        raise ValueError(f"unknown commercial state: {state}")
    return STATE_TO_CEL[state]
