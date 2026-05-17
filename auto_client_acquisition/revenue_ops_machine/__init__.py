"""Revenue Ops Machine — a governed online sales funnel.

Wires six ops systems (Lead Capture, Qualification, Booking, Sales Call,
Scope+Invoice, Delivery+Proof) into one 16-state, state-machine-driven
pipeline. It reuses the existing approval engine, proof ledger, OutreachQueue
and offer ladder — and never sends anything externally without founder
approval.
"""

from __future__ import annotations

from auto_client_acquisition.revenue_ops_machine.abcd_scorer import (
    ABCDResult,
    ABCDSignals,
    abcd_score,
    abcd_to_funnel_state,
    classify,
    recommend_offer,
    score_form,
    signals_from_form,
)
from auto_client_acquisition.revenue_ops_machine.context import (
    FunnelContext,
    load_context,
    new_context,
    save_context,
)
from auto_client_acquisition.revenue_ops_machine.drafts import (
    DraftSpec,
    GatedDraft,
    blocked_proof_events,
    gate_specs,
    to_outreach_records,
)
from auto_client_acquisition.revenue_ops_machine.funnel_state import (
    HARD_RULES,
    LEGACY_STAGE_BRIDGE,
    TRANSITIONS,
    FunnelState,
    IllegalTransition,
    RevenueOpsMachineError,
    advance,
    can_transition,
    legacy_stage,
)
from auto_client_acquisition.revenue_ops_machine.handlers import (
    HandlerResult,
    booking_ops,
    delivery_proof_ops,
    lead_capture_ops,
    qualification_ops,
    sales_call_ops,
    scope_invoice_ops,
)

__all__ = [
    # state machine
    "FunnelState",
    "TRANSITIONS",
    "HARD_RULES",
    "LEGACY_STAGE_BRIDGE",
    "can_transition",
    "advance",
    "legacy_stage",
    "RevenueOpsMachineError",
    "IllegalTransition",
    # scoring
    "ABCDSignals",
    "ABCDResult",
    "abcd_score",
    "classify",
    "abcd_to_funnel_state",
    "signals_from_form",
    "score_form",
    "recommend_offer",
    # context
    "FunnelContext",
    "new_context",
    "load_context",
    "save_context",
    # drafts
    "DraftSpec",
    "GatedDraft",
    "gate_specs",
    "to_outreach_records",
    "blocked_proof_events",
    # handlers
    "HandlerResult",
    "lead_capture_ops",
    "qualification_ops",
    "booking_ops",
    "sales_call_ops",
    "scope_invoice_ops",
    "delivery_proof_ops",
]
