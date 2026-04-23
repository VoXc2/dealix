"""Observability: cost tracking, OpenTelemetry tracing, Sentry."""

from dealix.observability.cost_tracker import (
    CostEntry,
    CostTracker,
    MODEL_PRICES,
    estimate_cost_usd,
)
from dealix.observability.otel import (
    agent_span,
    instrument_fastapi,
    instrument_sqlalchemy,
    llm_span,
    setup_tracing,
    tool_span,
)
from dealix.observability.sentry import setup_sentry

__all__ = [
    "CostEntry",
    "CostTracker",
    "MODEL_PRICES",
    "agent_span",
    "estimate_cost_usd",
    "instrument_fastapi",
    "instrument_sqlalchemy",
    "llm_span",
    "setup_sentry",
    "setup_tracing",
    "tool_span",
]
