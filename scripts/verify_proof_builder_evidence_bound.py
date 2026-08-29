#!/usr/bin/env python3
"""Fail-closed verifier for the evidence-bound commercial Proof Builder."""

from __future__ import annotations

from dealix.commercial.proof_builder import (
    CUSTOMER_VALIDATED_WITH_DELIVERY_REF,
    EVIDENCE_REF_PRESENT,
    PUBLIC_REUSE_REQUIRES_PERMISSION,
    RECORDED_NOT_VALIDATED,
    ProofBuildRequest,
    ProofBuilder,
    ProofEvent,
)


def _event(
    index: int,
    *,
    recorded_at: str = "2026-08-29T08:00:00Z",
    customer_validated: bool = False,
) -> ProofEvent:
    return ProofEvent(
        event_type=f"delivery-{index}",
        description_ar="خطوة موثقة",
        description_en="Documented step",
        metric_before="10",
        metric_after="11",
        delta_pct=10,
        source_ref="delivery:source",
        recorded_at=recorded_at,
        customer_validated=customer_validated,
        customer_validation_ref=(
            f"customer:validation:{index}" if customer_validated else ""
        ),
    )


def main() -> int:
    request = ProofBuildRequest(
        account_id="verification-account",
        company_name="Verification Account",
        approved_by_founder=True,
        delivery_evidence_refs=["delivery:proof-ref"],
        payment_evidence_refs=["payment:proof-ref"],
        events=[_event(index) for index in range(3)],
    )
    pack = ProofBuilder().build(request)
    assert pack.proof_level == "L1"
    assert pack.customer_value_claim is False
    assert pack.verified_result_state == RECORDED_NOT_VALIDATED
    assert pack.delivery_evidence_state == EVIDENCE_REF_PRESENT
    assert pack.payment_evidence_state == EVIDENCE_REF_PRESENT
    assert pack.public_reuse_authorized is False
    assert pack.public_reuse_state == PUBLIC_REUSE_REQUIRES_PERMISSION
    assert ProofBuilder().build(request).semantic_dict() == pack.semantic_dict()

    invalid_pack = ProofBuilder().build(
        ProofBuildRequest(
            account_id="verification-account",
            company_name="Verification Account",
            approved_by_founder=True,
            events=[_event(index, recorded_at="invalid") for index in range(3)],
        )
    )
    assert invalid_pack.proof_level == "L0"
    assert invalid_pack.is_fake_proof_gate_passed is False

    validated_pack = ProofBuilder().build(
        ProofBuildRequest(
            account_id="verification-account",
            company_name="Verification Account",
            approved_by_founder=True,
            delivery_evidence_refs=["delivery:proof-ref"],
            events=[_event(index, customer_validated=True) for index in range(3)],
        )
    )
    assert validated_pack.verified_result_state == CUSTOMER_VALIDATED_WITH_DELIVERY_REF
    assert validated_pack.customer_value_claim is False
    assert validated_pack.public_reuse_authorized is False

    print("PASS: evidence-bound Proof Builder")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
