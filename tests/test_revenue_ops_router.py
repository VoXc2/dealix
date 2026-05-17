"""Revenue Ops Machine — API router contract tests (in-memory DB)."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from api.routers.revenue_ops_machine import router as revops_router
from api.security.api_key import require_admin_key
from db.models import Base, OutreachQueueRecord
from db.session import get_db

A_GRADE_FORM = {
    "company": "Acme Trading Co",
    "contact_name": "Sami",
    "contact_email": "sami@acme.sa",
    "role": "Founder",
    "current_crm": "HubSpot",
    "ai_usage": "chatbot pilot",
    "region": "Riyadh",
    "urgency": "asap",
    "budget": 6000,
}


@pytest_asyncio.fixture
async def revops() -> AsyncGenerator[tuple[AsyncClient, async_sessionmaker], None]:
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
    app.include_router(revops_router)
    app.dependency_overrides[get_db] = _get_db
    app.dependency_overrides[require_admin_key] = lambda: None
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client, maker
    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.mark.asyncio
async def test_states_endpoint_lists_sixteen_states(
    revops: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, _ = revops
    res = await client.get("/api/v1/revenue-ops/states")
    assert res.status_code == 200
    body = res.json()
    assert len(body["states"]) == 16
    assert body["terminal_success"] == "retainer_candidate"
    assert len(body["hard_rules"]) == 5


@pytest.mark.asyncio
async def test_capture_creates_scored_lead_and_queues_drafts(
    revops: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, maker = revops
    res = await client.post("/api/v1/revenue-ops/capture", json=A_GRADE_FORM)
    assert res.status_code == 200
    body = res.json()
    assert body["funnel_state"] == "lead_captured"
    assert body["abcd_grade"] == "A"
    assert body["recommended_offer_id"] == "revenue_proof_sprint_499"

    # Every draft is queued for approval — none is ever sent.
    async with maker() as session:
        rows = (await session.execute(select(OutreachQueueRecord))).scalars().all()
    assert rows, "capture should queue at least one draft"
    for row in rows:
        assert row.status == "queued"
        assert row.approval_required is True
        assert row.sent_at is None


@pytest.mark.asyncio
async def test_qualify_routes_grade_a_to_qualified_a(
    revops: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, _ = revops
    lead_id = (await client.post("/api/v1/revenue-ops/capture", json=A_GRADE_FORM)).json()[
        "lead_id"
    ]
    res = await client.post("/api/v1/revenue-ops/qualify", json={"lead_id": lead_id})
    assert res.status_code == 200
    assert res.json()["funnel_state"] == "qualified_A"


@pytest.mark.asyncio
async def test_advance_rejects_illegal_transition_with_409(
    revops: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, _ = revops
    lead_id = (await client.post("/api/v1/revenue-ops/capture", json=A_GRADE_FORM)).json()[
        "lead_id"
    ]
    res = await client.post(
        "/api/v1/revenue-ops/advance",
        json={"lead_id": lead_id, "target_state": "invoice_sent"},
    )
    assert res.status_code == 409


@pytest.mark.asyncio
async def test_advance_allows_legal_transition(
    revops: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, _ = revops
    lead_id = (await client.post("/api/v1/revenue-ops/capture", json=A_GRADE_FORM)).json()[
        "lead_id"
    ]
    await client.post("/api/v1/revenue-ops/qualify", json={"lead_id": lead_id})
    res = await client.post(
        "/api/v1/revenue-ops/advance",
        json={"lead_id": lead_id, "target_state": "meeting_booked"},
    )
    assert res.status_code == 200
    assert res.json()["funnel_state"] == "meeting_booked"


@pytest.mark.asyncio
async def test_advance_unknown_state_is_400(
    revops: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, _ = revops
    lead_id = (await client.post("/api/v1/revenue-ops/capture", json=A_GRADE_FORM)).json()[
        "lead_id"
    ]
    res = await client.post(
        "/api/v1/revenue-ops/advance",
        json={"lead_id": lead_id, "target_state": "teleported"},
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_get_unknown_lead_is_404(
    revops: tuple[AsyncClient, async_sessionmaker],
) -> None:
    client, _ = revops
    res = await client.get("/api/v1/revenue-ops/lead/lead_does_not_exist")
    assert res.status_code == 404
