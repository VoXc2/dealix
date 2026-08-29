#!/usr/bin/env python3
"""Fail-closed verifier for Proof Builder reference-only evidence semantics."""

from __future__ import annotations

from dealix.commercial.proof_builder import (
    REFERENCE_ONLY,
    ProofBuildRequest,
    ProofBuilder,
    ProofEvent,
)


def main() -> int:
    event = ProofEvent(
        event_type="delivery",
        description_ar="خطوة موثقة",
        description_en="Documented step",
        metric_before="10",
        metric_after="11",
        delta_pct=10,
        source_ref="evidence://delivery/source",
        recorded_at="2026-08-29T08:00:00Z",
    )
    request = ProofBuildRequest(
        account_id="verification-account",
        company_name="Verification Account",
        approved_by_founder=True,
        delivery_evidence_refs=["raw-delivery-ref"],
        payment_evidence_refs=["raw-payment-ref"],
        events=[
            event,
            event.model_copy(update={"event_type": "delivery-2"}),
            event.model_copy(update={"event_type": "delivery-3"}),
        ],
    )
    pack = ProofBuilder().build(request)

    assert pack.proof_level == "L1"
    assert pack.delivery_evidence_state == REFERENCE_ONLY
    assert pack.payment_evidence_state == REFERENCE_ONLY
    assert pack.customer_value_claim is False
    assert pack.verified_result_state == "RECORDED_MEASUREMENT_NOT_CUSTOMER_VALIDATED"
    assert ProofBuilder().build(request).semantic_dict() == pack.semantic_dict()
    print("PASS: Proof Builder raw refs remain reference-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
