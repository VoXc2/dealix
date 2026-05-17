"""Affiliate / Partner Commission Machine — commission, clawback, payout."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from auto_client_acquisition.partnership_os import affiliate_store as store


@pytest.fixture(autouse=True)
def _isolated_store(tmp_path, monkeypatch):
    for env_var in store._PATH_DEFAULTS:
        monkeypatch.setenv(env_var, str(tmp_path / f"{env_var}.jsonl"))
    store.clear_for_test()
    yield
    store.clear_for_test()


def _referral_at(tier: str, *, disclosure: bool = True):
    """Return (partner, referral) with the referral in `invoice_paid`."""
    partner = store.apply_partner(
        display_name="Acme Partner",
        email="partner@acme.sa",
        partner_category="consultant",
        plan_text="GCC operator who promotes Dealix monthly with full disclosure.",
        disclosure_accepted=True,
    )
    store.approve_partner(partner_id=partner.partner_id, tier=tier)
    partner = store.get_partner(partner.partner_id)
    link = store.list_links(partner_id=partner.partner_id)[0]
    referral = store.submit_referral(
        code=link.code, lead_company="Buyer Co", lead_email="buyer@buyer.sa"
    )
    store.qualify_referral(
        affiliate_referral_id=referral.affiliate_referral_id,
        disclosure_present=disclosure,
    )
    store.mark_invoice_paid(
        affiliate_referral_id=referral.affiliate_referral_id,
        invoice_id="inv_001",
        deal_amount_sar=10_000,
    )
    return partner, store.get_referral(referral.affiliate_referral_id)


def test_commission_blocked_before_invoice_paid():
    partner = store.apply_partner(
        display_name="P", email="p@p.sa", disclosure_accepted=True,
        plan_text="GCC consultant promoting Dealix with disclosure on every post.",
    )
    store.approve_partner(partner_id=partner.partner_id, tier="tier2")
    link = store.list_links(partner_id=partner.partner_id)[0]
    referral = store.submit_referral(
        code=link.code, lead_company="Buyer", lead_email="b@b.sa"
    )
    store.qualify_referral(
        affiliate_referral_id=referral.affiliate_referral_id, disclosure_present=True
    )
    # qualified but no invoice_paid event yet
    with pytest.raises(ValueError, match="invoice_paid"):
        store.calculate_commission(
            affiliate_referral_id=referral.affiliate_referral_id
        )


def test_commission_blocked_without_disclosure():
    _, referral = _referral_at("tier2", disclosure=False)
    with pytest.raises(ValueError, match="disclosure"):
        store.calculate_commission(
            affiliate_referral_id=referral.affiliate_referral_id
        )


@pytest.mark.parametrize(
    "tier,expected_pct,expected_sar",
    [("tier1", 5, 500), ("tier2", 10, 1000), ("tier3", 15, 1500)],
)
def test_commission_pct_by_tier(tier, expected_pct, expected_sar):
    _, referral = _referral_at(tier)
    commission = store.calculate_commission(
        affiliate_referral_id=referral.affiliate_referral_id
    )
    assert commission.pct == expected_pct
    assert commission.commission_sar == expected_sar
    assert commission.base_amount_sar == 10_000


def test_tier3_pct_override_capped_at_20():
    _, referral = _referral_at("tier3")
    with pytest.raises(ValueError, match="20"):
        store.calculate_commission(
            affiliate_referral_id=referral.affiliate_referral_id,
            pct_override=25,
        )


def test_tier4_requires_flat_fee():
    _, referral = _referral_at("tier4")
    with pytest.raises(ValueError, match="flat_fee_sar"):
        store.calculate_commission(
            affiliate_referral_id=referral.affiliate_referral_id
        )
    commission = store.calculate_commission(
        affiliate_referral_id=referral.affiliate_referral_id,
        flat_fee_sar=2_500,
    )
    assert commission.commission_sar == 2_500
    assert commission.pct == 0


def test_no_double_commission_for_same_referral():
    _, referral = _referral_at("tier2")
    store.calculate_commission(
        affiliate_referral_id=referral.affiliate_referral_id
    )
    with pytest.raises(ValueError, match="already exists"):
        store.calculate_commission(
            affiliate_referral_id=referral.affiliate_referral_id
        )


def test_clawback_inside_window_succeeds():
    _, referral = _referral_at("tier2")
    commission = store.calculate_commission(
        affiliate_referral_id=referral.affiliate_referral_id
    )
    clawed = store.clawback_commission(
        commission_id=commission.commission_id, reason="refund issued day 5"
    )
    assert clawed is not None
    assert clawed.status == store.CommissionStatus.CLAWED_BACK.value
    ref = store.get_referral(referral.affiliate_referral_id)
    assert ref.status == store.AffiliateReferralStatus.CLAWED_BACK.value


def test_clawback_after_window_rejected(monkeypatch):
    # Force invoice_paid_at 40 days in the past → clawback deadline expired.
    # A nested context restores _now without undoing the fixture's env vars.
    old = (datetime.now(timezone.utc) - timedelta(days=40)).isoformat()
    with monkeypatch.context() as m:
        m.setattr(store, "_now", lambda: old)
        _, referral = _referral_at("tier2")
    commission = store.calculate_commission(
        affiliate_referral_id=referral.affiliate_referral_id
    )
    with pytest.raises(ValueError, match="window"):
        store.clawback_commission(
            commission_id=commission.commission_id, reason="late refund"
        )


def test_payout_requires_approved_commission():
    partner, referral = _referral_at("tier2")
    commission = store.calculate_commission(
        affiliate_referral_id=referral.affiliate_referral_id
    )
    # Not approved yet → payout must be rejected.
    with pytest.raises(ValueError, match="not approved"):
        store.mark_payout_paid(
            partner_id=partner.partner_id,
            commission_ids=[commission.commission_id],
        )
    store.approve_commission(commission_id=commission.commission_id)
    payout = store.mark_payout_paid(
        partner_id=partner.partner_id,
        commission_ids=[commission.commission_id],
    )
    assert payout.total_sar == 1000
    assert payout.status == store.PayoutStatus.PAID.value
    assert store.get_commission(commission.commission_id).status == (
        store.CommissionStatus.PAID.value
    )


def test_clawback_blocked_after_payout():
    partner, referral = _referral_at("tier2")
    commission = store.calculate_commission(
        affiliate_referral_id=referral.affiliate_referral_id
    )
    store.approve_commission(commission_id=commission.commission_id)
    store.mark_payout_paid(
        partner_id=partner.partner_id,
        commission_ids=[commission.commission_id],
    )
    with pytest.raises(ValueError, match="already paid"):
        store.clawback_commission(
            commission_id=commission.commission_id, reason="too late"
        )


def test_dashboard_totals():
    partner, referral = _referral_at("tier2")
    commission = store.calculate_commission(
        affiliate_referral_id=referral.affiliate_referral_id
    )
    store.approve_commission(commission_id=commission.commission_id)
    data = store.partner_dashboard(partner.partner_id)
    assert data["totals_sar"]["pending"] == 1000
    assert data["totals_sar"]["paid"] == 0
