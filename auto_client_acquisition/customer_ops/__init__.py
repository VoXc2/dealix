"""Customer Operations Kernel — thin reusable layer over canonical Dealix truth.

Reuses (never duplicates):
- auto_client_acquisition/whatsapp_client_os (inbound guard, permission ladder)
- auto_client_acquisition/support_os (classifier, escalation, responder)
- auto_client_acquisition/customer_data_plane (consent registry, contactability)
- auto_client_acquisition/channel_policy_gateway + safe_send_gateway (channel policy)
- auto_client_acquisition/approval_center + proof_ledger + revenue_memory
- auto_client_acquisition/knowledge_v10 (allow-listed retrieval)
- auto_client_acquisition/vertical_playbooks + service_catalog (sector refs)
- auto_client_acquisition/agent_observability + dealix.contracts (telemetry/envelope)
- dealix.commercial.market_intelligence + intelligence (official/public sources)

L0-L4 only: draft/answer/ask/escalate/hold. No live send, no charge, no
scraping, no cold outbound, no scheduler/CRM/model-router/chatbot duplication.
"""

from auto_client_acquisition.customer_ops.channels import (
    enforce_channel_policy,
    enforce_whatsapp_inbound_only,
)
from auto_client_acquisition.customer_ops.event_contract import (
    CANONICAL_EVENT_FIELDS,
    NON_RELATIONSHIP_SOURCES,
    RELATIONSHIP_EVIDENCE_SOURCES,
    CustomerOpsEvent,
    has_relationship_evidence,
    new_case_id,
    new_trace_id,
)
from auto_client_acquisition.customer_ops.market_intel import (
    official_sector_brief,
    watch_signals,
)
from auto_client_acquisition.customer_ops.pipeline import (
    CustomerOpsOutcome,
    run_customer_ops_event,
)
from auto_client_acquisition.customer_ops.provenance import (
    PROVENANCE_KEY,
    PROVENANCE_VERSION,
    attach_provenance_to_approval,
    attach_provenance_to_proof_event,
    build_provenance_attachment,
    build_relationship_refs,
    build_snapshot_provenance,
    case_evidence_ids,
    new_approval_request_for_outcome,
    new_proof_event_for_outcome,
    provenance_status_of,
    require_current_provenance,
)
from auto_client_acquisition.customer_ops.retrieval import (
    KnowledgeSnapshot,
    current_only_retrieve,
)
from auto_client_acquisition.customer_ops.sector_packs import (
    SECTOR_PACK_VERSION,
    SectorPack,
    get_sector_pack,
    list_sector_packs,
)
from auto_client_acquisition.customer_ops.telemetry import extend_trace_payload

__all__ = [
    "CANONICAL_EVENT_FIELDS",
    "NON_RELATIONSHIP_SOURCES",
    "PROVENANCE_KEY",
    "PROVENANCE_VERSION",
    "RELATIONSHIP_EVIDENCE_SOURCES",
    "SECTOR_PACK_VERSION",
    "CustomerOpsEvent",
    "CustomerOpsOutcome",
    "KnowledgeSnapshot",
    "SectorPack",
    "attach_provenance_to_approval",
    "attach_provenance_to_proof_event",
    "build_provenance_attachment",
    "build_relationship_refs",
    "build_snapshot_provenance",
    "case_evidence_ids",
    "current_only_retrieve",
    "enforce_channel_policy",
    "enforce_whatsapp_inbound_only",
    "extend_trace_payload",
    "get_sector_pack",
    "has_relationship_evidence",
    "list_sector_packs",
    "new_approval_request_for_outcome",
    "new_case_id",
    "new_proof_event_for_outcome",
    "new_trace_id",
    "official_sector_brief",
    "provenance_status_of",
    "require_current_provenance",
    "run_customer_ops_event",
    "watch_signals",
]
