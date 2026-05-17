"""Unit tests for the Affiliate OS module — Dealix Full Ops.

Covers the tiered commission engine, the eligibility gate, refund
clawback, affiliate-message compliance, partner-application scoring,
and the JSONL store.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.affiliate_os import (
    AffiliateTier,
    PartnerApplication,
    apply_clawback,
    check_affiliate_message,
    commission_eligible,
    commission_rate,
    compute_commission,
    is_handoff_tier,
    score_application,
    should_clawback,
    store,
    tier_table,
)
from auto_client_acquisition.affiliate_os.commission import CommissionStatus

# ─────────────── Tiers ───────────────


def test_commission_rate_per_tier() -> None:
    assert commission_rate(AffiliateTier.TIER_1_AFFILIATE_LEAD) == 0.05
    assert commission_rate(AffiliateTier.TIER_2_QUALIFIED_REFERRAL) == 0.10
    assert commission_rate(AffiliateTier.TIER_3_STRATEGIC_PARTNER) == 0.175
    assert commission_rate(AffiliateTier.TIER_4_IMPLEMENTATION_PARTNER) == 0.0


def test_tier4_is_handoff() -> None:
    assert is_handoff_tier(AffiliateTier.TIER_4_IMPLEMENTATION_PARTNER) is True
    assert is_handoff_tier(AffiliateTier.TIER_1_AFFILIATE_LEAD) is False


def test_tier_table_has_four_rows() -> None:
    rows = tier_table()
    assert len(rows) == 4
    assert {r["tier"] for r in rows} == {t.value for t in AffiliateTier}


# ─────────────── Commission computation ───────────────


def test_compute_commission_math() -> None:
    c = compute_commission(
        affiliate_id="aff_1",
        tier=AffiliateTier.TIER_2_QUALIFIED_REFERRAL,
        deal_amount_sar=4999,
    )
    assert c.rate == 0.10
    assert c.amount_sar == round(4999 * 0.10, 2)
    assert c.status == CommissionStatus.PENDING.value


def test_compute_commission_handoff_tier_is_zero() -> None:
    c = compute_commission(
        affiliate_id="aff_1",
        tier=AffiliateTier.TIER_4_IMPLEMENTATION_PARTNER,
        deal_amount_sar=10000,
    )
    assert c.amount_sar == 0.0
    assert "handoff" in c.notes


def test_compute_commission_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        compute_commission(
            affiliate_id="",
            tier=AffiliateTier.TIER_1_AFFILIATE_LEAD,
            deal_amount_sar=100,
        )
    with pytest.raises(ValueError):
        compute_commission(
            affiliate_id="aff_1",
            tier=AffiliateTier.TIER_1_AFFILIATE_LEAD,
            deal_amount_sar=0,
        )


# ─────────────── Eligibility gate ───────────────


def test_eligibility_blocks_unpaid_invoice() -> None:
    eligible, reasons = commission_eligible(invoice_status="draft")
    assert eligible is False
    assert any("invoice_not_paid" in r for r in reasons)


def test_eligibility_passes_on_paid_clean_lead() -> None:
    eligible, reasons = commission_eligible(invoice_status="paid")
    assert eligible is True
    assert reasons == ()


def test_eligibility_blocks_disallowed_lead() -> None:
    eligible, reasons = commission_eligible(
        invoice_status="paid",
        lead_flags=["duplicate", "out_of_icp"],
    )
    assert eligible is False
    assert any("disallowed_lead:duplicate" in r for r in reasons)
    assert any("disallowed_lead:out_of_icp" in r for r in reasons)


# ─────────────── Clawback ───────────────


def test_clawback_within_window() -> None:
    assert should_clawback(
        invoice_status="refunded",
        paid_at="2026-01-01T00:00:00+00:00",
        refunded_at="2026-01-10T00:00:00+00:00",
    ) is True


def test_no_clawback_outside_window() -> None:
    assert should_clawback(
        invoice_status="refunded",
        paid_at="2026-01-01T00:00:00+00:00",
        refunded_at="2026-03-01T00:00:00+00:00",
    ) is False


def test_no_clawback_when_not_refunded() -> None:
    assert should_clawback(invoice_status="paid") is False


def test_clawback_conservative_when_dates_missing() -> None:
    assert should_clawback(invoice_status="refunded") is True


def test_apply_clawback_flips_status() -> None:
    c = compute_commission(
        affiliate_id="aff_1",
        tier=AffiliateTier.TIER_1_AFFILIATE_LEAD,
        deal_amount_sar=499,
    )
    clawed = apply_clawback(c)
    assert clawed.status == CommissionStatus.CLAWED_BACK.value
    # original is untouched (immutable replace)
    assert c.status == CommissionStatus.PENDING.value


# ─────────────── Compliance ───────────────


def test_compliance_flags_missing_disclosure() -> None:
    result = check_affiliate_message("Check out Dealix, it is great!")
    assert result.compliant is False
    assert "missing_disclosure" in result.violations


def test_compliance_flags_guarantee_language() -> None:
    result = check_affiliate_message(
        "Disclosure: affiliate link. Dealix gives you guaranteed ROI."
    )
    assert result.compliant is False
    assert "guaranteed_outcome_language" in result.violations


def test_compliance_flags_cold_whatsapp() -> None:
    result = check_affiliate_message("affiliate disclosure", channel="cold_whatsapp")
    assert "cold_whatsapp" in result.violations


def test_compliance_passes_clean_disclosed_message() -> None:
    msg = "أوصي بـDealix لفريقك. تنويه: قد أحصل على عمولة إحالة عبر الرابط."
    result = check_affiliate_message(msg)
    assert result.has_disclosure is True
    assert result.compliant is True
    assert result.violations == []


# ─────────────── Partner application scoring ───────────────


def test_score_application_strong_candidate() -> None:
    app = PartnerApplication(
        audience_type="b2b",
        audience_in_gcc=True,
        is_consultant_or_operator=True,
        previous_b2b_referrals=3,
        content_quality_good=True,
        trusts_brand=True,
        promotion_plan_clear=True,
    )
    scored = score_application(app)
    assert scored.score == 16
    assert scored.recommendation == "recommend_accept"


def test_score_application_spam_rejected() -> None:
    app = PartnerApplication(
        audience_type="b2c",
        spam_behavior=True,
        fake_audience_suspected=True,
        accepts_disclosure=False,
        promotion_plan_clear=False,
    )
    scored = score_application(app)
    assert scored.score < 4
    assert scored.recommendation == "recommend_reject"


def test_score_application_mid_needs_review() -> None:
    app = PartnerApplication(
        audience_type="b2b",
        is_consultant_or_operator=True,
        promotion_plan_clear=True,
    )
    scored = score_application(app)
    assert 4 <= scored.score < 10
    assert scored.recommendation == "needs_review"


# ─────────────── Store ───────────────


@pytest.fixture()
def isolated_store(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AFFILIATES_PATH", str(tmp_path / "aff.jsonl"))
    monkeypatch.setenv(
        "DEALIX_AFFILIATE_COMMISSIONS_PATH", str(tmp_path / "com.jsonl")
    )
    monkeypatch.setenv(
        "DEALIX_AFFILIATE_PAYOUTS_PATH", str(tmp_path / "pay.jsonl")
    )
    store.clear_for_test()
    yield
    store.clear_for_test()


def test_store_register_and_list_affiliate(isolated_store) -> None:
    aff = store.register_affiliate(handle="creator_a", email="a@example.com")
    assert aff.status == "pending"
    assert store.get_affiliate(aff.affiliate_id) is not None
    assert len(store.list_affiliates(status="pending")) == 1
    assert store.list_affiliates(status="active") == []


def test_store_commission_lifecycle(isolated_store) -> None:
    c = compute_commission(
        affiliate_id="aff_1",
        tier=AffiliateTier.TIER_1_AFFILIATE_LEAD,
        deal_amount_sar=499,
    )
    store.save_commission(c)
    fetched = store.get_commission(c.commission_id)
    assert fetched is not None
    updated = store.update_commission(
        c.commission_id, status=CommissionStatus.ELIGIBLE.value
    )
    assert updated is not None
    assert updated.status == CommissionStatus.ELIGIBLE.value


def test_store_payout_requires_approval_id(isolated_store) -> None:
    with pytest.raises(ValueError):
        store.record_payout(
            commission_id="com_x",
            affiliate_id="aff_1",
            amount_sar=24.95,
            approval_id="",
        )
