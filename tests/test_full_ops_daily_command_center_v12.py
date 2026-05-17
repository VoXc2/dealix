"""V12 Phase 3 — Daily Command Center umbrella endpoint tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.full_ops import (
    WorkItem,
    get_default_queue,
)
from auto_client_acquisition.full_ops.work_queue import _reset


@pytest.mark.asyncio
async def test_daily_command_center_returns_200_with_empty_queue() -> None:
    from api.main import app

    _reset()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/daily-command-center")
    assert r.status_code == 200
    body = r.json()
    for key in (
        "today_top_3_decisions",
        "growth_queue",
        "sales_queue",
        "support_queue",
        "cs_queue",
        "delivery_queue",
        "compliance_alerts",
        "partner_queue",
        "evidence_ledger",
        "learning_loops",
        "executive_summary",
        "blocked_actions",
        "hard_gates",
        "degraded",
        "degraded_sections",
    ):
        assert key in body, f"missing field: {key}"
    assert body["growth_queue"]["count"] == 0
    assert body["degraded"] is False


@pytest.mark.asyncio
async def test_command_center_rolls_up_all_nine_subsystems() -> None:
    """Partner OS, Evidence Ledger and Learning loops must each roll up."""
    from api.main import app

    _reset()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/daily-command-center")
    assert r.status_code == 200
    body = r.json()

    partner = body["partner_queue"]
    assert "total_referrals" in partner
    assert "awaiting_invoice_paid" in partner
    assert "clawed_back" in partner

    evidence = body["evidence_ledger"]
    assert isinstance(evidence["proof_events_recorded"], int)

    learning = body["learning_loops"]
    assert "objection_library_size" in learning
    assert "kb_gap_candidates" in learning

    # Adding three live rollups must not degrade the command center.
    assert body["degraded"] is False


@pytest.mark.asyncio
async def test_daily_command_center_aggregates_per_os_queue() -> None:
    from api.main import app

    _reset()
    q = get_default_queue()
    q.add(WorkItem.make(os_type="growth", title_ar="g1", title_en="g1", source="t"))
    q.add(WorkItem.make(os_type="sales", title_ar="s1", title_en="s1", source="t"))
    q.add(WorkItem.make(os_type="support", title_ar="sup", title_en="sup", source="t", priority="p0"))
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/daily-command-center")
    assert r.status_code == 200
    body = r.json()
    assert body["growth_queue"]["count"] == 1
    assert body["sales_queue"]["count"] == 1
    assert body["support_queue"]["count"] == 1
    # p0 support item must surface in today_top_3_decisions
    top_ids = [it["id"] for it in body["today_top_3_decisions"]]
    assert any("support" in it.get("os_type", "") for it in body["today_top_3_decisions"])


@pytest.mark.asyncio
async def test_hard_gates_locked_in_command_center() -> None:
    from api.main import app

    _reset()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/daily-command-center")
    body = r.json()
    for gate in (
        "no_live_send",
        "no_live_charge",
        "no_scraping",
        "no_cold_outreach",
        "no_linkedin_automation",
        "no_fake_proof",
    ):
        assert body["hard_gates"][gate] is True


@pytest.mark.asyncio
async def test_full_ops_status_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "full_ops"
    assert body["version"] == "v12"


@pytest.mark.asyncio
async def test_command_center_never_returns_5xx_under_load() -> None:
    from api.main import app

    _reset()
    q = get_default_queue()
    # Stuff ~50 work items to ensure prioritize doesn't choke
    for i in range(50):
        q.add(WorkItem.make(
            os_type="growth", title_ar=f"g{i}", title_en=f"g{i}", source="t",
        ))
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/daily-command-center")
    assert 200 <= r.status_code < 300
    body = r.json()
    assert body["growth_queue"]["count"] == 50
    assert len(body["growth_queue"]["top_3"]) == 3


@pytest.mark.asyncio
async def test_command_center_executive_summary_counts_priorities() -> None:
    from api.main import app

    _reset()
    q = get_default_queue()
    q.add(WorkItem.make(os_type="growth", title_ar="a", title_en="a", source="t", priority="p0"))
    q.add(WorkItem.make(os_type="sales", title_ar="b", title_en="b", source="t", priority="p1"))
    q.add(WorkItem.make(os_type="sales", title_ar="c", title_en="c", source="t", priority="p2"))
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/full-ops/daily-command-center")
    body = r.json()
    bp = body["executive_summary"]["by_priority"]
    assert bp["p0"] == 1
    assert bp["p1"] == 1
    assert bp["p2"] == 1
    assert body["executive_summary"]["total_items"] == 3
