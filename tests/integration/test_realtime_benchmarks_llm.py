"""Integration tests for realtime / benchmarks / llm_usage routers."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_realtime_stream_returns_event_stream(async_client) -> None:
    # ASGITransport supports streaming; send a single short request.
    async with async_client.stream("GET", "/api/v1/realtime/stream") as r:
        assert r.status_code == 200
        assert r.headers["content-type"].startswith("text/event-stream")
        # We don't iterate the body — the hello event is emitted, then the
        # stream parks on the heartbeat loop. Closing the context cancels.


@pytest.mark.asyncio
async def test_benchmarks_route_falls_back(async_client) -> None:
    r = await async_client.get("/api/v1/benchmarks/sector")
    assert r.status_code == 200
    body = r.json()
    assert body["source"] in {"tinybird", "internal_aggregator", "empty"}
    assert "rows" in body


@pytest.mark.asyncio
async def test_llm_usage_route_registered(async_client) -> None:
    r = await async_client.get("/api/v1/customers/ten_test/llm/usage")
    # Auth gate or 200 with mostly-zero shape.
    assert r.status_code in {200, 401, 403}


@pytest.mark.asyncio
async def test_admin_nps_admin_only(async_client) -> None:
    r = await async_client.get("/api/v1/admin/nps/responses")
    # Without admin headers, must be 403.
    assert r.status_code in {403}
