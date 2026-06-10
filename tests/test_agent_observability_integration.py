"""Phase 11 — Agent Observability shim tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.agent_observability import (
    list_recent_traces,
    record_trace,
)
from auto_client_acquisition.agent_observability.cost import estimate_cost
from auto_client_acquisition.agent_observability.redaction import redact_trace
from auto_client_acquisition.agent_observability.trace import _reset_traces


def test_record_trace_basic() -> None:
    _reset_traces()
    t = record_trace(
        agent_name="growth_agent",
        action_mode="draft_only",
        customer_handle="ao-test-1",
    )
    assert t.trace_id.startswith("agt_")
    assert t.agent_name == "growth_agent"
    assert t.action_mode == "draft_only"


def test_redact_trace_strips_email() -> None:
    safe = redact_trace({"contact": "secret@private.sa"})
    blob = str(safe)
    assert "secret@private.sa" not in blob


def test_redact_trace_strips_phone() -> None:
    safe = redact_trace({"phone": "+966500000000"})
    blob = str(safe)
    assert "+966500000000" not in blob


def test_redact_trace_strips_secrets() -> None:
    """Whole secrets must not survive the redactor (any form of mask is OK)."""
    safe = redact_trace({
        "key1": "sk_live_abcdef1234567890",
        "key2": "ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "key3": "AIzaSyA1234567890123456789012345678901",
        "key4": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
    })
    blob = str(safe)
    # The original secrets (full strings) must no longer be reconstructable
    assert "sk_live_abcdef1234567890" not in blob
    assert "ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" not in blob
    assert "AIzaSyA1234567890123456789012345678901" not in blob
    assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in blob


def test_estimate_cost_returns_number() -> None:
    cost = estimate_cost(input_tokens=1000, output_tokens=500, model="claude-sonnet")
    assert isinstance(cost, float)
    assert cost > 0


def test_recent_traces_round_trip() -> None:
    _reset_traces()
    record_trace(agent_name="a1", action_mode="draft_only")
    record_trace(agent_name="a2", action_mode="approval_required")
    traces = list_recent_traces(limit=10)
    assert len(traces) == 2


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/agent-observability/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "agent_observability"
    assert body["hard_gates"]["no_secrets_in_trace"] is True


@pytest.mark.asyncio
async def test_trace_endpoint_safe_payload() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/agent-observability/trace", json={
            "agent_name": "test_agent",
            "action_mode": "draft_only",
            "payload": {"input": "test prompt"},
        })
    assert r.status_code == 200
    body = r.json()
    assert body["trace"]["agent_name"] == "test_agent"


@pytest.mark.asyncio
async def test_trace_endpoint_redacts_email() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/agent-observability/trace", json={
            "agent_name": "redact_agent",
            "action_mode": "draft_only",
            "payload": {"text": "contact me at secret-x@private-y.sa"},
        })
    blob = str(r.json()["trace"]["redacted_payload"])
    assert "secret-x@private-y.sa" not in blob


@pytest.mark.asyncio
async def test_trace_endpoint_redacts_phone() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/agent-observability/trace", json={
            "agent_name": "phone_agent",
            "action_mode": "draft_only",
            "payload": {"text": "call +966500000000"},
        })
    blob = str(r.json()["trace"]["redacted_payload"])
    assert "+966500000000" not in blob


@pytest.mark.asyncio
async def test_trace_endpoint_redacts_secret() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/agent-observability/trace", json={
            "agent_name": "secret_agent",
            "action_mode": "draft_only",
            "payload": {"key": "sk_live_zzzz9999aaaa1111"},
        })
    blob = str(r.json()["trace"]["redacted_payload"])
    assert "sk_live_zzzz" not in blob
    assert "[SECRET]" in blob


@pytest.mark.asyncio
async def test_trace_requires_action_mode() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/agent-observability/trace", json={
            "agent_name": "no_mode",
        })
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_trace_rejects_invalid_action_mode() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/agent-observability/trace", json={
            "agent_name": "x",
            "action_mode": "made_up_mode",
        })
    assert r.status_code == 422


@pytest.mark.asyncio
async def test_recent_endpoint() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/agent-observability/recent")
    assert r.status_code == 200
    body = r.json()
    assert "traces" in body
    assert "quality" in body
