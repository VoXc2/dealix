"""Full-Ops 10-Layer canonical contracts.

These schemas are the THIN SPINE that connects the 10 commercial
operating layers. They do NOT replace existing schemas — they
reference them by id and add the cross-layer envelope fields
(customer_handle, action_mode, safety_summary, evidence pointers).

See: docs/FULL_OPS_10_LAYER_CURRENT_REALITY.md (Phase 0 audit) for
the reuse map this spine sits on top of.
"""
from auto_client_acquisition.full_ops_contracts.schemas import (
    ApprovalRequestEnriched,
    CaseStudyCandidate,
    CustomerBrainSnapshot,
    CustomerHandle,
    CustomerPortalView,
    ExecutivePackRecord,
    LeadOpsRecord,
    PaymentStateRecord,
    ProofEventEnriched,
    ServiceSessionRecord,
    SupportTicketEnriched,
)

__all__ = [
    "ApprovalRequestEnriched",
    "CaseStudyCandidate",
    "CustomerBrainSnapshot",
    "CustomerHandle",
    "CustomerPortalView",
    "ExecutivePackRecord",
    "LeadOpsRecord",
    "PaymentStateRecord",
    "ProofEventEnriched",
    "ServiceSessionRecord",
    "SupportTicketEnriched",
]
