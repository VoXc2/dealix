"""Auditability OS — deterministic audit primitives for Enterprise Trust wave."""

from __future__ import annotations

from auto_client_acquisition.auditability_os.audit_event import (
    AuditEvent,
    AuditEventKind,
    AuditRecord,
    audit_event_valid,
    clear_for_test,
    list_events,
    record_event,
)
from auto_client_acquisition.auditability_os.audit_metrics import AUDIT_METRIC_KEYS, audit_metrics_coverage_score
from auto_client_acquisition.auditability_os.evidence_chain import (
    EVIDENCE_CHAIN_STAGES,
    EvidenceChain,
    EvidenceNode,
    build_chain,
    evidence_chain_complete,
)
from auto_client_acquisition.auditability_os.policy_check_log import PolicyCheckLogEntry
from auto_client_acquisition.auditability_os.responsibility_attribution import (
    ResponsibilityAttribution,
    attribution_valid,
)

__all__ = [
    "AUDIT_METRIC_KEYS",
    "EVIDENCE_CHAIN_STAGES",
    "AuditEvent",
    "AuditEventKind",
    "AuditRecord",
    "EvidenceChain",
    "EvidenceNode",
    "PolicyCheckLogEntry",
    "ResponsibilityAttribution",
    "attribution_valid",
    "audit_event_valid",
    "audit_metrics_coverage_score",
    "build_chain",
    "clear_for_test",
    "evidence_chain_complete",
    "list_events",
    "record_event",
]
