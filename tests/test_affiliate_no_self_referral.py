"""Doctrine guard: a partner cannot refer themselves.

Enforced two ways: the commission engine refuses a self-flagged
referral, and the router rejects a referral whose contact email hash
matches the partner's own.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.partnership_os import affiliate_store, commission_engine


def test_commission_engine_refuses_self_referral() -> None:
    referral = {
        "id": "ref_1",
        "partner_id": "ptn_1",
        "qualified": True,
        "self_referral": True,
    }
    deal = {"id": "deal_1", "invoice_paid": True, "amount_sar": 10_000, "tier": "affiliate_lead"}
    with pytest.raises(commission_engine.CommissionRefused):
        commission_engine.calculate(referral, deal)


def test_same_email_hash_identifies_self_referral() -> None:
    partner_email = "partner@agency.sa"
    partner_hash = affiliate_store.hash_email(partner_email)
    # The same email hashed again must collide — that is the router's check.
    assert affiliate_store.hash_email("PARTNER@AGENCY.SA") == partner_hash
    assert affiliate_store.hash_email("lead@prospect.sa") != partner_hash
