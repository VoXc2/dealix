"""Privacy-safe OpenTelemetry setup for Dealix.

The module instruments FastAPI, SQLAlchemy and HTTPX and provides bounded
GenAI/agent/tool spans. OTLP is an observability transport only; it is never a
business-truth owner. Prompt, message, customer, payload and secret content is
not captured by these helpers.
"""

from __future__ import annotations

import logging
import os
import re
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any

log = logging.getLogger(__name__)

try:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    _HAS_OTEL = True
except ImportError:  # pragma: no cover - observability is an optional dependency group
    _HAS_OTEL = False


_tracer: Any = None
_tracing_configured = False
_httpx_instrumented = False
_sqlalchemy_engine_ids: set[int] = set()

_SAFE_LABEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,127}$")

# Public callers may keep passing **attrs, but only these low-cardinality keys
# can leave the process. Unknown keys are dropped rather than exported.
_SAFE_ATTRIBUTE_MAP: dict[str, str] = {
    "operation_name": "gen_ai.operation.name",
    "provider_name": "gen_ai.provider.name",
    "workload_id": "dealix.workload.id",
    "evidence_id": "dealix.evidence.id",
    "authority_class": "dealix.authority.class",
    "result": "dealix.result",
    "source_sha": "dealix.source.sha",
    "cost_usd": "dealix.cost.usd",
    "elapsed_ms": "dealix.elapsed.ms",
    "founder_minutes": "dealix.founder.minutes",
    "agent_minutes": "dealix.agent.minutes",
}

_NUMERIC_ATTRIBUTE_KEYS = {
    "cost_usd",
    "elapsed_ms",
    "founder_minutes",
    "agent_minutes",
}

# Defense-in-depth: even if a sensitive name is accidentally added to the
# allowlist later, it must remain blocked here unless deliberately redesigned.
_SENSITIVE_KEY_FRAGMENTS = {
    "prompt",
    "input",
    "output",
    "content",
    "message",
    "customer",
    "contact",
    "email",
    "phone",
    "payload",
    "body",
    "header",
    "cookie",
    "authorization",
    "token",
    "secret",
    "password",
    "key",
    "url",
    "query",
    "document",
    "attachment",
}


def _safe_label(value: Any, *, fallback: str = "redacted_unclassified") -> str:
    """Return a bounded low-cardinality label or a non-sensitive fallback."""
    text = str(value).strip()
    if not text or not _SAFE_LABEL_RE.fullmatch(text):
        return fallback
    return text


def _safe_number(value: Any) -> int | float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if value < 0:
        return None
    return value


def safe_span_attributes(attrs: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Map explicitly allowed Dealix attrs to privacy-safe OTel attributes.

    No raw prompt/message/customer/payload/URL/header/token data is accepted.
    String attributes are restricted to low-cardinality identifier-like labels.
    """
    if not attrs:
        return {}

    sanitized: dict[str, Any] = {}
    for raw_key, value in attrs.items():
        key = str(raw_key).strip().lower()
        if any(fragment in key for fragment in _SENSITIVE_KEY_FRAGMENTS):
            continue
        target = _SAFE_ATTRIBUTE_MAP.get(key)
        if target is None:
            continue
        if key in _NUMERIC_ATTRIBUTE_KEYS:
            number = _safe_number(value)
            if number is not None:
                sanitized[target] = number
            continue
        sanitized[target] = _safe_label(value)
    return sanitized


def _parse_headers(value: str) -> dict[str, str]:
    """Parse OTLP headers without logging or otherwise exposing them."""
    headers: dict[str, str] = {}
    for item in value.split(","):
        if "=" not in item:
            continue
        name, header_value = item.split("=", 1)
        name = name.strip()
        header_value = header_value.strip()
        if name and header_value:
            headers[name] = header_value
    return headers


def setup_tracing(service_name: str = "dealix-api", version: str = "3.0.0") -> None:
    """Initialize OTel once. Safe and silent if optional OTel is unavailable."""
    global _tracer, _tracing_configured
    if _tracing_configured:
        return
    if not _HAS_OTEL:
        log.info("otel_unavailable — tracing disabled")
        return

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip()
    if not endpoint:
        log.info("otel_not_configured — tracing disabled")
        return

    resource = Resource.create(
        {
            "service.name": _safe_label(service_name, fallback="dealix-service"),
            "service.version": _safe_label(version, fallback="unknown"),
            "deployment.environment.name": _safe_label(
                os.getenv("APP_ENV", "production"),
                fallback="unknown",
            ),
        }
    )
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(
        endpoint=endpoint,
        headers=_parse_headers(os.getenv("OTEL_EXPORTER_OTLP_HEADERS", "")),
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    _tracer = trace.get_tracer(service_name, version)
    _tracing_configured = True

    # Never log endpoint or OTLP headers: either may contain credentials or
    # tenant-identifying values depending on the collector/provider.
    log.info("otel_enabled", extra={"service_name": resource.attributes.get("service.name")})


def instrument_fastapi(app: Any) -> None:
    """Instrument FastAPI/HTTPX once without changing application authority."""
    global _httpx_instrumented
    if not _HAS_OTEL or _tracer is None:
        return
    if not getattr(app, "_dealix_otel_instrumented", False):
        FastAPIInstrumentor.instrument_app(app)
        try:
            setattr(app, "_dealix_otel_instrumented", True)
        except Exception:  # pragma: no cover - unusual framework wrapper
            pass
    if not _httpx_instrumented:
        HTTPXClientInstrumentor().instrument()
        _httpx_instrumented = True


def instrument_sqlalchemy(engine: Any) -> None:
    """Instrument each SQLAlchemy engine at most once."""
    if not _HAS_OTEL or _tracer is None or engine is None:
        return
    engine_id = id(engine)
    if engine_id in _sqlalchemy_engine_ids:
        return
    SQLAlchemyInstrumentor().instrument(engine=engine)
    _sqlalchemy_engine_ids.add(engine_id)


@contextmanager
def llm_span(model: str, task: str, **attrs: Any) -> Iterator[Any]:
    """Create a bounded GenAI span without prompt or message content."""
    if not _HAS_OTEL or _tracer is None:
        yield None
        return

    attributes = {
        "gen_ai.request.model": _safe_label(model),
        "dealix.task": _safe_label(task),
        **safe_span_attributes(attrs),
    }
    with _tracer.start_as_current_span("gen_ai.operation", attributes=attributes) as span:
        yield span


@contextmanager
def agent_span(agent_name: str, **attrs: Any) -> Iterator[Any]:
    """Create a stable agent span with an allowlisted attribute surface."""
    if not _HAS_OTEL or _tracer is None:
        yield None
        return
    attributes = {
        "gen_ai.agent.name": _safe_label(agent_name),
        **safe_span_attributes(attrs),
    }
    with _tracer.start_as_current_span("gen_ai.agent", attributes=attributes) as span:
        yield span


@contextmanager
def tool_span(tool_name: str, **attrs: Any) -> Iterator[Any]:
    """Create a stable tool span without serializing tool inputs/outputs."""
    if not _HAS_OTEL or _tracer is None:
        yield None
        return
    attributes = {
        "dealix.tool.name": _safe_label(tool_name),
        **safe_span_attributes(attrs),
    }
    with _tracer.start_as_current_span("dealix.tool", attributes=attributes) as span:
        yield span


__all__ = [
    "agent_span",
    "instrument_fastapi",
    "instrument_sqlalchemy",
    "llm_span",
    "safe_span_attributes",
    "setup_tracing",
    "tool_span",
]
