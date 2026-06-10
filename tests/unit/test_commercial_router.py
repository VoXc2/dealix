"""ASGI integration tests for api/routers/commercial.py.

These tests go through the full FastAPI ASGI stack to exercise router
code paths and boost api module coverage above the 70% gate.

All endpoints are accessible without auth when DEALIX_ADMIN_API_KEY is
not set (dev/test mode — _require_admin returns early).

Note: imports api.main inside each test function to avoid collection
errors in environments where crypto packages aren't available.
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_commercial_daily_brief():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/commercial/daily-brief")
    assert r.status_code == 200
    data = r.json()
    assert "chain_status" in data
    assert "status" in data


@pytest.mark.asyncio
async def test_commercial_payment_tiers():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/commercial/payment/tiers")
    assert r.status_code == 200
    data = r.json()
    assert "tiers" in data
    assert "currency" in data
    assert "sprint_499" in data["tiers"]


@pytest.mark.asyncio
async def test_commercial_diagnostic_generate():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/diagnostic/generate",
            json={"company_name": "Test Co", "sector": "b2b_services"},
        )
    assert r.status_code == 200
    data = r.json()
    assert len(data["sections"]) == 10
    assert data["approval_status"] == "approval_required"


@pytest.mark.asyncio
async def test_commercial_diagnostic_markdown():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/diagnostic/generate/markdown",
            json={"company_name": "Test Co", "sector": "b2b_services"},
        )
    assert r.status_code == 200
    assert "Test Co" in r.text


@pytest.mark.asyncio
async def test_commercial_warm_intro_draft():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/warm-intro/draft",
            json={
                "prospect_name": "أحمد",
                "company_name": "شركة X",
                "sector": "b2b_services",
            },
        )
    assert r.status_code == 200
    data = r.json()
    assert data["approval_status"] == "approval_required"
    assert "whatsapp_drafts" in data


@pytest.mark.asyncio
async def test_commercial_pilot_start():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/pilot/start",
            json={"account_id": "test-001", "company_name": "Pilot Co"},
        )
    assert r.status_code == 200
    data = r.json()
    assert data["approval_status"] == "approval_required"
    assert len(data["day_plans"]) == 7


@pytest.mark.asyncio
async def test_commercial_pilot_report():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/commercial/pilot/test-001/report")
    assert r.status_code == 200
    assert len(r.text) > 0


@pytest.mark.asyncio
async def test_commercial_proof_build():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/proof/build",
            json={
                "account_id": "test-001",
                "company_name": "Test Co",
                "events": [],
            },
        )
    assert r.status_code == 200
    data = r.json()
    assert data["proof_level"] == "L0"
    assert data["approval_status"] == "approval_required"


@pytest.mark.asyncio
async def test_commercial_proof_markdown():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/proof/build/markdown",
            json={"account_id": "test-001", "company_name": "Test Co"},
        )
    assert r.status_code == 200
    assert len(r.text) > 0


@pytest.mark.asyncio
async def test_commercial_payment_link_sandbox():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/payment/link",
            json={"service_tier": "sprint_499", "customer_name": "Test"},
        )
    assert r.status_code == 200
    data = r.json()
    assert data["approval_status"] == "approval_required"
    assert data["is_live_mode"] is False


@pytest.mark.asyncio
async def test_commercial_upsell_check_not_eligible():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get(
            "/api/v1/commercial/upsell/check/test-001",
            params={"company_name": "Test Co", "proof_event_count": 0},
        )
    assert r.status_code == 200
    data = r.json()
    assert data["is_eligible"] is False


@pytest.mark.asyncio
async def test_commercial_upsell_check_eligible():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get(
            "/api/v1/commercial/upsell/check/test-002",
            params={
                "company_name": "Growth Co",
                "proof_event_count": 3,
                "proof_level": "L1",
            },
        )
    assert r.status_code == 200
    data = r.json()
    assert data["is_eligible"] is True
    assert data["recommended_tier"]


@pytest.mark.asyncio
async def test_commercial_case_study_generate():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/case-study/generate",
            json={
                "account_id": "test-001",
                "company_name": "Success Co",
                "sector": "b2b_services",
                "customer_consent": True,
            },
        )
    assert r.status_code == 200
    data = r.json()
    assert data["approval_status"] == "approval_required"
    assert data["study_id"]


@pytest.mark.asyncio
async def test_commercial_case_study_markdown():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/case-study/generate/markdown",
            json={
                "account_id": "test-001",
                "company_name": "Success Co",
                "sector": "b2b_services",
                "customer_consent": True,
            },
        )
    assert r.status_code == 200
    assert len(r.text) > 0
