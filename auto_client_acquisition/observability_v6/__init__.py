"""Observability v6 — minimal trace-record + audit-event helper.

Provides typed records and in-process buffers so any code can emit
data compliant with the trace contract documented in
``docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md``.

Pure stdlib + Pydantic v2 + the existing PII redactor.
NO async. NO I/O. NO file writes. NO external telemetry export.

Public API:
    from auto_client_acquisition.observability_v6 import (
        TraceRecord,
        AuditEvent,
        IncidentSeverity,
        Incident,
        build_correlation_id,
        record_audit,
        list_audit,
        record_incident,
        list_incidents,
    )
"""
from auto_client_acquisition.observability_v6.audit_event import (
    list_audit,
    record_audit,
)
from auto_client_acquisition.observability_v6.correlation import build_correlation_id
from auto_client_acquisition.observability_v6.incident import (
    list_incidents,
    record_incident,
)
from auto_client_acquisition.observability_v6.schemas import (
    AuditEvent,
    Incident,
    IncidentSeverity,
    TraceRecord,
)

__all__ = [
    "AuditEvent",
    "Incident",
    "IncidentSeverity",
    "TraceRecord",
    "build_correlation_id",
    "list_audit",
    "list_incidents",
    "record_audit",
    "record_incident",
]
