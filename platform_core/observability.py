"""Observability facade — append-only audit events + tracing hooks.

``AuditEvent`` is the schema-stable enterprise audit row. The tracing /
Sentry hooks are re-exported so the foundation has one import surface for
operational visibility.
"""

from __future__ import annotations

from auto_client_acquisition.auditability_os.audit_event import AuditEvent, audit_event_valid
from dealix.observability import instrument_fastapi, setup_sentry, setup_tracing

__all__ = [
    "AuditEvent",
    "audit_event_valid",
    "instrument_fastapi",
    "setup_sentry",
    "setup_tracing",
]
