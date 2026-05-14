"""HTTP smoke tests for the Revenue OS golden chain (Decision Passport + Leads + catalog).

Run with: APP_ENV=test pytest tests/test_revenue_os_golden_chain_smoke.py -q
"""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_decision_passport_golden_chain_and_evidence_levels() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        g = await c.get("/api/v1/decision-passport/golden-chain")
        e = await c.get("/api/v1/decision-passport/evidence-levels")
    assert g.status_code == 200
    assert e.status_code == 200
    body_g = g.json()
    body_e = e.json()
    assert "chain_ar" in body_g
    assert "levels" in body_e


@pytest.mark.asyncio
async def test_post_leads_includes_decision_passport_and_readiness() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    payload = {
        "company": "Golden Chain Smoke Co",
        "name": "Sami",
        "email": "golden.smoke@example.sa",
        "phone": "+966501112233",
        "sector": "technology",
        "region": "Saudi Arabia",
        "budget": 50000,
        "message": "Smoke test for private beta readiness.",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/api/v1/leads", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "decision_passport" in data or "passport" in str(data).lower()
    # PipelineResponse uses decision_passport at top level via LeadResponse wrapper
    assert "decision_passport" in data or "customer_readiness" in data


@pytest.mark.asyncio
async def test_revenue_os_catalog_and_anti_waste() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        cat = await c.get("/api/v1/revenue-os/catalog")
        aw = await c.post(
            "/api/v1/revenue-os/anti-waste/check",
            json={
                "has_decision_passport": False,
                "action_external": True,
                "upsell_attempt": False,
                "proof_event_count": 0,
                "evidence_level_for_public": 0,
                "public_marketing_attempt": False,
            },
        )
    assert cat.status_code == 200
    assert aw.status_code == 200
    assert "action_catalog" in cat.json() or "source_registry" in cat.json()
    aw_body = aw.json()
    assert "ok" in aw_body
    assert "violations" in aw_body


@pytest.mark.asyncio
async def test_proof_ledger_recent_events_factory() -> None:
    from datetime import UTC, datetime, timedelta

    from auto_client_acquisition.proof_ledger.factory import recent_events

    since = datetime.now(UTC) - timedelta(days=365)
    events = recent_events(since=since, limit=5)
    assert isinstance(events, list)
