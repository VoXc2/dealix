"""Support ticketing — persisted ticket lifecycle over the support_os
classifier and the Knowledge Base.

Hard rules:
  - Support never sends. Replies are drafted only; sending a reply is
    routed through the approval center.
  - High-risk categories (payment, refund, privacy/PDPL, angry customer,
    security) always escalate and are never auto-answerable.
  - Every lifecycle transition writes an evidence event.
"""

from __future__ import annotations

from auto_client_acquisition.support.lifecycle import (
    classify_ticket,
    create_ticket,
    draft_reply,
    escalate_ticket,
    request_send_reply,
    resolve_ticket,
)
from auto_client_acquisition.support.risk import (
    HIGH_RISK_CATEGORIES,
    is_auto_answerable,
    risk_level_for_category,
)
from auto_client_acquisition.support.ticket_store import (
    SupportTicket,
    TicketStore,
    get_default_ticket_store,
    reset_default_ticket_store,
)

__all__ = [
    "HIGH_RISK_CATEGORIES",
    "SupportTicket",
    "TicketStore",
    "classify_ticket",
    "create_ticket",
    "draft_reply",
    "escalate_ticket",
    "get_default_ticket_store",
    "is_auto_answerable",
    "request_send_reply",
    "reset_default_ticket_store",
    "resolve_ticket",
    "risk_level_for_category",
]
