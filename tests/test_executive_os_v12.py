"""V12 Phase 7 — Executive OS tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.full_ops import WorkItem, get_default_queue
from auto_client_acquisition.full_ops.work_queue import _reset


@pytest.mark.asyncio
async def test_status() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/executive-os/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "executive_os"
    assert body["hard_gates"]["no_fake_revenue"] is True
    assert body["hard_gates"]["no_fake_forecast"] is True


@pytest.mark.asyncio
async def test_daily_brief_empty_queue_returns_insufficient_data() -> None:
    from api.main import app

    _reset()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/executive-os/daily-brief")
    assert r.status_code == 200
    body = r.json()
    assert body["data_status"] == "insufficient_data"
    assert body["decisions"] == []


@pytest.mark.asyncio
async def test_daily_brief_with_items_returns_top3() -> None:
    from api.main import app

    _reset()
    q = get_default_queue()
    for i in range(5):
        q.add(WorkItem.make(
            os_type="sales", title_ar=f"a{i}", title_en=f"a{i}",
            source="t", priority="p1" if i < 2 else "p2",
        ))
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/executive-os/daily-brief")
    body = r.json()
    assert body["data_status"] == "live"
    assert len(body["decisions"]) == 3


@pytest.mark.asyncio
async def test_weekly_pack_aggregates_by_priority_and_os() -> None:
    from api.main import app

    _reset()
    q = get_default_queue()
    q.add(WorkItem.make(os_type="growth", title_ar="g", title_en="g", source="t", priority="p0"))
    q.add(WorkItem.make(os_type="support", title_ar="s", title_en="s", source="t", priority="p1"))
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/executive-os/weekly-pack")
    body = r.json()
    assert body["total_items"] == 2
    assert body["by_priority"]["p0"] == 1
    assert body["by_os_type"]["growth"] == 1
    assert body["by_os_type"]["support"] == 1
