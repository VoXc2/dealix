"""HTTP smoke tests for governed revenue + AI operating blueprint."""

from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_governed_ops_blueprint_surface(async_client) -> None:
    r = await async_client.get("/api/v1/governed-ops/blueprint")
    assert r.status_code == 200
    body = r.json()
    assert body["positioning"]["company_type_en"] == "Governed Revenue & AI Operations Company"
    assert body["north_star"]["metric_id"] == "governed_value_decisions_created"
    assert body["guardrails"]["approval_first"] is True


@pytest.mark.asyncio
async def test_governed_ops_offers_top_three(async_client) -> None:
    r = await async_client.get("/api/v1/governed-ops/offers")
    assert r.status_code == 200
    body = r.json()
    assert body["top_three_offer_ids"] == [
        "governed_revenue_ops_diagnostic",
        "revenue_intelligence_sprint",
        "governed_ops_retainer",
    ]
    assert len(body["offers"]) == 7


@pytest.mark.asyncio
async def test_governed_ops_state_machine_rules(async_client) -> None:
    r = await async_client.get("/api/v1/governed-ops/state-machine")
    assert r.status_code == 200
    body = r.json()
    states = {item["state"]: item["evidence_level"] for item in body["states"]}
    assert states["prepared_not_sent"] == "L2"
    assert states["invoice_paid"] == "L7_confirmed"
    assert "cannot_report_revenue_before_invoice_paid" in body["rules"]
