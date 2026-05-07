"""Service Sessions — lifecycle for one delivered service to one customer.

Wraps existing customer_loop.JourneyState + crm_v10.ServiceSession
with a thin state machine + persistence + approval-gated transitions.

Persistence: in-memory + JSONL (Article 11) — Postgres swap-in
documented in docs/FULL_OPS_10_LAYER_EVIDENCE_TABLE.md.
"""
from auto_client_acquisition.service_sessions.lifecycle import (
    advance_session,
    is_transition_allowed,
)
from auto_client_acquisition.service_sessions.store import (
    attach_deliverable,
    complete_session,
    get_session,
    list_sessions,
    start_session,
)

__all__ = [
    "advance_session",
    "attach_deliverable",
    "complete_session",
    "get_session",
    "is_transition_allowed",
    "list_sessions",
    "start_session",
]
