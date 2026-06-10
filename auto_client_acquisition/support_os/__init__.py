"""V12 Support OS — Arabic-first ticket classification + SLA + KB answers.

Pure-local rule-based classifier (no LLM in V12). Reuses
``customer_inbox_v10`` SLA + reply_suggestion patterns where possible.
Every external-facing reply is ``draft_only``; support never sends.
"""
from auto_client_acquisition.support_os.classifier import (
    SupportCategory,
    classify_message,
)
from auto_client_acquisition.support_os.escalation import (
    EscalationDecision,
    should_escalate,
)
from auto_client_acquisition.support_os.knowledge_answer import (
    KnowledgeAnswer,
    answer_from_knowledge_base,
)
from auto_client_acquisition.support_os.responder import (
    ReplyDraft,
    draft_response,
)
from auto_client_acquisition.support_os.sla import (
    SLATarget,
    compute_sla,
)
from auto_client_acquisition.support_os.ticket import (
    Priority,
    Ticket,
    TicketStatus,
    create_ticket,
)

__all__ = [
    "EscalationDecision",
    "KnowledgeAnswer",
    "Priority",
    "ReplyDraft",
    "SLATarget",
    "SupportCategory",
    "Ticket",
    "TicketStatus",
    "answer_from_knowledge_base",
    "classify_message",
    "compute_sla",
    "create_ticket",
    "draft_response",
    "should_escalate",
]
