"""Observability v10 — Langfuse + OpenTelemetry-aligned trace schema.

Extends ``observability_v6`` with cost + risk + model fields. Pure
in-memory; no external telemetry exporter, no I/O.

Public API::

    from auto_client_acquisition.observability_v10 import (
        TraceRecordV10,
        SpanRecord,
        record_v10_trace,
        list_v10_traces,
        validate_trace,
        _reset_v10_buffer,
    )
"""
from auto_client_acquisition.observability_v10.buffer import (
    _reset_v10_buffer,
    list_v10_traces,
    record_v10_trace,
)
from auto_client_acquisition.observability_v10.contract_registry import (
    ALLOWED_EVENT_TYPES,
    REQUIRED_FIELDS,
    ContractValidation,
    validate_observability_event,
)
from auto_client_acquisition.observability_v10.contract_trace_hook import record_contract_trace_event
from auto_client_acquisition.observability_v10.report import summarize_traces
from auto_client_acquisition.observability_v10.schemas import (
    SpanRecord,
    TraceRecordV10,
)
from auto_client_acquisition.observability_v10.trace_schema import validate_trace

__all__ = [
    "SpanRecord",
    "TraceRecordV10",
    "ALLOWED_EVENT_TYPES",
    "REQUIRED_FIELDS",
    "ContractValidation",
    "_reset_v10_buffer",
    "list_v10_traces",
    "record_v10_trace",
    "record_contract_trace_event",
    "summarize_traces",
    "validate_trace",
    "validate_observability_event",
]
