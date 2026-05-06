"""RX — revenue pipeline truth tests.

Asserts the canonical revenue truth labels (revenue ≠ draft invoice;
verbal ≠ commitment) cannot be silently flipped.
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.revenue_pipeline import (
    PipelineStage,
    advance_stage,
    counts_as_commitment,
    counts_as_revenue,
    snapshot_revenue_truth,
)
from auto_client_acquisition.revenue_pipeline.lead import Lead
from auto_client_acquisition.revenue_pipeline.pipeline import (
    RevenuePipeline,
    get_default_pipeline,
)


# ────────────── stage_policy ──────────────


def test_stage_advance_forward_only() -> None:
    new = advance_stage(current="warm_intro_selected", target="message_drafted")
    assert new == "message_drafted"


def test_stage_advance_skip_forward_blocked() -> None:
    """Cannot skip from warm_intro_selected straight to payment_received."""
    with pytest.raises(ValueError):
        advance_stage(current="warm_intro_selected", target="payment_received")


def test_pilot_offered_can_advance_to_payment_received() -> None:
    """Skipping commitment_received and going straight to payment_received
    is allowed (some customers pay without prior signed intent)."""
    new = advance_stage(current="pilot_offered", target="payment_received")
    assert new == "payment_received"


def test_any_stage_can_close_lost() -> None:
    for s in ("warm_intro_selected", "diagnostic_delivered", "pilot_offered",
              "commitment_received", "delivered"):
        new = advance_stage(current=s, target="closed_lost")
        assert new == "closed_lost"


def test_closed_won_is_terminal() -> None:
    with pytest.raises(ValueError):
        advance_stage(current="closed_won", target="upsell_offered")


def test_counts_as_revenue_only_after_payment() -> None:
    assert counts_as_revenue("warm_intro_selected") is False
    assert counts_as_revenue("diagnostic_delivered") is False
    assert counts_as_revenue("pilot_offered") is False
    assert counts_as_revenue("commitment_received") is False
    assert counts_as_revenue("payment_received") is True
    assert counts_as_revenue("delivered") is True
    assert counts_as_revenue("closed_won") is True


def test_counts_as_commitment_includes_commitment_and_above() -> None:
    assert counts_as_commitment("pilot_offered") is False
    assert counts_as_commitment("commitment_received") is True
    assert counts_as_commitment("payment_received") is True


# ────────────── pipeline ──────────────


def test_pipeline_advance_to_commitment_requires_evidence() -> None:
    p = RevenuePipeline()
    p.add(Lead.make(slot_id="A", sector="b2b"))
    lead = p.list_all()[0]
    p.advance(lead.id, "message_drafted")
    p.advance(lead.id, "founder_sent_manually")
    p.advance(lead.id, "replied")
    p.advance(lead.id, "diagnostic_requested")
    p.advance(lead.id, "diagnostic_delivered")
    p.advance(lead.id, "pilot_offered")
    # Verbal yes — NO evidence → MUST raise
    with pytest.raises(ValueError, match="commitment_evidence"):
        p.advance(lead.id, "commitment_received")
    # With evidence — OK
    updated = p.advance(
        lead.id, "commitment_received",
        commitment_evidence="email_2026-MM-DD_signed_intent_screenshot.png",
    )
    assert updated.stage == "commitment_received"


def test_pipeline_advance_to_payment_requires_evidence_and_amount() -> None:
    p = RevenuePipeline()
    p.add(Lead.make(slot_id="B", sector="b2b"))
    lead = p.list_all()[0]
    # Walk to pilot_offered
    for tgt in ("message_drafted", "founder_sent_manually", "replied",
                "diagnostic_requested", "diagnostic_delivered",
                "pilot_offered"):
        p.advance(lead.id, tgt)
    # No evidence, no amount → raise
    with pytest.raises(ValueError, match="payment_evidence"):
        p.advance(lead.id, "payment_received")
    # Evidence but no amount → raise
    with pytest.raises(ValueError, match="actual_amount_sar"):
        p.advance(
            lead.id, "payment_received",
            payment_evidence="moyasar_dashboard_screenshot.png",
        )
    # Both → OK
    updated = p.advance(
        lead.id, "payment_received",
        payment_evidence="moyasar_dashboard_screenshot.png",
        actual_amount_sar=499,
    )
    assert updated.stage == "payment_received"
    assert updated.actual_amount_sar == 499


def test_pipeline_summary_counts_correctly() -> None:
    p = RevenuePipeline()
    p.add(Lead.make(slot_id="A", sector="b2b"))
    p.add(Lead.make(slot_id="B", sector="b2b"))
    summary = p.summary()
    assert summary["total_leads"] == 2
    assert summary["paid"] == 0
    assert summary["commitments"] == 0
    assert summary["total_revenue_sar"] == 0


# ────────────── revenue truth snapshot ──────────────


def test_revenue_truth_with_no_data_says_no() -> None:
    truth = snapshot_revenue_truth(
        pipeline_summary={"total_leads": 0, "commitments": 0, "paid": 0,
                          "total_revenue_sar": 0},
        proof_event_files_count=0,
    )
    assert truth.revenue_live is False
    assert truth.v12_1_unlocked is False
    assert "no_paid_pilot_yet" in truth.blockers
    assert "no_real_proof_event_logged_yet" in truth.blockers


def test_revenue_truth_with_commitment_unlocks_v12_1() -> None:
    truth = snapshot_revenue_truth(
        pipeline_summary={"total_leads": 1, "commitments": 1, "paid": 0,
                          "total_revenue_sar": 0},
        proof_event_files_count=0,
    )
    assert truth.revenue_live is False  # cash hasn't landed
    assert truth.v12_1_unlocked is True


def test_revenue_truth_with_paid_pilot_flips_revenue_live() -> None:
    truth = snapshot_revenue_truth(
        pipeline_summary={"total_leads": 1, "commitments": 1, "paid": 1,
                          "total_revenue_sar": 499},
        proof_event_files_count=2,
    )
    assert truth.revenue_live is True
    assert truth.v12_1_unlocked is True
    assert truth.blockers == []


def test_revenue_truth_with_proof_event_alone_unlocks_v12_1() -> None:
    truth = snapshot_revenue_truth(
        pipeline_summary={"total_leads": 0, "commitments": 0, "paid": 0,
                          "total_revenue_sar": 0},
        proof_event_files_count=1,
    )
    assert truth.v12_1_unlocked is True
    assert truth.revenue_live is False


# ────────────── Router ──────────────


@pytest.mark.asyncio
async def test_status_endpoint() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/revenue-pipeline/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "revenue_pipeline"
    assert body["hard_gates"]["no_fake_revenue"] is True


@pytest.mark.asyncio
async def test_create_lead_then_summary_no_revenue() -> None:
    from api.main import app

    get_default_pipeline().reset()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r1 = await client.post(
            "/api/v1/revenue-pipeline/lead",
            json={"slot_id": "A", "sector": "b2b_services", "region": "riyadh"},
        )
        assert r1.status_code == 200
        r2 = await client.get("/api/v1/revenue-pipeline/summary")
    body = r2.json()
    assert body["pipeline_summary"]["total_leads"] == 1
    assert body["pipeline_summary"]["paid"] == 0
    assert body["revenue_truth"]["revenue_live"] is False
    assert "no_paid_pilot_yet" in body["revenue_truth"]["blockers"]


@pytest.mark.asyncio
async def test_advance_endpoint_blocks_payment_without_evidence() -> None:
    from api.main import app

    get_default_pipeline().reset()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r1 = await client.post(
            "/api/v1/revenue-pipeline/lead",
            json={"slot_id": "C", "sector": "b2b_services"},
        )
        lid = r1.json()["lead"]["id"]
        # Walk forward
        for tgt in ("message_drafted", "founder_sent_manually", "replied",
                    "diagnostic_requested", "diagnostic_delivered",
                    "pilot_offered"):
            r = await client.post(
                "/api/v1/revenue-pipeline/advance",
                json={"lead_id": lid, "target_stage": tgt},
            )
            assert r.status_code == 200, f"failed at {tgt}: {r.text}"
        # Now payment without evidence → 400
        r = await client.post(
            "/api/v1/revenue-pipeline/advance",
            json={"lead_id": lid, "target_stage": "payment_received"},
        )
        assert r.status_code == 400
        assert "payment_evidence" in r.text


@pytest.mark.asyncio
async def test_summary_endpoint_returns_revenue_truth_with_blockers() -> None:
    from api.main import app

    get_default_pipeline().reset()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/revenue-pipeline/summary")
    body = r.json()
    truth = body["revenue_truth"]
    assert "revenue_live" in truth
    assert "v12_1_unlocked" in truth
    assert "blockers" in truth
    assert "next_action_ar" in truth
    assert "next_action_en" in truth
