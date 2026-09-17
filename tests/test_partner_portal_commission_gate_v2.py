import pytest

from integrations.partner_portal.commission_engine import CommissionEngine
from integrations.partner_portal.referral_tracking import ReferralData, ReferralTracker


@pytest.mark.asyncio
async def test_won_referral_is_not_earned_commission():
    tracker = ReferralTracker()
    referral = await tracker.create_referral(
        "partner-1",
        ReferralData(
            company_name="Acme Saudi",
            contact_name="Buyer",
            contact_email="buyer@example.sa",
        ),
    )
    converted = await tracker.convert(referral.id, 100000)
    assert converted.success is True
    assert converted.deal_value_sar == 100000
    assert converted.commission_amount_sar == 0
    assert converted.commission_rate == 0
    assert "won_unpaid" in converted.notes
    assert tracker.get_referral(referral.id).commission_amount_sar == 0
    assert tracker.get_stats()["total_commission"] == 0


@pytest.mark.asyncio
async def test_commission_engine_uses_injected_canonical_tracker_as_projection_only():
    tracker = ReferralTracker()
    referral = await tracker.create_referral(
        "partner-1",
        ReferralData(
            company_name="Acme Saudi",
            contact_name="Buyer",
            contact_email="buyer@example.sa",
        ),
    )
    converted = await tracker.convert(referral.id, 100000)
    assert converted.success is True

    engine = CommissionEngine(tracker)
    commission = await engine.calculate(referral.id)
    assert commission.referral_id == referral.id
    assert commission.amount_sar == 10000
    assert commission.status == "projected_unpaid"
    assert commission.paid_at is None


@pytest.mark.asyncio
async def test_commission_payment_is_fail_closed_without_evidence():
    tracker = ReferralTracker()
    referral = await tracker.create_referral(
        "partner-1",
        ReferralData(company_name="Acme", contact_name="Buyer", contact_email="buyer@acme.sa"),
    )
    await tracker.convert(referral.id, 50000)
    engine = CommissionEngine(tracker)
    commission = await engine.calculate(referral.id)

    result = await engine.pay(commission.id)
    assert result.success is False
    assert "approval_reference_required" in result.errors
    assert "verified_collection_reference_required" in result.errors
    assert "clearing_period_not_complete" in result.errors
    assert engine.get_commission(commission.id).status == "projected_unpaid"


@pytest.mark.asyncio
async def test_commission_payment_can_stage_only_with_required_evidence():
    tracker = ReferralTracker()
    referral = await tracker.create_referral(
        "partner-1",
        ReferralData(company_name="Acme", contact_name="Buyer", contact_email="buyer@acme.sa"),
    )
    await tracker.convert(referral.id, 50000)
    engine = CommissionEngine(tracker)
    commission = await engine.calculate(referral.id)

    result = await engine.pay(
        commission.id,
        approval_reference="APR-verified-001",
        verified_collection_reference="COLL-bank-001",
        clearing_complete=True,
    )
    assert result.success is True
    assert result.amount_sar == 5000
    assert result.status == "staged_not_paid"
    assert result.payment_method == "external_payment_not_executed"
    assert engine.get_commission(commission.id).status == "approved_for_payment"
    assert engine.get_commission(commission.id).paid_at is None

    replay = await engine.pay(
        commission.id,
        approval_reference="APR-verified-001",
        verified_collection_reference="COLL-bank-001",
        clearing_complete=True,
    )
    assert replay.success is False
    assert replay.status == "staged_not_paid"
    assert replay.errors == ["commission_already_staged"]
    assert engine.get_commission(commission.id).paid_at is None


@pytest.mark.asyncio
async def test_partner_economics_v2_endpoint_uses_motion_authority():
    from integrations.partner_portal.api import partner_economics_v2

    payload = await partner_economics_v2()
    assert payload["authority"] == "dealix.commercial.partner_program_v2"
    assert payload["services"]["scout"] == 0.075
    assert payload["services"]["closer_sector_partner"] == 0.15
    assert payload["saas"]["growth_partner"] == 0.25
    assert payload["saas_commission_months"] == 12
    assert payload["protection_days"] == 120
    assert payload["payment_truth"] == "staged_not_paid_until_external_payment_receipt"
