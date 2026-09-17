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
async def test_legacy_projection_is_never_payable_even_with_evidence():
    tracker = ReferralTracker()
    referral = await tracker.create_referral(
        "partner-1",
        ReferralData(company_name="Acme", contact_name="Buyer", contact_email="buyer@acme.sa"),
    )
    await tracker.convert(referral.id, 50000)
    engine = CommissionEngine(tracker)
    commission = await engine.calculate(referral.id)

    missing = await engine.pay(commission.id)
    assert missing.success is False
    assert "legacy_projection_not_payable" in missing.errors

    with_evidence = await engine.pay(
        commission.id,
        approval_reference="APR-verified-001",
        verified_collection_reference="COLL-bank-001",
        clearing_complete=True,
    )
    assert with_evidence.success is False
    assert with_evidence.status == "hold"
    assert "v2_verified_collection_decision_required" in with_evidence.errors
    assert engine.get_commission(commission.id).status == "projected_unpaid"
    assert engine.get_commission(commission.id).paid_at is None

    stats = engine.get_stats()
    assert stats["total_projected"] == 5000
    assert stats["projected_count"] == 1
    assert stats["total_pending"] == 0
    assert stats["pending_count"] == 0


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
