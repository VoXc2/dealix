from __future__ import annotations

import pytest

from dealix.commercial.proof_builder import (
    CUSTOMER_VALIDATED_WITH_DELIVERY_REF,
    EVIDENCE_REF_PRESENT,
    PARTIALLY_VALIDATED,
    PUBLIC_REUSE_REQUIRES_PERMISSION,
    RECORDED_NOT_VALIDATED,
    ProofBuildRequest,
    ProofBuilder,
    ProofEvent,
)


def _event(
    index: int,
    *,
    source_ref: str = "delivery:source",
    recorded_at: str = "2026-08-29T08:00:00Z",
    synthetic: bool = False,
    customer_validated: bool = False,
    customer_validation_ref: str = "",
) -> ProofEvent:
    return ProofEvent(
        event_type=f"delivery-{index}",
        description_ar="تم تنفيذ خطوة موثقة",
        description_en="A documented step was completed",
        metric_before="10",
        metric_after="11",
        delta_pct=10,
        source_ref=source_ref,
        recorded_at=recorded_at,
        synthetic=synthetic,
        customer_validated=customer_validated,
        customer_validation_ref=customer_validation_ref,
    )


def test_three_events_without_founder_approval_stay_l0() -> None:
    pack = ProofBuilder().build(
        ProofBuildRequest(
            account_id="acct-1",
            company_name="Acme",
            events=[_event(index) for index in range(3)],
        )
    )
    assert pack.proof_level == "L0"
    assert pack.customer_value_claim is False
    assert pack.verified_result_state == RECORDED_NOT_VALIDATED


def test_source_and_valid_timestamp_are_required_for_proof_level() -> None:
    for source_ref, recorded_at in (("", "2026-08-29T08:00:00Z"), ("delivery:source", ""), ("delivery:source", "not-a-time"), ("delivery:source", "2026-08-29T08:00:00")):
        pack = ProofBuilder().build(
            ProofBuildRequest(
                account_id="acct-1",
                company_name="Acme",
                approved_by_founder=True,
                events=[
                    _event(index, source_ref=source_ref, recorded_at=recorded_at)
                    for index in range(3)
                ],
            )
        )
        assert pack.proof_level == "L0"
        assert pack.is_fake_proof_gate_passed is False


def test_reference_presence_never_becomes_payment_or_delivery_verification() -> None:
    request = ProofBuildRequest(
        account_id="acct-1",
        company_name="Acme",
        pilot_id="pilot-1",
        approved_by_founder=True,
        delivery_evidence_refs=["delivery:proof-1"],
        payment_evidence_refs=["payment:proof-1"],
        events=[_event(index) for index in range(3)],
    )
    first = ProofBuilder().build(request)
    second = ProofBuilder().build(request)

    assert first.proof_level == "L1"
    assert first.delivery_evidence_state == EVIDENCE_REF_PRESENT
    assert first.payment_evidence_state == EVIDENCE_REF_PRESENT
    assert first.customer_value_claim is False
    assert first.verified_result_state == RECORDED_NOT_VALIDATED
    assert first.public_reuse_authorized is False
    assert first.public_reuse_state == PUBLIC_REUSE_REQUIRES_PERMISSION
    assert first.semantic_dict() == second.semantic_dict()


def test_customer_validation_is_bounded_and_does_not_create_customer_value() -> None:
    pack = ProofBuilder().build(
        ProofBuildRequest(
            account_id="acct-1",
            company_name="Acme",
            approved_by_founder=True,
            delivery_evidence_refs=["delivery:proof-1"],
            events=[
                _event(
                    index,
                    customer_validated=True,
                    customer_validation_ref=f"customer:validation:{index}",
                )
                for index in range(3)
            ],
        )
    )
    assert pack.proof_level == "L1"
    assert pack.verified_result_state == CUSTOMER_VALIDATED_WITH_DELIVERY_REF
    assert pack.customer_value_claim is False
    assert pack.public_reuse_authorized is False


def test_partial_customer_validation_is_explicit() -> None:
    events = [_event(index) for index in range(3)]
    events[0] = _event(
        0,
        customer_validated=True,
        customer_validation_ref="customer:validation:0",
    )
    pack = ProofBuilder().build(
        ProofBuildRequest(
            account_id="acct-1",
            company_name="Acme",
            approved_by_founder=True,
            delivery_evidence_refs=["delivery:proof-1"],
            events=events,
        )
    )
    assert pack.verified_result_state == PARTIALLY_VALIDATED
    assert pack.customer_value_claim is False


def test_synthetic_events_do_not_raise_proof_level() -> None:
    pack = ProofBuilder().build(
        ProofBuildRequest(
            account_id="acct-1",
            company_name="Acme",
            approved_by_founder=True,
            events=[_event(index, synthetic=True) for index in range(3)],
        )
    )
    assert pack.proof_level == "L0"
    assert pack.evidence_refs == []
    assert pack.is_fake_proof_gate_passed is False


def test_delta_without_metric_after_is_rejected() -> None:
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
