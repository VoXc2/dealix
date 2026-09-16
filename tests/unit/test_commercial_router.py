"""ASGI integration tests for the current governed commercial authority.

These tests exercise the FastAPI router through the ASGI stack while preserving
launch truth: one quote-only pilot path, no live send, no live charge, no public
fixed pricing, and no automatic expansion.
"""

from __future__ import annotations

from datetime import date

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_commercial_status_is_governed_and_quote_only():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/commercial/status")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ready_for_governed_internal_commercial_ops"
    assert data["quote_only_after_discovery"] is True
    assert data["public_fixed_price"] is False
    assert data["live_charge"] is False
    assert data["automatic_upsell"] is False
    assert data["external_send"] is False


@pytest.mark.asyncio
async def test_commercial_daily_brief_is_fail_closed():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/commercial/daily-brief")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "governed_internal_only"
    assert data["payment"] == {"status": "blocked_no_live_charge", "tiers": []}
    assert data["expansion"]["automatic_upsell"] is False
    assert "NO_LIVE_SEND" in data["reminders"]
    assert "NO_FAKE_PROOF" in data["reminders"]


@pytest.mark.asyncio
async def test_commercial_payment_tiers_are_not_public_prices():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/commercial/payment/tiers")
    assert r.status_code == 200
    data = r.json()
    assert data["tiers"] == []
    assert data["product_count"] == 1
    assert data["public_fixed_price"] is False
    assert data["quote_only"] is True
    assert data["live_checkout"] is False
    assert data["live_charge"] is False


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
async def test_commercial_warm_intro_draft_stays_draft_only():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/warm-intro/draft",
            json={
                "prospect_name": "Ahmed",
                "company_name": "Company X",
                "sector": "b2b_services",
            },
        )
    assert r.status_code == 200
    data = r.json()
    assert data["approval_status"] == "approval_required"
    assert "whatsapp_drafts" in data


@pytest.mark.asyncio
async def test_commercial_current_warm_intro_requires_real_context():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/warm-intro/generate",
            json={
                "name": "Ahmed",
                "company": "Company X",
                "role": "Founder",
                "sector": "b2b_services",
                "relationship": "referral",
                "warm_context_ref": "referral-note:test-001",
            },
        )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "draft_only"
    assert data["external_send_allowed"] is False
    assert data["consent_inferred"] is False


@pytest.mark.asyncio
async def test_commercial_pilot_start_requires_named_governed_scope():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/pilot/start",
            json={
                "account_id": "test-001",
                "company_name": "Pilot Co",
                "start_date": date.today().isoformat(),
                "approved_duration_days": 21,
                "approved_duration_ref": "duration:test-001",
                "approved_scope_ref": "scope:test-001",
                "baseline_source_ref": "baseline:test-001",
                "approved_data_boundary_ref": "data-boundary:test-001",
                "approval_path_ref": "approval-path:test-001",
                "acceptance_criteria_ref": "acceptance:test-001",
                "customer_specific_quote_ref": "quote:test-001",
                "customer_acceptance_ref": "customer-acceptance:test-001",
                "start_condition_ref": "start-condition:test-001",
            },
        )
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "plan_prepared_approval_required"
    assert data["external_send_allowed"] is False
    assert data["live_charge_allowed"] is False
    assert len(data["plan"]["day_plans"]) == 7
    assert data["plan"]["proof_cadence"] == "approved_duration_proportional_and_final"


@pytest.mark.asyncio
async def test_commercial_pilot_week1_template_is_template_only():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get("/api/v1/commercial/pilot/week1-template")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "template_only"
    assert data["external_send_allowed"] is False
    assert "outcomes" in data["sections"]
    assert "evidence_gaps" in data["sections"]


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
async def test_commercial_payment_link_is_hard_blocked():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/payment/link",
            json={"customer_name": "Test"},
        )
    assert r.status_code == 409
    detail = r.json()["detail"]
    assert detail["code"] == "NO_LIVE_CHARGE"


@pytest.mark.asyncio
async def test_commercial_expansion_is_never_automatic():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.get(
            "/api/v1/commercial/upsell/check",
            params={
                "account_id": "test-001",
                "events_count": 9,
                "proof_pack_generated": True,
                "days_active": 30,
                "nps_score": 10,
            },
        )
    assert r.status_code == 200
    data = r.json()
    assert data["decision"] == "manual_review_required"
    assert data["eligible_for_automatic_expansion"] is False
    assert data["offer"] is None
    assert data["price_sar"] is None


@pytest.mark.asyncio
async def test_commercial_revenue_run_refuses_live_execution():
    from api.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        r = await client.post(
            "/api/v1/commercial/revenue/run",
            json={"trigger": "manual", "dry_run": False},
        )
    assert r.status_code == 409
    assert r.json()["detail"]["code"] == "NO_LIVE_COMMERCIAL_EXECUTION"


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
