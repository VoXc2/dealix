"""Economic truth authority — negative regression tests.

Proves invalid truth transitions fail closed:
  payment authority != revenue authority
  CUSTOMER_CONFIRMED alone != payment
  generic VERIFIED without domain/provenance != payment/revenue
  ESTIMATED/INFERRED/HYPOTHESIS/SYNTHETIC/TEST_ONLY cannot pollute real metrics
  generated plans cannot become real pipeline via aggregation
"""

from __future__ import annotations

import pytest

from dealix.commercial.financial_os import (
    FinancialOS,
    FinancialRecord,
    FinancialState,
    MetricProvenance,
)
from dealix.commercial.truth_types import (
    AUTHORITY_MATRIX,
    AUTHORITY_MATRIX_V2,
    EconomicTruth,
    EvidenceDomain,
    TruthClass,
    can_use_for,
    can_use_for_v2,
    ensure_real_value,
    ensure_verified_payment,
    ensure_verified_revenue,
)


def _truth(**overrides) -> EconomicTruth:
    base = {
        "value": 1000.0,
        "truth_class": TruthClass.VERIFIED,
        "source": "test",
        "verified_at": "2026-09-11T00:00:00Z",
        "evidence_ref": "ev-1",
    }
    base.update(overrides)
    return EconomicTruth(**base)


def test_customer_confirmed_alone_cannot_authorize_payment_or_revenue() -> None:
    truth = _truth(
        truth_class=TruthClass.CUSTOMER_CONFIRMED,
        evidence_domain=EvidenceDomain.CUSTOMER_ACCEPTANCE,
        business_state="CUSTOMER_ACCEPTED",
    )
    assert "payment" not in AUTHORITY_MATRIX[TruthClass.CUSTOMER_CONFIRMED]
    assert "revenue" not in AUTHORITY_MATRIX[TruthClass.CUSTOMER_CONFIRMED]
    assert not can_use_for_v2(TruthClass.CUSTOMER_CONFIRMED, "payment", truth.evidence_domain, truth.business_state)
    with pytest.raises(ValueError):
        ensure_verified_payment(truth)
    with pytest.raises(ValueError):
        ensure_verified_revenue(truth)


def test_generic_verified_without_domain_cannot_authorize_payment_or_revenue() -> None:
    truth = _truth()
    assert can_use_for(TruthClass.VERIFIED, "payment") is False
    assert can_use_for(TruthClass.VERIFIED, "revenue") is False
    assert not can_use_for_v2(TruthClass.VERIFIED, "payment", None, None)
    assert not can_use_for_v2(TruthClass.VERIFIED, "revenue", None, None)
    with pytest.raises(ValueError):
        ensure_verified_payment(truth)
    with pytest.raises(ValueError):
        ensure_verified_revenue(truth)


def test_payment_domain_with_wrong_business_state_is_denied() -> None:
    truth = _truth(evidence_domain=EvidenceDomain.PAYMENT, business_state="PROPOSAL_SENT")
    assert not can_use_for_v2(TruthClass.VERIFIED, "payment", truth.evidence_domain, truth.business_state)
    with pytest.raises(ValueError):
        ensure_verified_payment(truth)


def test_valid_payment_requires_domain_state_and_provenance() -> None:
    valid = _truth(evidence_domain=EvidenceDomain.PAYMENT, business_state="PAYMENT_VERIFIED")
    assert ensure_verified_payment(valid) == 1000.0

    no_provenance = _truth(
        evidence_domain=EvidenceDomain.PAYMENT,
        business_state="PAYMENT_VERIFIED",
        verified_at="",
        evidence_ref="",
    )
    with pytest.raises(ValueError):
        ensure_verified_payment(no_provenance)


def test_payment_domain_does_not_become_revenue() -> None:
    truth = _truth(evidence_domain=EvidenceDomain.PAYMENT, business_state="PAYMENT_VERIFIED")
    assert not can_use_for_v2(TruthClass.VERIFIED, "revenue", truth.evidence_domain, truth.business_state)
    with pytest.raises(ValueError):
        ensure_verified_revenue(truth)


def test_revenue_requires_accounting_or_invoice_and_recognized_state() -> None:
    valid = _truth(evidence_domain=EvidenceDomain.ACCOUNTING, business_state="REVENUE_RECOGNIZED")
    assert ensure_verified_revenue(valid) == 1000.0

    wrong_state = _truth(evidence_domain=EvidenceDomain.ACCOUNTING, business_state="PAYMENT_VERIFIED")
    with pytest.raises(ValueError):
        ensure_verified_revenue(wrong_state)

    wrong_domain = _truth(evidence_domain=EvidenceDomain.PAYMENT, business_state="REVENUE_RECOGNIZED")
    with pytest.raises(ValueError):
        ensure_verified_revenue(wrong_domain)


@pytest.mark.parametrize(
    "truth_class",
    [
        TruthClass.ESTIMATED,
        TruthClass.INFERRED,
        TruthClass.HYPOTHESIS,
        TruthClass.SYNTHETIC,
        TruthClass.SIMULATED,
        TruthClass.TEST_ONLY,
        TruthClass.UNKNOWN,
        TruthClass.OBSERVED,
    ],
)
def test_non_evidenced_classes_cannot_pollute_real_pipeline(truth_class: TruthClass) -> None:
    truth = EconomicTruth(value=9999.0, truth_class=truth_class, source="planner", evidence_ref="plan-1")
    assert can_use_for(truth_class, "pipeline") is False
    assert not can_use_for_v2(truth_class, "pipeline", EvidenceDomain.PROBLEM, "DISCOVERY")
    with pytest.raises(ValueError):
        ensure_real_value(truth)


def test_generated_plan_aggregation_cannot_become_real_pipeline() -> None:
    plans = [
        EconomicTruth(value=5000.0, truth_class=TruthClass.HYPOTHESIS, source="execute_20_plans", evidence_ref=f"plan-{i}")
        for i in range(20)
    ]
    total = 0.0
    for plan in plans:
        with pytest.raises(ValueError):
            total += ensure_real_value(plan)
    assert total == 0.0


def test_verified_pipeline_requires_domain_and_state() -> None:
    valid = _truth(
        evidence_domain=EvidenceDomain.DIAGNOSTIC,
        business_state="DIAGNOSTIC",
        value=7500.0,
    )
    assert ensure_real_value(valid) == 7500.0
    generic = _truth(value=7500.0)
    with pytest.raises(ValueError):
        ensure_real_value(generic)


def test_financial_os_classified_totals_never_mix_categories() -> None:
    fos = FinancialOS()
    fos.add_record(FinancialRecord(record_id="opp1", state=FinancialState.OPPORTUNITY_VALUE, amount_sar=100000, probability=0.5, evidence_ref="opp-ref-1"))
    fos.add_record(FinancialRecord(record_id="q1", state=FinancialState.QUOTE_VALUE, amount_sar=20000, probability=0.4, evidence_ref="quote-ref-1"))
    fos.add_record(FinancialRecord(record_id="p1", state=FinancialState.PAYMENT_VERIFIED, amount_sar=5000, probability=1.0, verified_at="2026-09-11T00:00:00Z", evidence_ref="bank-ref-1"))
    totals = fos.classified_totals()
    assert totals["estimated_pipeline"] == 50000.0
    assert totals["real_pipeline"] == 20000.0
    assert totals["verified_payment"] == 5000.0
    assert totals["recognized_revenue"] == 0.0


def test_payment_verified_requires_verified_at_and_evidence_ref() -> None:
    fos = FinancialOS()
    with pytest.raises(ValueError):
        fos.add_record(FinancialRecord(
            record_id="p2",
            state=FinancialState.PAYMENT_VERIFIED,
            amount_sar=100,
            evidence_ref="bank-ref-2",
        ))
    with pytest.raises(ValueError):
        fos.add_record(FinancialRecord(
            record_id="p3",
            state=FinancialState.PAYMENT_VERIFIED,
            amount_sar=100,
            verified_at="2026-09-11T00:00:00Z",
        ))


def test_revenue_recognized_requires_provenance() -> None:
    fos = FinancialOS()
    with pytest.raises(ValueError):
        fos.add_record(FinancialRecord(record_id="r1", state=FinancialState.REVENUE_RECOGNIZED, amount_sar=100))
    with pytest.raises(ValueError):
        fos.add_record(FinancialRecord(record_id="r2", state=FinancialState.REVENUE_RECOGNIZED, amount_sar=100, verified_at="2026-09-11T00:00:00Z"))


def test_payment_received_unverified_cannot_carry_verified_at() -> None:
    fos = FinancialOS()
    with pytest.raises(ValueError):
        fos.add_record(FinancialRecord(record_id="u1", state=FinancialState.PAYMENT_RECEIVED_UNVERIFIED, amount_sar=100, verified_at="2026-09-11T00:00:00Z"))


def test_financial_os_authority_delegates_to_canonical_truth_functions() -> None:
    fos = FinancialOS()
    payment = _truth(evidence_domain=EvidenceDomain.PAYMENT, business_state="PAYMENT_VERIFIED")
    assert fos.verify_payment_authority(payment) == 1000.0
    with pytest.raises(ValueError):
        fos.verify_revenue_authority(payment)

    revenue = _truth(evidence_domain=EvidenceDomain.INVOICE, business_state="REVENUE_RECOGNIZED")
    assert fos.verify_revenue_authority(revenue) == 1000.0
    with pytest.raises(ValueError):
        fos.verify_payment_authority(revenue)


def test_daily_benefit_simulation_is_not_real_value() -> None:
    from dealix.commercial.daily_benefit_maximizer import DailyBenefitMaximizer

    truth = DailyBenefitMaximizer().maximize().benefit_truth()
    assert truth.truth_class == TruthClass.SIMULATED
    assert truth.is_synthetic() is True
    with pytest.raises(ValueError):
        ensure_real_value(truth)


def test_money_now_expected_value_is_estimated_not_real() -> None:
    from dealix.commercial.realistic_money_now import RealisticMoneyNowCandidate

    candidate = RealisticMoneyNowCandidate(
        candidate_id="c1",
        relationship_id="r1",
        entity="Entity",
        buyer="CEO",
        problem="revenue leakage",
    )
    assert candidate.value_truth_class == TruthClass.ESTIMATED
    truth = candidate.expected_value_truth()
    assert truth.is_synthetic() is False
    with pytest.raises(ValueError):
        ensure_real_value(truth)


def test_authority_matrices_are_fail_closed_for_unknown_classes() -> None:
    assert AUTHORITY_MATRIX[TruthClass.UNKNOWN] == set()
    assert AUTHORITY_MATRIX[TruthClass.SYNTHETIC] == set()
    assert AUTHORITY_MATRIX_V2[(TruthClass.VERIFIED, "payment")] == {EvidenceDomain.PAYMENT}
    assert AUTHORITY_MATRIX_V2[(TruthClass.VERIFIED, "revenue")] == {EvidenceDomain.ACCOUNTING, EvidenceDomain.INVOICE}
    assert not can_use_for_v2(TruthClass.SYNTHETIC, "public_claim", EvidenceDomain.PUBLIC_CLAIM, "APPROVED")


# ─── FinancialOS Truth Model Regression Tests ─────────────────────────────

def test_empty_financial_os_creates_no_fake_numbers() -> None:
    """Empty FinancialOS must not fabricate any financial numbers."""
    fos = FinancialOS()
    view = fos.command_view()

    # No loaded evidence means unknown, never fabricated zero.
    assert view.cash_verified_sar is None
    assert view.cash_expected_sar is None
    assert view.accounts_receivable_sar is None
    assert view.quotes_outstanding_sar is None
    assert view.expected_7d_sar is None
    assert view.expected_30d_sar is None
    assert view.pipeline_weighted_sar is None
    assert view.delivery_liability_sar is None
    assert view.monthly_infra_cost_sar is None
    assert view.variable_model_cost_sar is None
    assert view.gross_margin_pct is None

    # All provenance should be NOT_PROVEN
    assert view.cash_verified_provenance == "NOT_PROVEN"
    assert view.cash_expected_provenance == "NOT_PROVEN"
    assert view.accounts_receivable_provenance == "NOT_PROVEN"
    assert view.quotes_outstanding_provenance == "NOT_PROVEN"
    assert view.expected_7d_provenance == "NOT_PROVEN"
    assert view.expected_30d_provenance == "NOT_PROVEN"
    assert view.pipeline_weighted_provenance == "NOT_PROVEN"
    assert view.delivery_liability_provenance == "NOT_PROVEN"
    assert view.monthly_infra_cost_provenance == "NOT_PROVEN"
    assert view.variable_model_cost_provenance == "NOT_PROVEN"
    assert view.gross_margin_provenance == "NOT_PROVEN"

    # Unknowns should list the lack of evidence
    assert "no financial records loaded" in view.financial_unknowns
    assert "no verified cash evidence (PAYMENT_VERIFIED + evidence_ref)" in view.financial_unknowns
    assert "no recognized revenue evidence (REVENUE_RECOGNIZED)" in view.financial_unknowns
    assert "pipeline weighted value is NOT_PROVEN" in view.financial_unknowns


def test_quote_invoice_never_become_verified_cash() -> None:
    """QUOTE_VALUE and INVOICE_VALUE states must never be counted as verified cash."""
    fos = FinancialOS()

    # Add quote
    fos.add_record(FinancialRecord(
        record_id="q1",
        state=FinancialState.QUOTE_VALUE,
        amount_sar=50000,
        probability=0.8,
        evidence_ref="quote-ref-50000",
    ))

    # Add invoice
    fos.add_record(FinancialRecord(
        record_id="inv1",
        state=FinancialState.INVOICE_VALUE,
        amount_sar=30000,
        probability=1.0,
        evidence_ref="invoice-ref-30000",
    ))

    # Add payment pending
    fos.add_record(FinancialRecord(
        record_id="pp1",
        state=FinancialState.PAYMENT_PENDING,
        amount_sar=20000,
        probability=1.0,
        evidence_ref="pending-ref-20000",
    ))

    view = fos.command_view()

    # Quote/invoice/pending evidence never proves that verified cash is zero.
    assert view.cash_verified_sar is None
    assert view.cash_verified_provenance == "NOT_PROVEN"

    # These are tracked separately but NOT as verified cash.
    assert view.quotes_outstanding_sar == 50000.0
    assert view.accounts_receivable_sar == 50000.0  # invoice + payment_pending

    # Pipeline weighted includes quote (probability adjusted)
    assert view.pipeline_weighted_sar == 40000.0  # 50000 * 0.8
    assert view.pipeline_weighted_provenance == "DERIVED_ESTIMATE"


def test_payment_verified_is_only_source_of_verified_cash() -> None:
    """Only PAYMENT_VERIFIED records contribute to verified cash."""
    fos = FinancialOS()

    # Add various records
    fos.add_record(FinancialRecord(
        record_id="q1",
        state=FinancialState.QUOTE_VALUE,
        amount_sar=10000,
        evidence_ref="quote-ref-10000",
    ))
    fos.add_record(FinancialRecord(
        record_id="inv1",
        state=FinancialState.INVOICE_VALUE,
        amount_sar=10000,
        evidence_ref="invoice-ref-10000",
    ))
    fos.add_record(FinancialRecord(
        record_id="p1",
        state=FinancialState.PAYMENT_VERIFIED,
        amount_sar=10000,
        verified_at="2026-09-11T00:00:00Z",
        evidence_ref="bank-ref-1",
    ))

    view = fos.command_view()

    # Only PAYMENT_VERIFIED counts as verified cash
    assert view.cash_verified_sar == 10000.0
    assert view.cash_verified_provenance == "VERIFIED"

    # Other states are separate
    assert view.quotes_outstanding_sar == 10000.0
    assert view.accounts_receivable_sar == 10000.0


def test_payment_verified_does_not_equal_revenue_recognized() -> None:
    """PAYMENT_VERIFIED and REVENUE_RECOGNIZED are distinct; payment != revenue."""
    fos = FinancialOS()

    # Add verified payment
    fos.add_record(FinancialRecord(
        record_id="pay1",
        state=FinancialState.PAYMENT_VERIFIED,
        amount_sar=50000,
        verified_at="2026-09-11T00:00:00Z",
        evidence_ref="bank-ref-1",
    ))

    # Add recognized revenue (separate record, separate state)
    fos.add_record(FinancialRecord(
        record_id="rev1",
        state=FinancialState.REVENUE_RECOGNIZED,
        amount_sar=30000,
        verified_at="2026-09-12T00:00:00Z",
        evidence_ref="accounting-ref-1",
    ))

    view = fos.command_view()
    totals = fos.classified_totals()

    # Verified cash is from PAYMENT_VERIFIED only
    assert view.cash_verified_sar == 50000.0

    # Recognized revenue is separate
    assert totals["recognized_revenue"] == 30000.0
    assert totals["verified_payment"] == 50000.0
    assert totals["verified_payment"] != totals["recognized_revenue"]


def test_explicit_evidence_backed_values_remain_usable() -> None:
    """Evidence-backed PAYMENT_VERIFIED and REVENUE_RECOGNIZED values must remain usable."""
    fos = FinancialOS()

    fos.add_record(FinancialRecord(
        record_id="pay1",
        state=FinancialState.PAYMENT_VERIFIED,
        amount_sar=75000,
        verified_at="2026-09-11T00:00:00Z",
        evidence_ref="bank-transfer-ref-001",
    ))
    fos.add_record(FinancialRecord(
        record_id="rev1",
        state=FinancialState.REVENUE_RECOGNIZED,
        amount_sar=60000,
        verified_at="2026-09-12T00:00:00Z",
        evidence_ref="rev-rec-001",
    ))

    view = fos.command_view()
    totals = fos.classified_totals()

    # Verified cash is usable
    assert view.cash_verified_sar == 75000.0
    assert view.cash_verified_provenance == "VERIFIED"

    # Recognized revenue is usable
    assert totals["recognized_revenue"] == 60000.0

    # Receivables from evidence-backed invoices
    fos.add_record(FinancialRecord(
        record_id="inv1",
        state=FinancialState.INVOICE_VALUE,
        amount_sar=25000,
        evidence_ref="inv-001",
    ))
    view2 = fos.command_view()
    assert view2.accounts_receivable_sar == 25000.0
    assert view2.accounts_receivable_provenance == "VERIFIED"


def test_delivery_liability_infra_model_cost_margin_are_not_proven() -> None:
    """Delivery liability, infra cost, model cost, margin must be NOT_PROVEN without evidence."""
    fos = FinancialOS()

    # Add some verified payment
    fos.add_record(FinancialRecord(
        record_id="pay1",
        state=FinancialState.PAYMENT_VERIFIED,
        amount_sar=100000,
        verified_at="2026-09-11T00:00:00Z",
        evidence_ref="bank-ref-1",
    ))

    view = fos.command_view()

    # These fields must remain NOT_PROVEN (None value, NOT_PROVEN provenance).
    assert view.delivery_liability_sar is None
    assert view.delivery_liability_provenance == "NOT_PROVEN"

    assert view.monthly_infra_cost_sar is None
    assert view.monthly_infra_cost_provenance == "NOT_PROVEN"

    assert view.variable_model_cost_sar is None
    assert view.variable_model_cost_provenance == "NOT_PROVEN"

    assert view.gross_margin_pct is None
    assert view.gross_margin_provenance == "NOT_PROVEN"


def test_unit_economics_is_explicit_estimate() -> None:
    """unit_economics() must be explicitly marked as DERIVED_ESTIMATE."""
    fos = FinancialOS()

    econ = fos.unit_economics(
        offer_id="offer-1",
        delivery_hours=10.0,
        eng_hours=5.0,
        founder_mins=30,
        model_cost=100.0,
        hosting=50.0,
        third_party=25.0,
        target_margin=0.4,
    )

    # All cost and price provenance must be DERIVED_ESTIMATE
    assert econ.cost_provenance == "DERIVED_ESTIMATE"
    assert econ.price_provenance == "DERIVED_ESTIMATE"

    # Price range and assumptions must expose estimate status.
    assert "DERIVED_ESTIMATE" in econ.price_range_internal
    assert "not verified" in econ.price_range_internal.lower()
    assert any("delivery_hourly_rate_sar=" in item for item in econ.assumptions)
    assert any("engineering_hourly_rate_sar=" in item for item in econ.assumptions)
    assert econ.timeframe_days is None


def test_evidence_less_records_do_not_mint_verified_financial_metrics() -> None:
    fos = FinancialOS()
    fos.add_record(FinancialRecord(
        record_id="quote-no-proof",
        state=FinancialState.QUOTE_VALUE,
        amount_sar=25000,
        probability=0.5,
    ))
    fos.add_record(FinancialRecord(
        record_id="invoice-no-proof",
        state=FinancialState.INVOICE_VALUE,
        amount_sar=10000,
    ))
    view = fos.command_view()
    assert view.cash_verified_sar is None
    assert view.accounts_receivable_sar is None
    assert view.quotes_outstanding_sar is None
    assert view.pipeline_weighted_sar is None
    assert view.cash_verified_provenance == "NOT_PROVEN"
    assert view.accounts_receivable_provenance == "NOT_PROVEN"
    assert view.quotes_outstanding_provenance == "NOT_PROVEN"
    assert view.pipeline_weighted_provenance == "NOT_PROVEN"


def test_zero_known_vs_unknown_distinguished() -> None:
    """Zero-known (explicit 0 from evidence) vs unknown (no evidence) must be distinguishable."""
    fos = FinancialOS()

    # Empty ledger: unknown is represented as None, not synthetic zero.
    view_empty = fos.command_view()
    assert view_empty.cash_verified_sar is None
    assert view_empty.cash_verified_provenance == "NOT_PROVEN"
    assert view_empty.accounts_receivable_sar is None
    assert view_empty.accounts_receivable_provenance == "NOT_PROVEN"

    # Add explicit zero-amount verified payment (weird but possible)
    fos.add_record(FinancialRecord(
        record_id="pay-zero",
        state=FinancialState.PAYMENT_VERIFIED,
        amount_sar=0.0,
        verified_at="2026-09-11T00:00:00Z",
        evidence_ref="bank-ref-zero",
    ))

    view_zero = fos.command_view()
    # Even with 0 amount, provenance is VERIFIED because evidence exists
    assert view_zero.cash_verified_sar == 0.0
    assert view_zero.cash_verified_provenance == "VERIFIED"

    # Add explicit zero-amount invoice
    fos.add_record(FinancialRecord(
        record_id="inv-zero",
        state=FinancialState.INVOICE_VALUE,
        amount_sar=0.0,
        evidence_ref="inv-ref-zero",
    ))

    view_zero2 = fos.command_view()
    assert view_zero2.accounts_receivable_sar == 0.0
    assert view_zero2.accounts_receivable_provenance == "VERIFIED"
