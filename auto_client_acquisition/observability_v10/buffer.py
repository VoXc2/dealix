"""Thread-safe append-only trace buffer.

Hard rule: every record is re-redacted on insert via
``customer_data_plane.pii_redactor.redact_dict`` so no raw PII can
sit in the buffer even if a caller forgot to redact upstream.
"""
from __future__ import annotations

import threading
from typing import Any

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_dict
from auto_client_acquisition.observability_v10.schemas import TraceRecordV10
from auto_client_acquisition.observability_v10.trace_schema import validate_trace

_TRACE_BUFFER: list[TraceRecordV10] = []
_TRACE_LOCK = threading.Lock()


def record_v10_trace(record: dict[str, Any] | TraceRecordV10) -> TraceRecordV10:
    """Validate, redact, and append ``record`` to the buffer.

    Accepts either a plain dict (validated via Pydantic) or an
    already-built :class:`TraceRecordV10` (re-redacted defensively).
    Returns the stored record so callers can chain.
    """
    if isinstance(record, TraceRecordV10):
        redacted_payload = redact_dict(dict(record.redacted_payload or {}))
        stored = record.model_copy(update={"redacted_payload": redacted_payload})
    else:
        validated = validate_trace(record)
        redacted_payload = redact_dict(dict(validated.redacted_payload or {}))
        stored = validated.model_copy(update={"redacted_payload": redacted_payload})
    with _TRACE_LOCK:
        _TRACE_BUFFER.append(stored)
    return stored


def list_v10_traces(limit: int = 100) -> list[TraceRecordV10]:
    """Return up to the last ``limit`` traces (newest last)."""
    if limit < 0:
        limit = 0
    with _TRACE_LOCK:
        if limit == 0:
            return []
        return list(_TRACE_BUFFER[-limit:])


def _reset_v10_buffer() -> None:
    """Test-only helper — clears the in-process buffer."""
    with _TRACE_LOCK:
        _TRACE_BUFFER.clear()
