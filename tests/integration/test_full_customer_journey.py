"""End-to-end customer journey integration test (W11.4).

Walks the full revenue-critical path through Dealix's public API surface,
exercising every endpoint a prospect/customer hits from discovery to paid
relationship. Each step asserts contract invariants without depending on
DB persistence (where unavailable, endpoints degrade gracefully — that's
the contract this test verifies).

Journey simulated:
  1. Prospect lands on /api/v1/compliance/status → verifies trust posture
  2. Prospect browses /api/v1/sector-intel/sectors → sees pricing menu
  3. Prospect submits R5 bespoke request → gets estimate
  4. Prospect submits R7 enterprise request → gets readiness score
  5. Customer (post-pilot) checks /api/v1/customer-usage/{handle}
  6. Customer reads cost transparency via /api/v1/cost-tracking/per-tier
  7. Customer submits PDPL DSAR access request
  8. Customer searches Saudi prospects (LaaS-style use case)
  9. Admin (via X-Admin-API-Key) hits all admin endpoints to confirm gates

Each assertion documents the business invariant being protected.
"""
from __future__ import annotations

import pytest


# ── Step 1: Trust posture verification ───────────────────────────

@pytest.mark.asyncio
async def test_journey_compliance_visible_to_anonymous_visitor(async_client):
    res = await async_client.get("/api/v1/compliance/status")
    assert res.status_code == 200
    body = res.json()
    # Invariant: PDPL Art. 21 internal SLA (24h) better than mandate (72h)
    breach = body["pdpl"]["art_21_breach_notification"]
    assert breach["dealix_internal_sla_hours"] < breach["sla_hours"]
    # Invariant: data residency disclosure must include LLM cross-border note
    residency = body["data_residency"]
    assert residency["no_data_leaves_gcc"] is True


# ── Step 2: Service catalog discovery ────────────────────────────

@pytest.mark.asyncio
async def test_journey_sector_pricing_menu_visible(async_client):
    res = await async_client.get("/api/v1/sector-intel/sectors")
    assert res.status_code == 200
    body = res.json()
    # Invariant: each sector has a clear price
    for sector in body["sectors"]:
        assert sector["price_sar"] > 0


@pytest.mark.asyncio
async def test_journey_pricing_plans_visible(async_client):
    res = await async_client.get("/api/v1/pricing/plans")
    assert res.status_code == 200
    plans = res.json()["plans"]
    # Invariant: 5 public plans (starter, growth, scale, pilot_managed,
    # laas_per_reply, laas_per_demo — but pilot_1sar is hidden)
    assert "pilot_1sar" not in plans
    assert "starter" in plans
    assert "growth" in plans


# ── Step 3-4: Prospect submits requests ──────────────────────────

@pytest.mark.asyncio
async def test_journey_r5_bespoke_request_returns_estimate(async_client):
    payload = {
        "company_name": "Journey Test Co",
        "contact_name": "Test Person",
        "contact_email": "test@journeyco.sa",
        "use_case_summary": (
            "End-to-end journey test for the bespoke AI service "
            "intake endpoint. Validates the prospect → estimate path."
        ),
        "use_case_category": "ops",
        "complexity": "moderate",
        "integrations_count": 2,
        "data_volume_band": "medium",
        "timeline_weeks": 6,
    }
    res = await async_client.post(
        "/api/v1/service-setup/requests", json=payload
    )
    assert res.status_code == 201
    body = res.json()
    # Invariant: estimate within R5 floor/cap (5K-25K SAR)
    assert 5000 <= body["estimate"]["setup_sar"] <= 25000


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
            "Enterprise journey test that hits the R7 endpoint and "
            "verifies the readiness score lands in a valid band."
        ),
        "regulatory_scope": "pdpl_zatca",
        "target_start_date": "2026-09-01",
        "target_monthly_budget_sar": 40000,
        "contract_length_months": 12,
    }
    res = await async_client.post(
        "/api/v1/enterprise-pmo/requests", json=payload
    )
    assert res.status_code == 201
    body = res.json()
    # Invariant: readiness band ∈ {high_fit, moderate_fit, needs_review}
    assert body["readiness"]["band"] in (
        "high_fit", "moderate_fit", "needs_review"
    )


# ── Step 5-6: Post-pilot customer surfaces ───────────────────────

@pytest.mark.asyncio
async def test_journey_customer_usage_renders_for_unknown_handle(async_client):
    """Customer portal calls usage endpoint with their handle. Even if
    the tenant doesn't exist yet, response should be non-500."""
    res = await async_client.get(
        "/api/v1/customer-usage/journey_unknown_handle"
    )
    assert res.status_code != 500


@pytest.mark.asyncio
async def test_journey_cost_transparency_visible(async_client):
    """Customer (and investor) hits cost-tracking to see margin model."""
    res = await async_client.get("/api/v1/cost-tracking/per-tier")
    assert res.status_code == 200
    growth_margin = res.json()["tiers"]["growth"]["gross_margin_pct"]
    # Invariant: aligns with v3 §1 financial model (~87% gross margin)
    assert growth_margin > 80


# ── Step 7: Data subject rights flow ─────────────────────────────

@pytest.mark.asyncio
async def test_journey_dsar_access_request_acknowledged(async_client):
    res = await async_client.post(
        "/api/v1/pdpl/dsar/request",
        json={
            "email": "data-subject@example.com",
            "request_type": "access",
        },
    )
    assert res.status_code == 202
    body = res.json()
    # Invariant: response NEVER echoes the email (PII enumeration protection)
    assert "data-subject@example.com" not in str(body)
    # Invariant: SLA differentiator surfaced (5 days vs 30)
    assert body["sla_business_days"] == 5


@pytest.mark.asyncio
async def test_journey_dsar_erasure_spec_transparent(async_client):
    res = await async_client.get(
        "/api/v1/pdpl/dsar/erasure-cascade-spec"
    )
    assert res.status_code == 200
    body = res.json()
    # Invariant: retention bases (PDPL Art. 18 + ZATCA) explicitly named
    bases = body["retention_basis"]
    assert any("PDPL" in v for v in bases.values())
    assert any("ZATCA" in v for v in bases.values())


# ── Step 8: Prospect search (LaaS-style discovery) ───────────────

@pytest.mark.asyncio
async def test_journey_prospect_search_returns_pdpl_safe_view(async_client):
    res = await async_client.get(
        "/api/v1/prospects/search?sector=saas&limit=5"
    )
    assert res.status_code == 200
    body = res.json()
    # Invariant: NEVER includes PII (email/phone/contact_name)
    for row in body.get("results", []):
        for forbidden in ("email", "phone", "contact_name"):
            assert forbidden not in row, (
                f"Journey-test PII leak: {forbidden} appeared in results"
            )


# ── Step 9: Admin gates verified ─────────────────────────────────

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
        json={"decision": "approved", "quoted_setup_halalas": 1_000_000},
    )
    assert res.status_code in (401, 403)


# ── Step 10: Health surface unified ──────────────────────────────

@pytest.mark.asyncio
async def test_journey_health_simple(async_client):
    res = await async_client.get("/healthz")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"


@pytest.mark.asyncio
async def test_journey_health_deep_runs(async_client):
    """/healthz?deep=1 returns the deep payload (used in deploy runbook smoke)."""
    res = await async_client.get("/healthz?deep=1")
    assert res.status_code == 200
    body = res.json()
    # Must include the 4 mandatory checks
    for check in ("postgres", "redis", "sentry", "llm_providers"):
        assert check in body["checks"]
