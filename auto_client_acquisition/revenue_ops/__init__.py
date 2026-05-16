"""Governed Revenue Ops domain package."""

from auto_client_acquisition.revenue_ops.schemas import (
    DiagnosticRequest,
    EvidenceEventRequest,
    FollowUpDraftRequest,
    InvoiceDraftRequest,
    RevenueOpsState,
    ScoreRequest,
    UploadRequest,
)
from auto_client_acquisition.revenue_ops.store import (
    add_upload,
    apply_transition,
    attach_approval_id,
    create_diagnostic,
    create_follow_up_drafts,
    get_record,
    list_records,
    record_evidence_event,
    score_opportunities,
)

__all__ = [
    "DiagnosticRequest",
    "EvidenceEventRequest",
    "FollowUpDraftRequest",
    "InvoiceDraftRequest",
    "RevenueOpsState",
    "ScoreRequest",
    "UploadRequest",
    "add_upload",
    "apply_transition",
    "attach_approval_id",
    "create_diagnostic",
    "create_follow_up_drafts",
    "get_record",
    "list_records",
    "record_evidence_event",
    "score_opportunities",
]
