"""Revenue Ops Machine — daily dashboard aggregation tests (in-memory DB)."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from api.routers.revenue_ops_dashboard import router as dashboard_router
from api.security.api_key import require_admin_key
from auto_client_acquisition.revenue_ops_machine import (
    FunnelContext,
    FunnelState,
    save_context,
)
from db.models import Base, LeadRecord, OutreachQueueRecord
from db.session import get_db


@pytest_asyncio.fixture
async def dash() -> AsyncGenerator[tuple[AsyncClient, async_sessionmaker], None]:
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)

    async def _get_db() -> AsyncGenerator:
        async with maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    app = FastAPI()
    app.include_router(dashboard_router)
    app.dependency_overrides[get_db] = _get_db
    app.dependency_overrides[require_admin_key] = lambda: None
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client, maker
    app.dependency_overrides.clear()
    await engine.dispose()


async def _seed_lead(
    maker: async_sessionmaker,
    lead_id: str,
    state: FunnelState,
    *,
    grade: str = "",
    queued: int = 0,
    idle_hours: float = 0.0,
) -> None:
    ctx = FunnelContext(lead_id=lead_id, funnel_state=state, abcd_grade=grade)
    if state != FunnelState.visitor:
        ctx.history.append({"state": "visitor", "at": datetime.now(UTC).isoformat()})
    updated = datetime.now(UTC) - timedelta(hours=idle_hours)
    async with maker() as session:
        session.add(
            LeadRecord(
                id=lead_id,
                source="website",
                company_name=f"Co {lead_id}",
                meta_json=save_context({}, ctx),
                updated_at=updated,
            )
        )
        for i in range(queued):
            session.add(
                OutreachQueueRecord(
                    id=f"oq_{lead_id}_{i}",
                    lead_id=lead_id,
                    channel="email",
                    message="draft",
                    approval_required=True,
                    status="queued",
                )
            )
        await session.commit()


@pytest.mark.asyncio
async def test_empty_dashboard(
    dash: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, _ = dash
    res = await client.get("/api/v1/revenue-ops/dashboard")
    assert res.status_code == 200
    body = res.json()
    assert body["funnel_snapshot"]["total_in_machine"] == 0
    assert body["pending_approvals"] == 0


@pytest.mark.asyncio
async def test_dashboard_aggregates_states_grades_and_approvals(
    dash: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, maker = dash
    await _seed_lead(maker, "l1", FunnelState.lead_captured, grade="A", queued=2)
    await _seed_lead(maker, "l2", FunnelState.qualified_A, grade="A", queued=1)
    await _seed_lead(maker, "l3", FunnelState.nurture, grade="C")

    body = (await client.get("/api/v1/revenue-ops/dashboard")).json()
    assert body["funnel_snapshot"]["total_in_machine"] == 3
    assert body["funnel_snapshot"]["by_state"]["lead_captured"] == 1
    assert body["funnel_snapshot"]["by_state"]["qualified_A"] == 1
    assert body["abcd_distribution"] == {"A": 2, "C": 1}
    assert body["pending_approvals"] == 3


@pytest.mark.asyncio
async def test_dashboard_flags_stuck_leads(
    dash: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, maker = dash
    await _seed_lead(maker, "fresh", FunnelState.qualified_A, idle_hours=1)
    await _seed_lead(maker, "warn", FunnelState.qualified_A, idle_hours=30)
    await _seed_lead(maker, "alert", FunnelState.qualified_A, idle_hours=80)

    body = (await client.get("/api/v1/revenue-ops/dashboard")).json()
    warn_ids = {x["lead_id"] for x in body["stuck_leads"]["warn_24h"]}
    alert_ids = {x["lead_id"] for x in body["stuck_leads"]["alert_72h"]}
    assert warn_ids == {"warn"}
    assert alert_ids == {"alert"}


@pytest.mark.asyncio
async def test_dashboard_lists_retainer_candidates(
    dash: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, maker = dash
    await _seed_lead(maker, "ret", FunnelState.retainer_candidate, grade="A")
    body = (await client.get("/api/v1/revenue-ops/dashboard")).json()
    assert len(body["retainer_candidates"]) == 1
    assert body["retainer_candidates"][0]["lead_id"] == "ret"
