from __future__ import annotations

import pytest

from dealix.commercial.proof_builder import (
    REFERENCE_ONLY,
    UNKNOWN,
    ProofBuildRequest,
    ProofBuilder,
    ProofEvent,
)


def _event(index: int, *, synthetic: bool = False) -> ProofEvent:
    return ProofEvent(
        event_type=f"delivery-{index}",
        description_ar="تم تنفيذ خطوة موثقة",
        description_en="A documented step was completed",
        metric_before="10",
        metric_after="11",
        delta_pct=10,
        source_ref=f"evidence://delivery/{index}",
        recorded_at="2026-08-29T08:00:00Z",
        synthetic=synthetic,
    )


def test_raw_delivery_and_payment_refs_are_reference_only() -> None:
    request = ProofBuildRequest(
        account_id="acct-1",
        company_name="Acme",
        approved_by_founder=True,
        delivery_evidence_refs=["anything-called-delivery"],
        payment_evidence_refs=["anything-called-payment"],
        events=[_event(index) for index in range(3)],
    )
    pack = ProofBuilder().build(request)

    assert pack.proof_level == "L1"
    assert pack.delivery_evidence_state == REFERENCE_ONLY
    assert pack.payment_evidence_state == REFERENCE_ONLY
    assert pack.verified_result_state == "RECORDED_MEASUREMENT_NOT_CUSTOMER_VALIDATED"
    assert pack.customer_value_claim is False
    assert "Payment reference state: REFERENCE_PRESENT_NOT_VERIFIED" in pack.markdown_ar_en


def test_customer_validation_does_not_turn_raw_delivery_ref_into_verified_delivery() -> None:
    events = [
        _event(0).model_copy(
            update={
                "customer_validated": True,
                "customer_validation_ref": "customer://validation/1",
            }
        ),
        _event(1),
        _event(2),
    ]
    pack = ProofBuilder().build(
        ProofBuildRequest(
            account_id="acct-1",
            company_name="Acme",
            approved_by_founder=True,
            delivery_evidence_refs=["delivery://raw-ref"],
            events=events,
        )
    )

    assert pack.delivery_evidence_state == REFERENCE_ONLY
    assert pack.payment_evidence_state == UNKNOWN
    assert pack.verified_result_state == "RECORDED_MEASUREMENT_CUSTOMER_VALIDATED_DELIVERY_UNVERIFIED"
    assert pack.customer_value_claim is False


def test_synthetic_events_and_incomplete_measurements_do_not_raise_proof() -> None:
    synthetic = ProofBuilder().build(
        ProofBuildRequest(
            account_id="acct-1",
            company_name="Acme",
            approved_by_founder=True,
            events=[_event(index, synthetic=True) for index in range(3)],
        )
    )
    assert synthetic.proof_level == "L0"
    assert synthetic.evidence_refs == []

    with pytest.raises(ValueError, match="NO_FAKE_PROOF"):
        ProofBuilder().build(
            ProofBuildRequest(
                account_id="acct-1",
                company_name="Acme",
                events=[
                    ProofEvent(
                        event_type="delivery",
                        description_ar="حدث",
                        description_en="Event",
                        delta_pct=10,
                    )
                ],
            )
        )


def test_semantic_output_is_stable_and_missing_refs_stay_unknown() -> None:
    request = ProofBuildRequest(
        account_id="acct-1",
        company_name="Acme",
        events=[_event(1)],
    )
    first = ProofBuilder().build(request)
    second = ProofBuilder().build(request)
    assert first.semantic_dict() == second.semantic_dict()
    assert first.delivery_evidence_state == UNKNOWN
    assert first.payment_evidence_state == UNKNOWN
