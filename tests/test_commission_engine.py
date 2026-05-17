"""Commission engine — tier calculation + clawback window.

Verifies the unified 4-tier rates, the invoice-paid hard gate, and the
30-day refund clawback window.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from auto_client_acquisition.partnership_os import commission_engine
from auto_client_acquisition.partnership_os.tiers import rate_for


def _paid_deal(tier: str = "affiliate_lead", amount: float = 10_000.0) -> dict[str, object]:
    return {
        "id": "deal_1",
        "invoice_paid": True,
        "invoice_paid_at": datetime.now(timezone.utc).isoformat(),
        "amount_sar": amount,
        "tier": tier,
    }


def _qualified_referral() -> dict[str, object]:
    return {"id": "ref_1", "partner_id": "ptn_1", "qualified": True, "stage": "won"}


def test_affiliate_lead_tier_is_five_percent() -> None:
    line = commission_engine.calculate(_qualified_referral(), _paid_deal("affiliate_lead"))
    assert line.rate == 0.05
    assert line.amount_sar == 500.0


def test_qualified_referral_tier_is_ten_percent() -> None:
    line = commission_engine.calculate(
        _qualified_referral(), _paid_deal("qualified_referral")
    )
    assert line.rate == 0.10
    assert line.amount_sar == 1000.0


def test_strategic_partner_tier_rate() -> None:
    assert rate_for("strategic_partner") == 0.175
    line = commission_engine.calculate(
        _qualified_referral(), _paid_deal("strategic_partner", amount=20_000.0)
    )
    assert line.amount_sar == 3500.0


def test_commission_refused_when_invoice_not_paid() -> None:
    deal = _paid_deal()
    deal["invoice_paid"] = False
    with pytest.raises(commission_engine.CommissionRefused):
        commission_engine.calculate(_qualified_referral(), deal)


def test_tier_two_requires_qualified_referral() -> None:
    referral = {"id": "ref_2", "partner_id": "ptn_1", "qualified": False}
    with pytest.raises(commission_engine.CommissionRefused):
        commission_engine.calculate(referral, _paid_deal("qualified_referral"))


def test_unknown_tier_refused() -> None:
    with pytest.raises(commission_engine.CommissionRefused):
        commission_engine.calculate(_qualified_referral(), _paid_deal("not_a_tier"))


def test_clawback_within_window_voids_commission() -> None:
    paid = datetime.now(timezone.utc)
    refund = paid + timedelta(days=10)
    commission = {"status": "eligible", "amount_sar": 500.0, "invoice_paid_at": paid.isoformat()}
    patch = commission_engine.clawback(commission, refund.isoformat())
    assert patch["clawed_back"] is True
    assert patch["status"] == "clawed_back"
    assert patch["amount_sar"] == 0.0


def test_clawback_outside_window_keeps_commission() -> None:
    paid = datetime.now(timezone.utc)
    refund = paid + timedelta(days=45)
    commission = {"status": "eligible", "amount_sar": 500.0, "invoice_paid_at": paid.isoformat()}
    patch = commission_engine.clawback(commission, refund.isoformat())
    assert patch["clawed_back"] is False
    assert patch["amount_sar"] == 500.0


def test_clawback_window_boundary_is_thirty_days() -> None:
    paid = datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert commission_engine.within_clawback_window(
        paid.isoformat(), (paid + timedelta(days=30)).isoformat()
    )
    assert not commission_engine.within_clawback_window(
        paid.isoformat(), (paid + timedelta(days=31)).isoformat()
    )
