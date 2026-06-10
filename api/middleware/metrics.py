from __future__ import annotations

import time
from typing import Any, Callable

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Gauge, Histogram, generate_latest, REGISTRY
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

llm_calls_total = Counter(
    "dealix_llm_calls_total",
    "Total LLM calls",
    ["provider", "model", "status"],
)

llm_cost_total = Counter(
    "dealix_llm_cost_total",
    "Total LLM cost in USD",
    ["provider", "model"],
)

agent_calls_total = Counter(
    "dealix_agent_calls_total",
    "Total agent calls",
    ["agent", "status"],
)

pipeline_stage_total = Counter(
    "dealix_pipeline_stage_total",
    "Pipeline stage execution count",
    ["stage"],
)

request_duration_seconds = Histogram(
    "dealix_request_duration_seconds",
    "Request duration in seconds",
    ["method", "endpoint", "status"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0),
)

active_agents = Gauge(
    "dealix_active_agents",
    "Number of currently active agents",
)

active_sessions = Gauge(
    "dealix_active_sessions",
    "Number of currently active sessions",
)

queue_depth = Gauge(
    "dealix_queue_depth",
    "Current queue depth",
    ["queue_name"],
)

llm_latency_seconds = Histogram(
    "dealix_llm_latency_seconds",
    "LLM call latency in seconds",
    ["provider", "model"],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0),
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        exclude_paths: set[str] | None = None,
    ):
        super().__init__(app)
        self.exclude_paths = exclude_paths or {"/metrics", "/health", "/ready"}

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        start = time.time()
        try:
            response = await call_next(request)
        except Exception:
            response = Response(status_code=500)
            raise
        finally:
            duration = time.time() - start
            request_duration_seconds.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code,
            ).observe(duration)

        return response


def track_llm_call(
    provider: str,
    model: str,
    status: str = "success",
    cost: float = 0.0,
    latency_ms: float = 0.0,
) -> None:
    llm_calls_total.labels(provider=provider, model=model, status=status).inc()
    if cost > 0:
        llm_cost_total.labels(provider=provider, model=model).inc(cost)
    if latency_ms > 0:
        llm_latency_seconds.labels(provider=provider, model=model).observe(latency_ms / 1000)


def track_agent_call(agent: str, status: str = "success") -> None:
    agent_calls_total.labels(agent=agent, status=status).inc()


def track_pipeline_stage(stage: str) -> None:
    pipeline_stage_total.labels(stage=stage).inc()


def set_active_agents(count: int) -> None:
    active_agents.set(count)


def set_active_sessions(count: int) -> None:
    active_sessions.set(count)


def set_queue_depth(queue_name: str, depth: int) -> None:
    queue_depth.labels(queue_name=queue_name).set(depth)


def get_metrics_response() -> Response:
    data = generate_latest(REGISTRY)
    return Response(content=data, media_type="text/plain; charset=utf-8")


def setup_metrics(app: FastAPI) -> None:
    @app.get("/metrics")
    async def metrics_endpoint():
        return get_metrics_response()

    app.add_middleware(PrometheusMiddleware)

    @app.on_event("startup")
    async def init_gauges():
        set_active_agents(0)
        set_active_sessions(0)
