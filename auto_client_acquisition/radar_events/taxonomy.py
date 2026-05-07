"""Radar event taxonomy."""
from __future__ import annotations

EVENT_TYPES: tuple[str, ...] = (
    "lead_created",
    "lead_scored",
    "diagnostic_created",
    "approval_requested",
    "approval_accepted",
    "support_ticket_created",
    "support_ticket_escalated",
    "service_session_started",
    "payment_intent_created",
    "payment_confirmed",
    "proof_event_created",
    "proof_pack_generated",
    "executive_pack_generated",
    "unsafe_action_blocked",
    "whatsapp_decision_requested",
    "customer_portal_opened",
    "customer_portal_degraded",
    "case_study_candidate_created",
)


def is_known_event_type(event_type: str) -> bool:
    return event_type in EVENT_TYPES
