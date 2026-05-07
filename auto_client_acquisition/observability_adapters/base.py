"""Wave 8 §10 — Base Observability Adapter."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ObservabilityEvent:
    """Structured event for observability emission."""
    event_type: str                           # e.g. "llm_call", "lead_scored", "approval_triggered"
    customer_handle: str = ""                 # customer identifier (never PII)
    trace_id: str = ""
    span_id: str = ""
    model: str = ""                           # LLM model name
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_ms: float = 0.0
    success: bool = True
    error_type: str = ""                      # safe error label, not raw stacktrace
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "customer_handle": self.customer_handle,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "model": self.model,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "latency_ms": self.latency_ms,
            "success": self.success,
            "error_type": self.error_type,
            "metadata": self.metadata,
        }


class BaseObservabilityAdapter:
    """Abstract base for observability adapters.

    All methods are fail-safe: missing credentials or errors = noop + log warning.
    Never raises. Never exposes PII or raw stacktraces externally.
    """

    adapter_name: str = "base"

    def is_configured(self) -> bool:
        """Return True if this adapter has valid credentials."""
        return False

    def emit(self, event: ObservabilityEvent) -> None:
        """Emit an observability event. Fail-safe — never raises."""
        raise NotImplementedError

    def start_trace(self, name: str, metadata: dict | None = None) -> str:
        """Start a trace. Returns trace_id or empty string."""
        return ""

    def end_trace(self, trace_id: str, success: bool = True, error_type: str = "") -> None:
        """End a trace. Fail-safe."""
        pass

    def flush(self) -> None:
        """Flush any buffered events. Fail-safe."""
        pass


class NoopAdapter(BaseObservabilityAdapter):
    """No-op adapter used when observability is not configured.

    Returns safe defaults. All operations succeed silently.
    """

    adapter_name = "noop"

    def is_configured(self) -> bool:
        return True  # Always "configured" — it just does nothing

    def emit(self, event: ObservabilityEvent) -> None:
        logger.debug("NoopAdapter.emit: %s (observability not configured)", event.event_type)

    def start_trace(self, name: str, metadata: dict | None = None) -> str:
        return ""

    def end_trace(self, trace_id: str, success: bool = True, error_type: str = "") -> None:
        pass

    def flush(self) -> None:
        pass


def get_adapter(adapter_type: str = "noop") -> BaseObservabilityAdapter:
    """Factory: return the appropriate adapter. Falls back to NoopAdapter on any error."""
    try:
        if adapter_type == "otel":
            from auto_client_acquisition.observability_adapters.otel_adapter import OtelAdapter
            return OtelAdapter()
        if adapter_type == "langfuse":
            from auto_client_acquisition.observability_adapters.langfuse_adapter import LangfuseAdapter
            return LangfuseAdapter()
    except Exception as exc:
        logger.warning("Failed to initialize %s adapter: %s — falling back to noop", adapter_type, exc)
    return NoopAdapter()
