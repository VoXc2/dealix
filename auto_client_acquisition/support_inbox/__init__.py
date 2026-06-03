"""Support Inbox state store + SLA monitor.

Wraps existing support_os modules (classifier, ticket, escalation,
responder) with persistence + a webhook handler entry point.

Persistence: in-memory + JSONL (Article 11) at data/support_tickets.jsonl.
"""
from auto_client_acquisition.support_inbox.sla_monitor import (
    find_breached_tickets,
)
from auto_client_acquisition.support_inbox.state_store import (
    classify_and_store,
    get_ticket,
    list_tickets,
    set_status,
)

__all__ = [
    "classify_and_store",
    "find_breached_tickets",
    "get_ticket",
    "list_tickets",
    "set_status",
]
