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
    fos.add_record(FinancialRecord(record_id="opp1", state=FinancialState.OPPORTUNITY_VALUE, amount_sar=100000, probability=0.5))
    fos.add_record(FinancialRecord(record_id="q1", state=FinancialState.QUOTE_VALUE, amount_sar=20000, probability=0.4))
    fos.add_record(FinancialRecord(record_id="p1", state=FinancialState.PAYMENT_VERIFIED, amount_sar=5000, probability=1.0, verified_at="2026-09-11T00:00:00Z"))
    totals = fos.classified_totals()
    assert totals["estimated_pipeline"] == 50000.0
    assert totals["real_pipeline"] == 20000.0
    assert totals["verified_payment"] == 5000.0
    assert totals["recognized_revenue"] == 0.0


def test_payment_verified_requires_verified_at() -> None:
    fos = FinancialOS()
    with pytest.raises(ValueError):
        fos.add_record(FinancialRecord(record_id="p2", state=FinancialState.PAYMENT_VERIFIED, amount_sar=100))


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
