"""Sales OS — partner engine: classification + commission guardrails."""

from __future__ import annotations

from auto_client_acquisition.sales_os.partner_engine import (
    CommissionContext,
    PartnerType,
    classify_partner,
    commission_eligible,
)


def test_classify_referral() -> None:
    assert classify_partner(can_refer=True) == PartnerType.REFERRAL


def test_classify_implementation() -> None:
    assert classify_partner(can_deliver=True) == PartnerType.IMPLEMENTATION


def test_classify_co_selling() -> None:
    assert classify_partner(sells_alongside=True) == PartnerType.CO_SELLING


def test_classify_service_exchange() -> None:
    assert classify_partner(trades_service=True) == PartnerType.SERVICE_EXCHANGE


def test_classify_white_label() -> None:
    assert classify_partner(rebrands_product=True) == PartnerType.WHITE_LABEL


def test_white_label_wins_when_multiple_capabilities() -> None:
    assert (
        classify_partner(can_refer=True, can_deliver=True, rebrands_product=True)
        == PartnerType.WHITE_LABEL
    )


def test_no_signal_defaults_to_referral() -> None:
    assert classify_partner() == PartnerType.REFERRAL


def test_commission_rejected_before_invoice_paid() -> None:
    ctx = CommissionContext(partner_type=PartnerType.REFERRAL, invoice_paid=False)
    ok, reason = commission_eligible(ctx)
    assert not ok
    assert reason == "no_payout_before_invoice_paid"


def test_commission_allowed_after_invoice_paid() -> None:
    ctx = CommissionContext(partner_type=PartnerType.REFERRAL, invoice_paid=True)
    ok, reason = commission_eligible(ctx)
    assert ok
    assert reason == "eligible"


def test_white_label_blocked_under_three_proof_packs() -> None:
    ctx = CommissionContext(
        partner_type=PartnerType.WHITE_LABEL, invoice_paid=True, completed_proof_packs=2
    )
    ok, reason = commission_eligible(ctx)
    assert not ok
    assert reason == "white_label_requires_3_proof_packs"


def test_white_label_allowed_at_exactly_three_proof_packs() -> None:
    ctx = CommissionContext(
        partner_type=PartnerType.WHITE_LABEL, invoice_paid=True, completed_proof_packs=3
    )
    ok, reason = commission_eligible(ctx)
    assert ok
    assert reason == "eligible"


def test_white_label_still_blocked_before_invoice_even_with_packs() -> None:
    ctx = CommissionContext(
        partner_type=PartnerType.WHITE_LABEL, invoice_paid=False, completed_proof_packs=5
    )
    ok, reason = commission_eligible(ctx)
    assert not ok
    assert reason == "no_payout_before_invoice_paid"
