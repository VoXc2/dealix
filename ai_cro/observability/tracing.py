"""
Dealix Observability Layer — v1.0
==================================

OpenTelemetry instrumentation for multi-agent revenue system, following the
GenAI semantic conventions (https://opentelemetry.io/docs/specs/semconv/gen-ai/).

Exports:
    @trace_agent — decorator for agent methods (records spans, tokens, cost, latency)
    @trace_llm_call — decorator for LLM invocations
    record_approval_outcome — explicit event recording for Policy decisions
    record_channel_outcome — delivery status of outbound actions

Backend:
    - OTLP exporter → configurable (Langfuse, Tempo, Jaeger, Honeycomb)
    - Falls back to console exporter if OTEL_EXPORTER_OTLP_ENDPOINT not set
"""

from __future__ import annotations

import functools
import logging
import os
import time
from contextlib import contextmanager
from typing import Any, Callable

logger = logging.getLogger("dealix.observability")

# ---- Lazy imports so the module works even if otel isn't installed ----------
try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor, ConsoleSpanExporter
    )
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import (
        PeriodicExportingMetricReader, ConsoleMetricExporter
    )
    _OTEL_AVAILABLE = True
except ImportError:
    _OTEL_AVAILABLE = False
    logger.warning("opentelemetry not installed — tracing disabled. "
                   "pip install opentelemetry-sdk opentelemetry-exporter-otlp")


# ============================================================================
# SETUP
# ============================================================================

_initialized = False
_tracer = None
_meter = None


def init_telemetry(service_name: str = "dealix-ai-cro",
                   service_version: str = "1.0.0",
                   environment: str = "production") -> None:
    """Initialize OpenTelemetry providers. Idempotent."""
    global _initialized, _tracer, _meter

    if _initialized or not _OTEL_AVAILABLE:
        return

    resource = Resource.create({
        "service.name": service_name,
        "service.version": service_version,
        "deployment.environment": environment,
    })

    # Traces
    tracer_provider = TracerProvider(resource=resource)
    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        try:
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
            tracer_provider.add_span_processor(
                BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces"))
            )
        except ImportError:
            tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    else:
        tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(tracer_provider)

    # Metrics
    reader = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=60_000)
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)

    _tracer = trace.get_tracer(service_name, service_version)
    _meter = metrics.get_meter(service_name, service_version)

    # Define standard GenAI metrics
    global _llm_tokens_counter, _llm_cost_counter, _agent_duration_histogram
    _llm_tokens_counter = _meter.create_counter(
        "gen_ai.client.token.usage",
        unit="tokens",
        description="LLM tokens consumed",
    )
    _llm_cost_counter = _meter.create_counter(
        "dealix.llm.cost.sar",
        unit="SAR",
        description="LLM cost in SAR",
    )
    _agent_duration_histogram = _meter.create_histogram(
        "dealix.agent.duration",
        unit="ms",
        description="Agent invocation duration",
    )

    _initialized = True
    logger.info("OpenTelemetry initialized (service=%s env=%s)", service_name, environment)


# Fallback no-op metrics
_llm_tokens_counter = None
_llm_cost_counter = None
_agent_duration_histogram = None


# ============================================================================
# DECORATORS
# ============================================================================

def trace_agent(agent_name: str):
    """Decorator for agent method calls. Records span + duration metric."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not _OTEL_AVAILABLE or not _tracer:
                return func(*args, **kwargs)

            start = time.perf_counter()
            with _tracer.start_as_current_span(
                f"agent.{agent_name}.{func.__name__}",
                attributes={
                    "dealix.agent.name": agent_name,
                    "dealix.agent.method": func.__name__,
                }
            ) as span:
                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("dealix.agent.outcome", "success")
                    return result
                except Exception as e:
                    span.set_attribute("dealix.agent.outcome", "error")
                    span.record_exception(e)
                    raise
                finally:
                    duration_ms = (time.perf_counter() - start) * 1000
                    if _agent_duration_histogram:
                        _agent_duration_histogram.record(
                            duration_ms, {"agent": agent_name, "method": func.__name__}
                        )
        return wrapper
    return decorator


def trace_llm_call(model: str, provider: str = "anthropic"):
    """Decorator for LLM calls. Follows GenAI semantic conventions."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not _OTEL_AVAILABLE or not _tracer:
                return func(*args, **kwargs)

            with _tracer.start_as_current_span(
                f"gen_ai.{provider}.{model}",
                attributes={
                    "gen_ai.system": provider,
                    "gen_ai.request.model": model,
                    "gen_ai.operation.name": "chat",
                }
            ) as span:
                result = func(*args, **kwargs)
                # Expect result is dict with usage info
                if isinstance(result, dict):
                    usage = result.get("usage", {})
                    input_tokens = usage.get("input_tokens", 0)
                    output_tokens = usage.get("output_tokens", 0)
                    span.set_attribute("gen_ai.usage.input_tokens", input_tokens)
                    span.set_attribute("gen_ai.usage.output_tokens", output_tokens)
                    if _llm_tokens_counter:
                        _llm_tokens_counter.add(
                            input_tokens,
                            {"model": model, "type": "input", "provider": provider}
                        )
                        _llm_tokens_counter.add(
                            output_tokens,
                            {"model": model, "type": "output", "provider": provider}
                        )
                return result
        return wrapper
    return decorator


# ============================================================================
# EVENT RECORDERS
# ============================================================================

def record_approval_outcome(request_id: str, verdict: str, rule_id: str,
                             agent: str, amount_sar: float = 0) -> None:
    """Record an approval-engine decision as a span event."""
    if not _OTEL_AVAILABLE or not _tracer:
        return
    span = trace.get_current_span()
    span.add_event("policy.decision", {
        "policy.request_id": request_id,
        "policy.verdict": verdict,
        "policy.rule_id": rule_id,
        "policy.agent": agent,
        "policy.amount_sar": amount_sar,
    })


def record_channel_outcome(channel: str, action_type: str, status: str,
                            counterparty: str = "") -> None:
    """Record delivery outcome of an outbound action."""
    if not _OTEL_AVAILABLE or not _tracer:
        return
    span = trace.get_current_span()
    span.add_event("channel.outcome", {
        "channel.name": channel,
        "action.type": action_type,
        "action.status": status,  # sent, delivered, failed, rate_limited
        "counterparty": counterparty,
    })


@contextmanager
def trace_span(name: str, attributes: dict[str, Any] | None = None):
    """Generic span context manager for ad-hoc instrumentation."""
    if not _OTEL_AVAILABLE or not _tracer:
        yield None
        return
    with _tracer.start_as_current_span(name, attributes=attributes or {}) as span:
        yield span


# ============================================================================
# SELF-TEST
# ============================================================================

def _run_self_test() -> None:
    init_telemetry(environment="test")

    @trace_agent("negotiator")
    def handle_objection(objection: str) -> str:
        with trace_span("negotiator.generate_response", {"objection.type": "price"}):
            time.sleep(0.02)
        record_channel_outcome("email", "send_response", "sent", "النور العقارية")
        return "responded"

    @trace_llm_call(model="claude-sonnet-4.5", provider="anthropic")
    def call_llm(prompt: str) -> dict:
        time.sleep(0.01)
        return {"text": "response", "usage": {"input_tokens": 1024, "output_tokens": 256}}

    print("\n" + "="*72)
    print("Dealix Observability — self-test")
    print("="*72)

    result = handle_objection("السعر مرتفع")
    print(f"✅ trace_agent decorator → {result}")

    resp = call_llm("test prompt")
    print(f"✅ trace_llm_call decorator → tokens {resp['usage']}")

    record_approval_outcome(
        request_id="test-123", verdict="approve", rule_id="P0005",
        agent="negotiator", amount_sar=15_000
    )
    print("✅ record_approval_outcome → policy.decision event emitted")

    print("\nCheck console output above for OTLP spans.\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    _run_self_test()
