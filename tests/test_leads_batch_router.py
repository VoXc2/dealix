"""Batch leads router — Tier1 policy + mocked pipeline."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.dependencies import get_acquisition_pipeline
from api.routers.leads import router as leads_router
from auto_client_acquisition.agents.intake import Lead, LeadSource, LeadStatus
from auto_client_acquisition.pipeline import PipelineResult


@pytest_asyncio.fixture
async def leads_app_client() -> AsyncGenerator[tuple[FastAPI, AsyncClient], None]:
    """Minimal FastAPI app with leads router + ASGI client."""
    app = FastAPI()
    app.include_router(leads_router)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield app, client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def leads_client(
    leads_app_client: tuple[FastAPI, AsyncClient],
) -> AsyncGenerator[AsyncClient, None]:
    yield leads_app_client[1]


@pytest.mark.asyncio
async def test_leads_batch_rejects_scraping_tier1(leads_client: AsyncClient) -> None:
    res = await leads_client.post(
        "/api/v1/leads/batch",
        json={
            "tier1_source": "scraping",
            "items": [
                {
                    "company": "Co",
                    "name": "User",
                    "email": "u@example.com",
                    "message": "Hi",
                }
            ],
        },
    )
    assert res.status_code == 422
    body = res.json()
    detail = body.get("detail")
    assert detail is not None


@pytest.mark.asyncio
async def test_leads_batch_warm_intro_succeeds_with_mock_pipeline(
    leads_app_client: tuple[FastAPI, AsyncClient],
) -> None:
    app, leads_client = leads_app_client

    lead = Lead(
        id="lead_batch_router_ok",
        source=LeadSource.REFERRAL,
        company_name="Test Co",
        contact_name="Tester",
        contact_email="tester@example.com",
        contact_phone="+966501111111",
        sector="technology",
        region="Saudi Arabia",
        budget=50000.0,
        message="Need help with revenue ops",
        status=LeadStatus.NEW,
        fit_score=0.4,
        urgency_score=0.2,
        pain_points=[],
        metadata={},
    )
    result = PipelineResult(lead=lead, warnings=[])
    mock_pipeline = AsyncMock()
    mock_pipeline.run = AsyncMock(return_value=result)

    app.dependency_overrides[get_acquisition_pipeline] = lambda: mock_pipeline

    try:
        with (
            patch("api.routers.leads.notify_founder_on_intake", new_callable=AsyncMock),
            patch("api.routers.leads._persist_lead_row", new_callable=AsyncMock),
        ):
            res = await leads_client.post(
                "/api/v1/leads/batch",
                json={
                    "tier1_source": "warm_intro",
                    "items": [
                        {
                            "company": "Test Co",
                            "name": "Tester",
                            "email": "tester@example.com",
                            "phone": "+966501111111",
                            "sector": "technology",
                            "region": "Saudi Arabia",
                            "budget": 50000,
                            "message": "Need help with revenue ops",
                        }
                    ],
                },
            )
    finally:
        app.dependency_overrides.pop(get_acquisition_pipeline, None)

    assert res.status_code == 200
    data = res.json()
    assert data["succeeded"] == 1
    assert data["failed"] == 0
    assert data["results"][0]["ok"] is True
    assert data["results"][0]["lead_id"] == "lead_batch_router_ok"


@pytest.mark.asyncio
async def test_discover_local_rejects_invalid_targeting_profile(
    leads_client: AsyncClient,
) -> None:
    res = await leads_client.post(
        "/api/v1/leads/discover/local",
        json={
            "industry": "dental_clinic",
            "city": "riyadh",
            "targeting_profile": "not-a-dict",
        },
    )
    assert res.status_code == 400
