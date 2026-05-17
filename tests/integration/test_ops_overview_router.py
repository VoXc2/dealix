"""Integration tests for the Unified Ops router — Dealix Full Ops."""
from __future__ import annotations

import pytest

_OPS_VIEWS = {
    "/api/v1/ops/founder/overview": "founder_overview",
    "/api/v1/ops/sales/pipeline": "sales_pipeline",
    "/api/v1/ops/partners/dashboard": "partners_dashboard",
    "/api/v1/ops/support/inbox": "support_inbox",
    "/api/v1/ops/governance/status": "governance_status",
}


@pytest.mark.asyncio
@pytest.mark.parametrize("path,view", list(_OPS_VIEWS.items()))
async def test_ops_views_return_guardrails(async_client, path, view):
    res = await async_client.get(path)
    assert res.status_code == 200
    body = res.json()
    assert body["service"] == "ops_overview"
    assert body["view"] == view
    assert body["guardrails"]["no_llm_calls"] is True
    assert body["guardrails"]["read_only"] is True
    assert "generated_at" in body


@pytest.mark.asyncio
async def test_founder_overview_aggregates_action_items(async_client):
    res = await async_client.get("/api/v1/ops/founder/overview")
    body = res.json()
    assert "action_items" in body
    assert "approvals_pending" in body["action_items"]
    assert "commission_owed_sar" in body["action_items"]
    assert isinstance(body["sources"], list) and body["sources"]


@pytest.mark.asyncio
async def test_partners_dashboard_reports_compliance_flags(async_client):
    res = await async_client.get("/api/v1/ops/partners/dashboard")
    body = res.json()
    assert "compliance_flags" in body
    assert "void_commissions" in body["compliance_flags"]


@pytest.mark.asyncio
async def test_support_inbox_reports_knowledge_base(async_client):
    res = await async_client.get("/api/v1/ops/support/inbox")
    body = res.json()
    assert "knowledge_base" in body


@pytest.mark.asyncio
async def test_governance_status_states_doctrine(async_client):
    res = await async_client.get("/api/v1/ops/governance/status")
    body = res.json()
    assert body["doctrine"]["no_external_action_without_approval"] is True
    assert body["doctrine"]["no_payout_before_invoice_paid"] is True
