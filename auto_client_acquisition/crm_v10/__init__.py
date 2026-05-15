"""CRM v10 — typed object model + lead/deal scoring + customer health.

Twenty CRM-inspired schemas. Pure Pydantic + scoring functions, NO DB,
NO LLM, NO external HTTP. Foundation for a future Twenty CRM real adapter.

Hard rules: Pydantic v2 ``extra="forbid"``; no PII fields; no marketing
claims; deterministic scoring (no random).
"""
from auto_client_acquisition.crm_v10.account_timeline import build_timeline
from auto_client_acquisition.crm_v10.customer_health import compute_health
from auto_client_acquisition.crm_v10.deal_scoring import (
    STAGE_BASE_WIN_PROB,
    score_deal,
)
from auto_client_acquisition.crm_v10.lead_scoring import (
    CANONICAL_SAUDI_B2B_SECTORS,
    PRIORITY_REGIONS,
    URGENCY_TOKENS,
    score_lead,
)
from auto_client_acquisition.crm_v10.object_model import (
    all_object_schemas,
    get_object_schema,
    list_object_types,
)
from auto_client_acquisition.crm_v10.schemas import (
    OBJECT_TYPES,
    Account,
    ApprovalRequestRef,
    Campaign,
    Contact,
    CustomerHealth,
    Deal,
    InvoiceIntent,
    Lead,
    ManualPaymentRecord,
    Opportunity,
    Partner,
    ProofEventRef,
    Proposal,
    ServiceSession,
    SupportTicket,
)
from auto_client_acquisition.crm_v10.stage_machine import (
    DEAL_TRANSITIONS,
    LEAD_TRANSITIONS,
    InvalidStageTransition,
    advance_deal,
    advance_lead,
)


def crm_v10_guardrails() -> dict[str, object]:
    """Canonical guardrails for the CRM v10 module."""
    return {
        "guardrails": {
            "no_llm_calls": True, "no_external_http": True,
            "no_database": True, "approval_required": True,
            "deterministic_scoring": True, "no_pii_fields": True,
        },
        "object_type_count": len(OBJECT_TYPES),
    }


__all__ = [
    "CANONICAL_SAUDI_B2B_SECTORS",
    "DEAL_TRANSITIONS",
    "LEAD_TRANSITIONS",
    "OBJECT_TYPES",
    "PRIORITY_REGIONS",
    "STAGE_BASE_WIN_PROB",
    "URGENCY_TOKENS",
    "Account",
    "ApprovalRequestRef",
    "Campaign",
    "Contact",
    "CustomerHealth",
    "Deal",
    "InvalidStageTransition",
    "InvoiceIntent",
    "Lead",
    "ManualPaymentRecord",
    "Opportunity",
    "Partner",
    "ProofEventRef",
    "Proposal",
    "ServiceSession",
    "SupportTicket",
    "advance_deal",
    "advance_lead",
    "all_object_schemas",
    "build_timeline",
    "compute_health",
    "crm_v10_guardrails",
    "get_object_schema",
    "list_object_types",
    "score_deal",
    "score_lead",
]
