from decimal import Decimal

import pytest

from dealix.commercial.partner_program_v2 import (
    ATTRIBUTION_MAX_EXTENSION_DAYS,
    ATTRIBUTION_PROTECTION_DAYS,
    DEFAULT_SPLIT,
    allocate_commission_pool,
    attribution_window_days,
    calculate_nccr,
    calculate_partner_commission,
    commission_rate_for,
    requires_compliance_hold,
    validate_attribution_split,
)


def test_nccr_deducts_tax_refunds_and_pass_through_costs():
    nccr = calculate_nccr({
        "collected_cash_sar": 100000,
        "vat_sar": 13043.48,
        "refunds_sar": 5000,
        "third_party_licenses_at_cost_sar": 10000,
        "government_fees_sar": 1000,
    })
    assert nccr == Decimal("70956.52")


def test_nccr_never_goes_negative():
    assert calculate_nccr({"collected_cash_sar": 100, "refunds_sar": 200}) == Decimal("0.00")


@pytest.mark.parametrize(
    "economics",
    [
        {"collected_cash_sar": -1},
        {"collected_cash_sar": 1000, "refunds_sar": -1},
        {"collected_cash_sar": 1000, "vat_sar": -1},
    ],
)
def test_nccr_rejects_negative_financial_inputs(economics):
    with pytest.raises(ValueError):
        calculate_nccr(economics)


def test_service_rates_are_motion_based():
    assert commission_rate_for("scout", "services") == Decimal("0.075")
    assert commission_rate_for("growth_partner", "services") == Decimal("0.10")
    assert commission_rate_for("closer_sector_partner", "services") == Decimal("0.15")


def test_unknown_revenue_type_fails_closed():
    with pytest.raises(ValueError):
        commission_rate_for("scout", "license")


def test_saas_rates_are_recurring_and_capped_at_twelve_months():
    assert commission_rate_for("growth_partner", "saas") == Decimal("0.25")
    decision = calculate_partner_commission(
        motion="growth_partner",
        revenue_type="saas",
        economics={"collected_cash_sar": 5000},
        verified_collection=True,
        recurring_month_index=12,
    )
    assert decision.eligible is True
    assert decision.commission_sar == Decimal("1250.00")
    assert decision.recurring_month_limit == 12


def test_saas_requires_explicit_recurring_month_index():
    decision = calculate_partner_commission(
        motion="growth_partner",
        revenue_type="saas",
        economics={"collected_cash_sar": 5000},
        verified_collection=True,
    )
    assert decision.eligible is False
    assert decision.commission_sar == Decimal("0")
    assert "recurring_month_index_required" in decision.reasons


def test_month_thirteen_is_not_commissionable():
    decision = calculate_partner_commission(
        motion="growth_partner",
        revenue_type="saas",
        economics={"collected_cash_sar": 5000},
        verified_collection=True,
        recurring_month_index=13,
    )
    assert decision.eligible is False
    assert "outside_saas_commission_window" in decision.reasons


def test_invoice_or_won_without_verified_cash_is_hold():
    decision = calculate_partner_commission(
        motion="co_sell_partner",
        revenue_type="services",
        economics={"collected_cash_sar": 100000},
        verified_collection=False,
    )
    assert decision.eligible is False
    assert decision.commission_sar == Decimal("0")
    assert "verified_collection_missing" in decision.reasons


def test_duplicate_existing_pipeline_is_not_commissionable():
    decision = calculate_partner_commission(
        motion="scout",
        revenue_type="services",
        economics={"collected_cash_sar": 50000},
        verified_collection=True,
        duplicate_or_existing_pipeline=True,
    )
    assert decision.eligible is False
    assert "duplicate_or_existing_pipeline" in decision.reasons


def test_strategic_services_requires_margin_approval():
    decision = calculate_partner_commission(
        motion="strategic_channel",
        revenue_type="services",
        economics={"collected_cash_sar": 200000},
        verified_collection=True,
    )
    assert decision.eligible is False
    assert decision.approval_required is True


def test_government_deal_is_compliance_hold():
    decision = calculate_partner_commission(
        motion="closer_sector_partner",
        revenue_type="services",
        economics={"collected_cash_sar": 300000},
        verified_collection=True,
        government_or_tender=True,
    )
    assert decision.eligible is False
    assert decision.status == "compliance_hold"
    assert decision.approval_required is True


def test_default_multi_partner_split_is_40_20_40():
    assert validate_attribution_split(DEFAULT_SPLIT) == DEFAULT_SPLIT
    amounts = allocate_commission_pool(10000)
    assert amounts == {
        "source": Decimal("4000.00"),
        "qualification": Decimal("2000.00"),
        "close": Decimal("4000.00"),
    }


def test_custom_split_rounding_does_not_require_close_role():
    amounts = allocate_commission_pool(
        Decimal("0.01"),
        {"source": Decimal("0.50"), "qualification": Decimal("0.50")},
    )
    assert set(amounts) == {"source", "qualification"}
    assert sum(amounts.values(), Decimal("0")) == Decimal("0.01")


def test_invalid_or_empty_split_rejected():
    with pytest.raises(ValueError):
        validate_attribution_split({"source": 0.5, "qualification": 0.5, "close": 0.5})
    with pytest.raises(ValueError):
        validate_attribution_split({})


def test_negative_commission_pool_rejected():
    with pytest.raises(ValueError):
        allocate_commission_pool(-1)


def test_attribution_window_defaults_to_120_and_caps_extension_at_180():
    assert attribution_window_days() == ATTRIBUTION_PROTECTION_DAYS == 120
    assert attribution_window_days(extension_approved=True) == ATTRIBUTION_MAX_EXTENSION_DAYS == 180


def test_compliance_hold_covers_influence_consent_and_cold_whatsapp():
    hold, reasons = requires_compliance_hold(
        government_or_tender=True,
        government_official_or_employee=True,
        influence_based_compensation=True,
        cold_whatsapp=True,
        consent_proven=False,
    )
    assert hold is True
    assert "government_or_tender_review" in reasons
    assert "government_official_or_employee" in reasons
    assert "influence_based_compensation_prohibited" in reasons
    assert "cold_whatsapp_prohibited" in reasons
    assert "marketing_consent_not_proven" in reasons


def test_clear_non_government_opt_in_partner_motion_is_not_compliance_hold():
    hold, reasons = requires_compliance_hold(consent_proven=True)
    assert hold is False
    assert reasons == ()
