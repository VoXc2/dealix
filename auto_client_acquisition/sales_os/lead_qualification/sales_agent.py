"""Sales qualification agent — a thin, identity-bound agent.

The agent has an ``AgentCard`` (no agent without identity) at autonomy
level 1 (draft-only — it never auto-sends). It produces draft response
copy only; the orchestrator owns every side effect (approval, CRM,
metrics). Every draft is prefixed with an explicit draft label so it can
never be mistaken for an approved, sendable message.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from auto_client_acquisition.agent_os.agent_card import AgentCard, agent_card_valid
from auto_client_acquisition.agent_os.agent_registry import get_agent, register_agent
from auto_client_acquisition.sales_os.lead_qualification.schemas import LeadInput

SALES_AGENT_ID = "sales_agent"

SALES_AGENT_CARD = AgentCard(
    agent_id=SALES_AGENT_ID,
    name="Sales Qualification Agent",
    owner="founder",
    purpose="Qualify inbound leads and draft governed responses pending founder approval",
    autonomy_level=1,  # draft-only — never auto-sends
    status="active",
)

DRAFT_LABEL = "[DRAFT — pending approval | مسودة — بانتظار الموافقة]"

# An LLM hook is injected so production can swap a real model in; tests
# pass a deterministic stub. Signature: (lead, verdict, cited_context) -> str.
DraftLLM = Callable[[LeadInput, str, dict[str, Any]], str]


def register_sales_agent() -> AgentCard:
    """Register the sales agent identity (idempotent)."""
    register_agent(SALES_AGENT_CARD)
    return SALES_AGENT_CARD


def ensure_sales_agent_identity() -> AgentCard:
    """Guarantee the agent has a valid registered identity before it runs."""
    card = get_agent(SALES_AGENT_ID)
    if card is None:
        card = register_sales_agent()
    if not agent_card_valid(card):
        raise ValueError("sales_agent identity invalid")
    return card


def _default_draft(lead: LeadInput, verdict: str, cited_context: dict[str, Any]) -> str:
    """Deterministic bilingual draft body (no LLM, no forbidden language)."""
    has_context = bool(cited_context.get("citations"))
    context_note_en = (
        "Grounded in your shared materials."
        if has_context
        else "We will confirm details with you before any next step."
    )
    context_note_ar = (
        "مستند إلى المواد التي شاركتموها."
        if has_context
        else "سنؤكد التفاصيل معكم قبل أي خطوة تالية."
    )
    return (
        f"مرحبًا فريق {lead.company_name}،\n"
        f"شكرًا لتواصلكم. بعد مراجعة أولية، نتيجة التأهيل: {verdict}. {context_note_ar}\n"
        "هذه مسودة داخلية بانتظار موافقة المؤسس قبل الإرسال.\n\n"
        f"Hello {lead.company_name} team,\n"
        f"Thank you for reaching out. Initial qualification verdict: {verdict}. {context_note_en}\n"
        "This is an internal draft pending founder approval before any send."
    )


def draft_response(
    lead: LeadInput,
    verdict: str,
    cited_context: dict[str, Any],
    *,
    llm: DraftLLM | None = None,
) -> str:
    """Produce a labeled draft response. Never sends anything."""
    body = (
        llm(lead, verdict, cited_context)
        if llm is not None
        else _default_draft(lead, verdict, cited_context)
    )
    return f"{DRAFT_LABEL}\n\n{body}"


__all__ = [
    "DRAFT_LABEL",
    "SALES_AGENT_CARD",
    "SALES_AGENT_ID",
    "DraftLLM",
    "draft_response",
    "ensure_sales_agent_identity",
    "register_sales_agent",
]
