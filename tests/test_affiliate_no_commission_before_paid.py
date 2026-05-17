"""Doctrine guard: no commission before the deal invoice is paid.

A commission line must never exist for a deal whose invoice has not
been paid. The commission engine is the single enforcement point.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.partnership_os import commission_engine


def test_commission_refused_when_invoice_unpaid() -> None:
    referral = {"id": "ref_1", "partner_id": "ptn_1", "qualified": True}
    deal = {"id": "deal_1", "invoice_paid": False, "amount_sar": 10_000, "tier": "affiliate_lead"}
    with pytest.raises(commission_engine.CommissionRefused):
        commission_engine.calculate(referral, deal)


def test_commission_allowed_only_when_invoice_paid() -> None:
    referral = {"id": "ref_1", "partner_id": "ptn_1", "qualified": True}
    deal = {"id": "deal_1", "invoice_paid": True, "amount_sar": 10_000, "tier": "affiliate_lead"}
    line = commission_engine.calculate(referral, deal)
    assert line.amount_sar == 500.0
    assert line.status == "eligible"
