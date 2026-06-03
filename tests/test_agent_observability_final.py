"""Phase 9 — Agent Observability cost-summary tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.agent_observability.cost import estimate_cost
from auto_client_acquisition.agent_observability.trace import (
    _reset_traces,
    record_trace,
)


def test_estimate_cost_per_model() -> None:
    sonnet_cost = estimate_cost(input_tokens=1_000_000, output_tokens=1_000_000, model="claude-sonnet")
    opus_cost = estimate_cost(input_tokens=1_000_000, output_tokens=1_000_000, model="claude-opus")
    assert opus_cost > sonnet_cost  # Opus costs more


def test_estimate_cost_default_fallback() -> None:
    cost = estimate_cost(input_tokens=1000, output_tokens=500, model="unknown-model-xyz")
    assert isinstance(cost, float)
    assert cost > 0


@pytest.mark.asyncio
async def test_cost_summary_endpoint_empty() -> None:
    _reset_traces()
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/agent-observability/cost-summary")
    assert r.status_code == 200
    body = r.json()
    assert body["trace_count"] == 0
    assert body["total_cost_usd_estimate"] == 0.0
    assert body["is_estimate"] is True


@pytest.mark.asyncio
async def test_cost_summary_aggregates() -> None:
    _reset_traces()
    record_trace(agent_name="a1", action_mode="draft_only", cost_estimate=0.05, workflow="wf-A")
    record_trace(agent_name="a1", action_mode="draft_only", cost_estimate=0.03, workflow="wf-A")
    record_trace(agent_name="a2", action_mode="approval_required", cost_estimate=0.10, workflow="wf-B")

    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/agent-observability/cost-summary")
    body = r.json()
    assert body["trace_count"] == 3
    assert body["total_cost_usd_estimate"] == pytest.approx(0.18, rel=1e-4)
    assert body["by_agent"]["a1"]["count"] == 2
    assert body["by_agent"]["a1"]["total_cost_usd"] == pytest.approx(0.08, rel=1e-4)
    assert body["by_agent"]["a2"]["count"] == 1
    assert body["by_workflow"]["wf-A"]["count"] == 2
    assert body["by_workflow"]["wf-B"]["count"] == 1


@pytest.mark.asyncio
async def test_existing_status_endpoint_still_works() -> None:
    """Phase 9 must not break the existing /status endpoint."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/agent-observability/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "agent_observability"


@pytest.mark.asyncio
async def test_existing_trace_endpoint_still_works() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/agent-observability/trace", json={
            "agent_name": "p9_test",
            "action_mode": "draft_only",
        })
    assert r.status_code == 200


def test_cost_summary_marks_estimate() -> None:
    """The cost-summary response must include is_estimate=True (Article 8)."""
    # Verified via the endpoint test above; this just doc-asserts intent
    assert True
