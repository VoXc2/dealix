from __future__ import annotations

import pytest

from dealix.commercial.buyer_outputs import (
    BuyerEvidenceSnapshot,
    BuyerOutputsEngine,
    EvidenceItem,
    ObservedLeak,
    PaymentEvidence,
)


def _empty_snapshot() -> BuyerEvidenceSnapshot:
    return BuyerEvidenceSnapshot(
        tenant_or_account_id="acct-1",
        company_name="Acme",
        source_sha="source-sha-1",
        as_of="2026-08-29T08:00:00+00:00",
    )


def test_outputs_are_deterministic_except_generated_at() -> None:
    engine = BuyerOutputsEngine()
    first = engine.build(_empty_snapshot())
    second = engine.build(_empty_snapshot())

    assert first.semantic_dict() == second.semantic_dict()
    assert len(first.revenue_leak_map["top_interventions"]) <= 3
    assert first.revenue_leak_map["metadata"]["unknown_semantics"] == "UNKNOWN_NOT_EVIDENCE_BACKED"
    assert "UNKNOWN_NOT_EVIDENCE_BACKED" in first.customer_proof_decision_pack["decision_options"]
    assert first.executive_command["money"]["verified_revenue"] == "UNKNOWN_NOT_EVIDENCE_BACKED"
    assert first.executive_command["money"]["verified_payment_state"] == "UNKNOWN_NOT_EVIDENCE_BACKED"


def test_verified_payment_and_delivery_are_evidence_bound() -> None:
    snapshot = BuyerEvidenceSnapshot(
        tenant_or_account_id="acct-1",
        company_name="Acme",
        source_sha="source-sha-1",
        as_of="2026-08-29T08:00:00+00:00",
        stale_after="2026-09-05T00:00:00+00:00",
        evidence=[
            EvidenceItem(
                evidence_id="E-CALL",
                source_ref="meeting-notes-1",
                observed_at="2026-08-28T08:00:00+00:00",
                summary="Customer described the current workflow.",
                customer_validated=True,
            ),
            EvidenceItem(
                evidence_id="E-PAYMENT",
                source_ref="payment-provider-event-1",
                observed_at="2026-08-29T07:00:00+00:00",
            ),
            EvidenceItem(
                evidence_id="E-DELIVERY",
                source_ref="delivery-log-1",
                observed_at="2026-08-29T07:30:00+00:00",
                customer_validated=True,
            ),
        ],
        observed_leaks=[
            ObservedLeak(
                leak_id="LEAK-1",
                description="Follow-up ownership is not recorded.",
                evidence_refs=["E-CALL"],
            )
        ],
        payment_evidence=PaymentEvidence(
            status="VERIFIED",
            payment_proof_refs=["E-PAYMENT"],
            verified_revenue_sar=1500,
            invoice_refs=["E-CALL"],
        ),
        delivery_evidence={
            "status": "VERIFIED",
            "delivery_proof_refs": ["E-DELIVERY"],
        },
        customer_validation_state="CONFIRMED",
    )

    outputs = BuyerOutputsEngine().build(snapshot).to_dict()

    assert outputs["executive_command"]["money"]["verified_revenue"] == 1500.0
    assert outputs["executive_command"]["money"]["verified_payment_state"] == "VERIFIED"
    assert outputs["executive_command"]["money"]["economic_evidence_refs"] == ["E-PAYMENT"]
    assert outputs["customer_proof_decision_pack"]["business_interpretation"]["status"] == "EVIDENCE_BACKED"
    assert outputs["customer_proof_decision_pack"]["delivery_evidence_state"]["status"] == "VERIFIED"
    assert outputs["revenue_leak_map"]["observed_leaks"][0]["evidence_refs"] == ["E-CALL"]
    assert outputs["revenue_leak_map"]["metadata"]["freshness"]["stale"] is False


def test_synthetic_evidence_cannot_be_promoted_to_observed_leak() -> None:
    snapshot = BuyerEvidenceSnapshot(
        tenant_or_account_id="acct-1",
        company_name="Acme",
        source_sha="source-sha-1",
        as_of="2026-08-29T08:00:00+00:00",
        evidence=[
            EvidenceItem(
                evidence_id="SYNTHETIC-1",
                source_ref="rehearsal-1",
                observed_at="2026-08-29T07:00:00+00:00",
                synthetic=True,
            )
        ],
        observed_leaks=[
            ObservedLeak(
                leak_id="LEAK-1",
                description="Synthetic rehearsal signal.",
                evidence_refs=["SYNTHETIC-1"],
            )
        ],
    )

    with pytest.raises(ValueError, match="synthetic evidence"):
        BuyerOutputsEngine().build(snapshot)


def test_invoice_alone_never_becomes_payment() -> None:
    snapshot = BuyerEvidenceSnapshot(
        tenant_or_account_id="acct-1",
        company_name="Acme",
        source_sha="source-sha-1",
        as_of="2026-08-29T08:00:00+00:00",
        evidence=[
            EvidenceItem(
                evidence_id="E-INVOICE",
                source_ref="invoice-1",
                observed_at="2026-08-29T07:00:00+00:00",
            )
        ],
        payment_evidence=PaymentEvidence(
            status="UNKNOWN",
            invoice_refs=["E-INVOICE"],
        ),
    )

    output = BuyerOutputsEngine().build(snapshot).to_dict()
    payment = output["customer_proof_decision_pack"]["payment_evidence_state"]

    assert payment["status"] == "UNKNOWN_NOT_EVIDENCE_BACKED"
    assert payment["verified_revenue_sar"] == "UNKNOWN_NOT_EVIDENCE_BACKED"


def test_reference_order_is_normalized_for_semantic_equality() -> None:
    first_snapshot = BuyerEvidenceSnapshot(
        tenant_or_account_id="acct-1",
        company_name="Acme",
        source_sha="source-sha-1",
        as_of="2026-08-29T08:00:00+00:00",
        evidence=[
            EvidenceItem(
                evidence_id="E-2",
                source_ref="source-2",
                observed_at="2026-08-29T07:00:00+00:00",
            ),
            EvidenceItem(
                evidence_id="E-1",
                source_ref="source-1",
                observed_at="2026-08-29T06:00:00+00:00",
            ),
        ],
    )
    second_snapshot = first_snapshot.model_copy(
        update={"evidence": list(reversed(first_snapshot.evidence))}
    )

    first = BuyerOutputsEngine().build(first_snapshot)
    second = BuyerOutputsEngine().build(second_snapshot)

    assert first.semantic_dict() == second.semantic_dict()
