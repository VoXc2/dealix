"""In-process append-only audit-event buffer.

Hard rule: the ``action_summary`` field is redacted via
``customer_data_plane.pii_redactor.redact_text`` BEFORE storage so
no raw PII can ever sit in the buffer. Tests pin this.
"""
from __future__ import annotations

import threading

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from auto_client_acquisition.observability_v6.schemas import AuditEvent

_AUDIT_BUFFER: list[AuditEvent] = []
_AUDIT_LOCK = threading.Lock()


def record_audit(event: AuditEvent) -> AuditEvent:
    """Append a redacted copy of ``event`` to the buffer.

    Returns the stored (redacted) record so callers can chain.
    """
    redacted_summary = redact_text(event.action_summary)
    stored = event.model_copy(update={"action_summary": redacted_summary})
    with _AUDIT_LOCK:
        _AUDIT_BUFFER.append(stored)
    return stored


def list_audit(limit: int = 100) -> list[AuditEvent]:
    """Return up to the last ``limit`` events (newest last)."""
    if limit < 0:
        limit = 0
    with _AUDIT_LOCK:
        if limit == 0:
            return []
        return list(_AUDIT_BUFFER[-limit:])


def _reset_audit_buffer() -> None:
    """Test-only helper — clears the in-process buffer."""
    with _AUDIT_LOCK:
        _AUDIT_BUFFER.clear()
