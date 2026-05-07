"""Phase 8 — Per-customer Executive Pack tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_daily_pack_returns_all_required_sections() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customers/exec-test/executive-pack/today")
    assert r.status_code == 200
    pack = r.json()["pack"]
    # All required sections present
    assert pack["customer_handle"] == "exec-test"
    assert pack["cadence"] == "daily"
    assert "leads" in pack
    assert "support" in pack
    assert "blockers" in pack
    assert "next_3_actions" in pack
    assert "sector_context" in pack
    # Hard gates enforced
    gates = r.json()["hard_gates"]
    assert gates["no_fake_revenue"] is True
    assert gates["no_fake_forecast"] is True


@pytest.mark.asyncio
async def test_weekly_pack_has_week_label() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customers/exec-test/executive-pack/week")
    assert r.status_code == 200
    pack = r.json()["pack"]
    assert pack["cadence"] == "weekly"
    assert pack["week_label"] is not None
    assert pack["week_label"].startswith(str(2025)[:2])  # 2026-Wxx etc.


@pytest.mark.asyncio
async def test_pack_reflects_leadops_records() -> None:
    """Create some leadops records → pack KPIs should reflect them."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Create 3 records
        for i in range(3):
            await c.post("/api/v1/leadops/run", json={
                "raw_payload": {
                    "company": f"Pack Test {i}",
                    "email": f"x{i}@pack-test.sa",
                    "sector": "real_estate",
                    "region": "Riyadh",
                },
                "source": "manual",
                "customer_handle": "pack-leadops-test",
            })
        r = await c.get("/api/v1/customers/pack-leadops-test/executive-pack/today")
    pack = r.json()["pack"]
    assert pack["leads"]["leads_total"] >= 3
    assert pack["leads"]["leads_allowed"] >= 3
    # Each allowed lead should have produced a draft
    assert pack["leads"]["drafts_created"] >= 3


@pytest.mark.asyncio
async def test_pack_reflects_support_breaches() -> None:
    """Backdate a ticket and confirm SLA breach surfaces in support kpis."""
    from datetime import datetime, timedelta, timezone
    from auto_client_acquisition.support_inbox.state_store import _INDEX
    from auto_client_acquisition.support_os.ticket import create_ticket

    t = create_ticket(
        message_text_redacted="overdue support",
        customer_id="pack-support-test",
        channel="email",
        category="payment",
        priority="p0",
    )
    t.sla_due_at = datetime.now(timezone.utc) - timedelta(hours=3)
    _INDEX[t.id] = t

    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customers/pack-support-test/executive-pack/today")
    pack = r.json()["pack"]
    assert pack["support"]["sla_breached_count"] >= 1


@pytest.mark.asyncio
async def test_pack_summary_reflects_state() -> None:
    """Empty customer → 'no updates today' summary."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customers/empty-customer/executive-pack/today")
    pack = r.json()["pack"]
    assert "لا تحديثات" in pack["executive_summary_ar"] or "ليد" in pack["executive_summary_ar"]


@pytest.mark.asyncio
async def test_pack_safety_summary_present() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customers/safety-test/executive-pack/today")
    pack = r.json()["pack"]
    assert "no_fake" in pack["safety_summary"]
