"""Canonical Auditability OS — every decision can be explained.

Composes existing proof_ledger + governance_os.runtime_decision history
+ approval_center + friction_log into a single audit chain export.

Wave 3 preview — enterprise procurement-ready.
"""
from auto_client_acquisition.auditability_os.audit_event import (
    AuditEvent,
    AuditEventKind,
    record_event,
    list_events,
)
from auto_client_acquisition.auditability_os.evidence_chain import (
    EvidenceChain,
    build_chain,
)

__all__ = [
    "AuditEvent",
    "AuditEventKind",
    "EvidenceChain",
    "build_chain",
    "list_events",
    "record_event",
]
