"""Wave 8 §10 — OpenTelemetry Adapter.

Wraps opentelemetry-sdk with graceful fallback when OTEL_EXPORTER_OTLP_ENDPOINT
is not configured. All operations are fail-safe.
"""
from __future__ import annotations

import logging
import os
import uuid
from typing import Any

from auto_client_acquisition.observability_adapters.base import (
    BaseObservabilityAdapter,
    ObservabilityEvent,
)

logger = logging.getLogger(__name__)

_OTEL_AVAILABLE = False
try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    _OTEL_AVAILABLE = True
except ImportError:
    pass


class OtelAdapter(BaseObservabilityAdapter):
    """OpenTelemetry tracing adapter.

    Configures a TracerProvider with OTLP export if OTEL_EXPORTER_OTLP_ENDPOINT
    is set; otherwise uses a no-op console exporter or pure noop.

    Never raises. Never logs PII or raw stacktraces.
    """

    adapter_name = "otel"

    def __init__(self) -> None:
        self._provider = None
        self._tracer = None
        self._active_spans: dict[str, Any] = {}
        self._setup()

    def _setup(self) -> None:
        if not _OTEL_AVAILABLE:
            logger.debug("OtelAdapter: opentelemetry-sdk not installed; using noop")
            return

        try:
            endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "")
            service_name = os.environ.get("OTEL_SERVICE_NAME", "dealix")

            from opentelemetry.sdk.resources import Resource
            resource = Resource.create({"service.name": service_name})
            self._provider = TracerProvider(resource=resource)

            if endpoint:
                try:
                    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
                    exporter = OTLPSpanExporter(endpoint=endpoint)
                    self._provider.add_span_processor(BatchSpanProcessor(exporter))
                    logger.info("OtelAdapter: OTLP exporter configured → %s", endpoint)
                except Exception as exc:
                    logger.warning("OtelAdapter: OTLP exporter setup failed (%s); falling back to noop", exc)
            else:
                logger.debug("OtelAdapter: OTEL_EXPORTER_OTLP_ENDPOINT not set; noop mode")

            trace.set_tracer_provider(self._provider)
            self._tracer = trace.get_tracer("dealix.auto_client_acquisition")
        except Exception as exc:
            logger.warning("OtelAdapter._setup failed: %s", exc)
            self._provider = None
            self._tracer = None

    def is_configured(self) -> bool:
        return _OTEL_AVAILABLE and bool(os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT"))

    def emit(self, event: ObservabilityEvent) -> None:
        if not self._tracer:
            return
        try:
            with self._tracer.start_as_current_span(event.event_type) as span:
                span.set_attribute("customer_handle", event.customer_handle)
                span.set_attribute("model", event.model)
                span.set_attribute("prompt_tokens", event.prompt_tokens)
                span.set_attribute("completion_tokens", event.completion_tokens)
                span.set_attribute("latency_ms", event.latency_ms)
                span.set_attribute("success", event.success)
                if event.error_type:
                    span.set_attribute("error_type", event.error_type)
        except Exception as exc:
            logger.debug("OtelAdapter.emit failed (noop): %s", exc)

    def start_trace(self, name: str, metadata: dict | None = None) -> str:
        if not self._tracer:
            return ""
        try:
            span = self._tracer.start_span(name)
            trace_id = str(uuid.uuid4())
            self._active_spans[trace_id] = span
            return trace_id
        except Exception as exc:
            logger.debug("OtelAdapter.start_trace failed: %s", exc)
            return ""

    def end_trace(self, trace_id: str, success: bool = True, error_type: str = "") -> None:
        span = self._active_spans.pop(trace_id, None)
        if span:
            try:
                span.set_attribute("success", success)
                if error_type:
                    span.set_attribute("error_type", error_type)
                span.end()
            except Exception as exc:
                logger.debug("OtelAdapter.end_trace failed: %s", exc)

    def flush(self) -> None:
        if self._provider:
            try:
                self._provider.force_flush()
            except Exception as exc:
                logger.debug("OtelAdapter.flush failed: %s", exc)
