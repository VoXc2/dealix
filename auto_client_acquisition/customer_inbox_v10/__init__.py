"""Customer Inbox v10 — Chatwoot-inspired typed shell.

Pure native Python. NO LLM. NO live send. Outbound is always
draft_only / approval_required / blocked. Cold WhatsApp outbound is
platform-blocked unless explicit consent is registered.
"""
from auto_client_acquisition.customer_inbox_v10.schemas import (
    Channel,
    ConsentStatus,
    Conversation,
    Message,
    MessageDirection,
    ReplySuggestion,
    SLAStatus,
)
from auto_client_acquisition.customer_inbox_v10.consent_status import check_consent
from auto_client_acquisition.customer_inbox_v10.conversation_model import (
    add_inbound,
    start_conversation,
)
from auto_client_acquisition.customer_inbox_v10.escalation import escalate
from auto_client_acquisition.customer_inbox_v10.reply_suggestion import suggest_reply
from auto_client_acquisition.customer_inbox_v10.routing_policy import route_to_channel
from auto_client_acquisition.customer_inbox_v10.sla_policy import (
    compute_sla,
    default_sla_hours,
    sla_table,
)

__all__ = [
    "Channel",
    "ConsentStatus",
    "Conversation",
    "Message",
    "MessageDirection",
    "ReplySuggestion",
    "SLAStatus",
    "add_inbound",
    "check_consent",
    "compute_sla",
    "default_sla_hours",
    "escalate",
    "route_to_channel",
    "sla_table",
    "start_conversation",
    "suggest_reply",
]
