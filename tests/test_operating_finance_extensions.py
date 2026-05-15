"""Tests for operating finance extensions."""

from __future__ import annotations

from auto_client_acquisition.operating_finance_os import (
    OfferUnitEconomics,
    RetainerEconomics,
    ai_cost_per_proof_pack_usd,
    cost_guard_breached,
    estimate_run_cost_usd,
    margin_percent_by_offer,
    total_ai_run_cost_usd,
)
from auto_client_acquisition.operating_finance_os.margin_protection import MarginAction, margin_protection_action


def test_offer_gross_margin() -> None:
    o = OfferUnitEconomics(
        offer_id="ri_sprint",
        price=10000,
        delivery_hours=20,
        qa_hours=4,
        governance_overhead_hours=3,
        ai_cost=200,
        blended_hour_cost=150,
    )
    assert o.gross_margin > 0.4


def test_margin_by_offer_map() -> None:
    o = OfferUnitEconomics("x", 5000, 10, 2, 2, 50, 100)
    m = margin_percent_by_offer({"x": o})
    assert m["x"] == round(100.0 * o.gross_margin, 2)


def test_retainer_health_ratio() -> None:
    r = RetainerEconomics(
        mrr=20000,
        monthly_delivery_hours=40,
        monthly_ai_cost=400,
        blended_hour_cost=200,
    )
    assert r.health_ratio > 1.0


def test_ai_cost_helpers() -> None:
    assert total_ai_run_cost_usd(0.1, 0.2) == 0.3
    assert ai_cost_per_proof_pack_usd(0.05, 0.1, 0.02) == 0.17
    assert estimate_run_cost_usd("economy_route", 1000, 500) > 0
    assert cost_guard_breached(price=1000, ai_cost=200, max_ai_to_price_ratio=0.12)


def test_margin_protection_no_action_when_healthy() -> None:
    assert margin_protection_action(gross_margin=0.5) == MarginAction.NO_ACTION
