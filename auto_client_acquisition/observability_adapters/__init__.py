"""Wave 8 §10 — Observability Adapters.

Provides pluggable observability backends:
- OtelAdapter: OpenTelemetry tracing
- LangfuseAdapter: LLM trace + eval logging
- Redaction: PII scrubbing before log emission

All adapters are non-blocking; missing credentials = noop, never raises.
"""
from __future__ import annotations

from auto_client_acquisition.observability_adapters.base import (
    BaseObservabilityAdapter,
    NoopAdapter,
    ObservabilityEvent,
)
from auto_client_acquisition.observability_adapters.langfuse_adapter import LangfuseAdapter
from auto_client_acquisition.observability_adapters.otel_adapter import OtelAdapter
from auto_client_acquisition.observability_adapters.redaction import RedactionFilter

__all__ = [
    "BaseObservabilityAdapter",
    "LangfuseAdapter",
    "NoopAdapter",
    "ObservabilityEvent",
    "OtelAdapter",
    "RedactionFilter",
]
