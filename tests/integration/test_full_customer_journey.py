"""End-to-end customer journey integration test under current Dealix authority.

Journey simulated:
  1. Anonymous trust posture
  2. Sector research discovery without public pricing authority
  3. Quote-only pricing gate
  4. Bespoke intake without automatic estimate
  5. Enterprise readiness intake
  6. Post-pilot customer/cost surfaces
  7. PDPL DSAR
  8. PDPL-safe prospect research
  9. Admin gates
 10. Health surfaces
"""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_journey_compliance_visible_to_anonymous_visitor(async_client):
    res = await async_client.get("/api/v1/compliance/status")
    assert res.status_code == 200
    body = res.json()
    breach = body["pdpl"]["art_21_breach_notification"]
    assert breach["dealix_internal_sla_hours"] < breach["sla_hours"]
    residency = body["data_residency"]
    assert residency["no_data_leaves_gcc"] is True


@pytest.mark.asyncio
async def test_journey_sector_research_visible_without_public_price(async_client):
    res = await async_client.get("/api/v1/sector-intel/sectors")
    assert res.status_code == 200
    body = res.json()
    assert body["sectors"]
    for sector in body["sectors"]:
        assert "price_sar" not in sector
        assert sector["data_maturity"] in {"partial", "placeholder"}
    authority = body["commercial_authority"]
    assert authority["public_fixed_price"] is False
    assert authority["live_charge_allowed"] is False
    assert authority["price_authority"] == "customer_specific_quote_after_qualified_discovery"


@pytest.mark.asyncio
async def test_journey_pricing_waits_for_specific_public_authority(async_client):
    res = await async_client.get("/api/v1/pricing/plans")
    assert res.status_code == 200
    body = res.json()
    assert body["plans"] == {}
    assert body["public_pricing_enabled"] is False
    assert body["status"] == "founder_approval_required"
    assert body["catalog_status"] in {"registry", "unavailable"}


@pytest.mark.asyncio
async def test_journey_r5_bespoke_request_routes_to_discovery_not_estimate(async_client):
    payload = {
        "company_name": "Journey Test Co",
        "contact_name": "Test Person",
        "contact_email": "test@journeyco.sa",
        "use_case_summary": (
            "End-to-end journey test for the bespoke AI service intake endpoint. "
            "Validates the prospect to diagnostic and discovery path."
        ),
        "use_case_category": "ops",
        "complexity": "moderate",
        "integrations_count": 2,
        "data_volume_band": "medium",
        "timeline_weeks": 6,
    }
    res = await async_client.post("/api/v1/service-setup/requests", json=payload)
    assert res.status_code == 201
    body = res.json()
    assert body["status"] == "intake_received"
    assert body["automatic_price_estimate"] is False
    assert body["public_fixed_price"] is False
    assert body["price_authority"] == "customer_specific_quote_after_qualified_discovery"
    assert body["next_step"] == "free_mini_diagnostic_then_qualified_discovery"
    assert "estimate" not in body


@pytest.mark.asyncio
async def test_journey_r7_enterprise_request_returns_readiness(async_client):
    payload = {
        "company_name": "Journey Enterprise",
        "contact_name": "Exec Person",
        "contact_title": "VP",
        "contact_email": "vp@journey-enterprise.sa",
        "org_size": "mid_250_1000",
        "use_case_category": "revenue_ops",
        "use_case_summary": (
            "Enterprise journey test that hits the R7 endpoint and verifies "
            "the readiness score lands in a valid band."
        ),
        "regulatory_scope": "pdpl_zatca",
        "target_start_date": "2026-09-01",
        "target_monthly_budget_sar": 40000,
        "contract_length_months": 12,
    }
    res = await async_client.post("/api/v1/enterprise-pmo/requests", json=payload)
    assert res.status_code == 201
    body = res.json()
    assert body["readiness"]["band"] in ("high_fit", "moderate_fit", "needs_review")


@pytest.mark.asyncio
async def test_journey_customer_usage_renders_for_unknown_handle(async_client):
    res = await async_client.get("/api/v1/customer-usage/journey_unknown_handle")
    assert res.status_code != 500


@pytest.mark.asyncio
async def test_journey_cost_transparency_visible(async_client):
    res = await async_client.get("/api/v1/cost-tracking/per-tier")
    assert res.status_code == 200
    growth_margin = res.json()["tiers"]["growth"]["gross_margin_pct"]
    assert growth_margin > 80


@pytest.mark.asyncio
async def test_journey_dsar_access_request_acknowledged(async_client):
    res = await async_client.post(
        "/api/v1/pdpl/dsar/request",
        json={"email": "data-subject@example.com", "request_type": "access"},
    )
    assert res.status_code == 202
    body = res.json()
    assert "data-subject@example.com" not in str(body)
    assert body["sla_business_days"] == 5


@pytest.mark.asyncio
async def test_journey_dsar_erasure_spec_transparent(async_client):
    res = await async_client.get("/api/v1/pdpl/dsar/erasure-cascade-spec")
    assert res.status_code == 200
    body = res.json()
    bases = body["retention_basis"]
    assert any("PDPL" in v for v in bases.values())
    assert any("ZATCA" in v for v in bases.values())


@pytest.mark.asyncio
async def test_journey_prospect_search_returns_pdpl_safe_view(async_client):
    res = await async_client.get("/api/v1/prospects/search?sector=saas&limit=5")
    assert res.status_code == 200
    body = res.json()
    for row in body.get("results", []):
        for forbidden in ("email", "phone", "contact_name"):
            assert forbidden not in row, f"Journey-test PII leak: {forbidden} appeared"


@pytest.mark.asyncio
async def test_journey_admin_tenants_blocked_without_key(async_client):
    res = await async_client.get("/api/v1/admin/tenants")
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_journey_admin_cost_summary_blocked_without_key(async_client):
    res = await async_client.get("/api/v1/cost-tracking/summary")
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_journey_admin_engagement_create_blocked_without_key(async_client):
    res = await async_client.post(
        "/api/v1/admin/enterprise-pmo/engagements",
        json={
            "request_id": "epr_aaaaaaaaaaaaaaaaaaaa",
            "tenant_handle": "test_tenant",
            "monthly_halalas": 3_000_000,
            "contract_start": "2026-09-01",
            "contract_months": 12,
            "exec_sponsor_name": "X",
            "exec_sponsor_email": "x@x.sa",
        },
    )
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_journey_admin_decision_blocked_without_key(async_client):
    res = await async_client.post(
        "/api/v1/admin/service-setup/requests/ssr_aaaaaaaaaaaaaaaaaaaa/decision",
        json={"decision": "approved"},
    )
    assert res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_journey_health_simple(async_client):
    res = await async_client.get("/healthz")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"


@pytest.mark.asyncio
async def test_journey_health_deep_runs(async_client):
    res = await async_client.get("/health/deep")
    assert res.status_code == 200
    body = res.json()
    for check in ("postgres", "redis", "sentry", "llm_providers"):
        assert check in body["checks"]
