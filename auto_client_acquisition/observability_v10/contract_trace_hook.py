"""Bridge observability contract events into TraceRecordV10 storage (in-process buffer)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.observability_v10.buffer import record_v10_trace
from auto_client_acquisition.observability_v10.contract_registry import validate_observability_event
from auto_client_acquisition.observability_v10.schemas import TraceRecordV10


def record_contract_trace_event(
    *,
    tenant_id: str,
    correlation_id: str,
    run_id: str,
    event_type: str,
    source_module: str,
    actor: str,
    occurred_at: str | None = None,
    payload_schema_version: int = 1,
    extra_payload: dict[str, Any] | None = None,
) -> TraceRecordV10:
    """Validate a contract-shaped event, then persist as a trace record with redacted_payload carrying lineage fields."""
    event: dict[str, Any] = {
        "tenant_id": tenant_id,
        "correlation_id": correlation_id,
        "run_id": run_id,
        "event_type": event_type,
        "source_module": source_module,
        "actor": actor,
        "occurred_at": occurred_at or datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "payload_schema_version": payload_schema_version,
    }
    if extra_payload:
        event.update(extra_payload)
    validation = validate_observability_event(event)
    if not validation.valid:
        raise ValueError(f"contract_validation_failed:{','.join(validation.errors)}")

    trace = TraceRecordV10(
        correlation_id=correlation_id,
        workflow_id=run_id,
        redacted_payload=dict(event),
        created_at=datetime.now(UTC),
    )
    return record_v10_trace(trace)


__all__ = ["record_contract_trace_event"]
