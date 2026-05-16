"""Tests for Governed Revenue & AI Operations contracts."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.governed_revenue_ops import (
    GovernedValueAdvanceRequest,
    ValueState,
    advance_state,
)


def test_advance_rejects_l7_confirmed_without_payment() -> None:
    result = advance_state(
        GovernedValueAdvanceRequest(
            current_state=ValueState.INVOICE_SENT,
            target_state=ValueState.INVOICE_PAID,
            founder_confirmed=True,
            payment_received=False,
        )
    )
    assert result.accepted is False
    assert "payment_received=true" in (result.rejection_reason or "")


def test_advance_rejects_l6_without_used_in_meeting() -> None:
    result = advance_state(
        GovernedValueAdvanceRequest(
            current_state=ValueState.MEETING_BOOKED,
            target_state=ValueState.SCOPE_REQUESTED,
            founder_confirmed=True,
        )
    )
    assert result.accepted is False
    assert "not allowed" in (result.rejection_reason or "")


def test_advance_invoice_paid_counts_as_revenue_and_governed_decision() -> None:
    result = advance_state(
        GovernedValueAdvanceRequest(
            current_state=ValueState.INVOICE_SENT,
            target_state=ValueState.INVOICE_PAID,
            founder_confirmed=True,
            payment_received=True,
            source_reference="crm_export_2026-05-16",
            approval_reference="approval_01",
            evidence_reference="bank_statement_ref_12345",
        )
    )
    assert result.accepted is True
    assert result.level == "L7_confirmed"
    assert result.revenue_eligible is True
    assert result.governed_value_decision_created is True
    assert result.missing_chain_links == []


@pytest.mark.asyncio
async def test_router_status_exposes_positioning_and_north_star() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/governed-revenue-ops/status")
    assert response.status_code == 200
    payload = response.json()
    assert payload["service"] == "governed_revenue_ops"
    assert "Governed Revenue & AI Operations" in payload["positioning_en"]
    assert payload["north_star"]["metric_id"] == "governed_value_decisions_created"


@pytest.mark.asyncio
async def test_router_state_machine_blocks_send_without_founder_confirmation() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/governed-revenue-ops/state-machine/advance",
            json={
                "current_state": "prepared_not_sent",
                "target_state": "sent",
                "founder_confirmed": False,
            },
        )
    assert response.status_code == 409
    detail = response.json()["detail"]
    assert detail["accepted"] is False
    assert "founder_confirmed=true" in detail["rejection_reason"]


@pytest.mark.asyncio
async def test_router_services_exposes_three_featured_offers() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/governed-revenue-ops/services")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["featured_first_meeting"]) == 3
