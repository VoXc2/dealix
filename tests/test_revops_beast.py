"""V12.5 Beast — RevOps full layer tests."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.revops import (
    build_finance_brief,
    compute_margin,
    create_invoice_draft,
    record_payment_confirmation,
    transition_invoice,
)
from auto_client_acquisition.revops.payment_confirmation import (
    reset_confirmations,
)


# ─────────────── Invoice state machine ───────────────


def test_invoice_draft_creation_amount_validation() -> None:
    inv = create_invoice_draft(customer_handle="Slot-A", amount_sar=499)
    assert inv.status == "draft"
    assert inv.amount_sar == 499
    assert inv.amount_halalah == 49900


def test_invoice_amount_zero_rejected() -> None:
    with pytest.raises(ValueError):
        create_invoice_draft(customer_handle="Slot-A", amount_sar=0)


def test_invoice_amount_above_50000_rejected() -> None:
    with pytest.raises(ValueError):
        create_invoice_draft(customer_handle="Slot-A", amount_sar=100000)


def test_invoice_transition_draft_to_sent() -> None:
    inv = create_invoice_draft(customer_handle="X", amount_sar=499)
    sent = transition_invoice(inv, "sent")
    assert sent.status == "sent"


def test_invoice_cannot_skip_sent() -> None:
    inv = create_invoice_draft(customer_handle="X", amount_sar=499)
    with pytest.raises(ValueError, match="invalid invoice transition"):
        transition_invoice(inv, "paid")


def test_invoice_paid_can_only_refund() -> None:
    inv = transition_invoice(
        transition_invoice(create_invoice_draft(customer_handle="X", amount_sar=499), "sent"),
        "paid",
    )
    refunded = transition_invoice(inv, "refunded")
    assert refunded.status == "refunded"
    with pytest.raises(ValueError):
        transition_invoice(refunded, "voided")


# ─────────────── Payment confirmation evidence requirement ───────────────


def test_payment_confirmation_requires_evidence() -> None:
    reset_confirmations()
    with pytest.raises(ValueError, match="evidence_reference"):
        record_payment_confirmation(
            invoice_id="inv_x",
            customer_handle="Slot-A",
            amount_sar=499,
            payment_method="bank_transfer",
            evidence_reference="",  # empty → reject
        )


def test_payment_confirmation_short_evidence_rejected() -> None:
    reset_confirmations()
    with pytest.raises(ValueError, match="evidence_reference"):
        record_payment_confirmation(
            invoice_id="inv_x", customer_handle="X", amount_sar=499,
            payment_method="bank_transfer", evidence_reference="ok",
        )


def test_payment_confirmation_with_evidence_succeeds() -> None:
    reset_confirmations()
    c = record_payment_confirmation(
        invoice_id="inv_x", customer_handle="Slot-A", amount_sar=499,
        payment_method="bank_transfer",
        evidence_reference="bank_statement_2026-05-08_ref_X12345",
    )
    assert c.amount_sar == 499
    assert c.evidence_reference.startswith("bank_statement")


# ─────────────── Margin calculator ───────────────


def test_margin_zero_revenue_returns_none_pct() -> None:
    s = compute_margin(customer_handle="X", revenue_sar=0)
    assert s.margin_pct is None
    assert s.margin_sar == 0


def test_margin_positive_revenue() -> None:
    s = compute_margin(
        customer_handle="X",
        revenue_sar=1000,
        delivery_cost_sar=200,
        support_cost_sar=100,
    )
    assert s.margin_sar == 700
    assert s.margin_pct == 0.7


def test_margin_negative_inputs_rejected() -> None:
    with pytest.raises(ValueError):
        compute_margin(customer_handle="X", revenue_sar=-1)
    with pytest.raises(ValueError):
        compute_margin(customer_handle="X", revenue_sar=100, delivery_cost_sar=-1)


# ─────────────── Finance brief ───────────────


def test_finance_brief_no_revenue_says_insufficient_data() -> None:
    brief = build_finance_brief(
        pipeline_summary={"total_revenue_sar": 0, "paid": 0, "commitments": 0,
                          "total_leads": 0},
    )
    assert brief.cash_collected_sar == 0
    assert brief.data_status == "insufficient_data"
    assert "no_paid_pilot_yet" in brief.blockers


def test_finance_brief_with_revenue_says_live() -> None:
    brief = build_finance_brief(
        pipeline_summary={"total_revenue_sar": 499, "paid": 1, "commitments": 1,
                          "total_leads": 5},
        margins=[0.7],
    )
    assert brief.data_status == "live"
    assert brief.avg_margin_pct == 0.7
    assert brief.blockers == []


def test_finance_brief_commitment_only_still_insufficient() -> None:
    brief = build_finance_brief(
        pipeline_summary={"total_revenue_sar": 0, "paid": 0, "commitments": 1,
                          "total_leads": 1},
    )
    assert brief.data_status == "insufficient_data"
    assert "no_paid_pilot_yet" in brief.blockers


# ─────────────── Router ───────────────


@pytest.mark.asyncio
async def test_revops_status_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/revops/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "revops"
    assert body["hard_gates"]["draft_invoice_is_not_revenue"] is True


@pytest.mark.asyncio
async def test_create_invoice_draft_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/revops/invoice-state",
            json={"customer_handle": "Slot-A", "amount_sar": 499,
                  "description": "Pilot"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["invoice"]["status"] == "draft"
    assert body["invoice"]["amount_halalah"] == 49900
    assert "ليس إيراد" in body["note_ar"] or "إيراد" in body["note_ar"]


@pytest.mark.asyncio
async def test_payment_confirm_rejects_short_evidence() -> None:
    from api.main import app

    reset_confirmations()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/revops/payment-confirm",
            json={
                "invoice_id": "inv_test",
                "customer_handle": "X",
                "amount_sar": 499,
                "payment_method": "bank_transfer",
                "evidence_reference": "",
            },
        )
    # Pydantic min_length=5 → 422; or 400 from app-level
    assert r.status_code in (400, 422)


@pytest.mark.asyncio
async def test_finance_brief_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/revops/finance-brief")
    assert r.status_code == 200
    body = r.json()
    for key in ("cash_collected_sar", "commitments_open_sar",
                "data_status", "blockers", "next_action_ar", "next_action_en"):
        assert key in body


@pytest.mark.asyncio
async def test_margin_snapshot_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/revops/margin-snapshot",
            json={"customer_handle": "X", "revenue_sar": 1000,
                  "delivery_cost_sar": 200, "support_cost_sar": 100},
        )
    body = r.json()
    assert body["margin_sar"] == 700
    assert body["margin_pct"] == 0.7
