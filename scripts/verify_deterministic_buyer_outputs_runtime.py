#!/usr/bin/env python3
"""Runtime verification for the deterministic buyer outputs engine."""

from __future__ import annotations

from dealix.commercial.buyer_outputs import (
    BuyerEvidenceSnapshot,
    BuyerOutputsEngine,
    EvidenceItem,
    PaymentEvidence,
)


def main() -> int:
    snapshot = BuyerEvidenceSnapshot(
        tenant_or_account_id="verification-account",
        company_name="Verification Account",
        source_sha="verification-source-sha",
        as_of="2026-08-29T08:00:00+00:00",
        evidence=[
            EvidenceItem(
                evidence_id="E-1",
                source_ref="verification-source-1",
                observed_at="2026-08-29T07:00:00+00:00",
            )
        ],
        payment_evidence=PaymentEvidence(invoice_refs=["E-1"]),
    )
    engine = BuyerOutputsEngine()
    first = engine.build(snapshot)
    second = engine.build(snapshot)

    assert first.semantic_dict() == second.semantic_dict()
    assert set(first.to_dict()) == {
        "revenue_leak_map",
        "customer_proof_decision_pack",
        "executive_command",
    }
    assert "UNKNOWN_NOT_EVIDENCE_BACKED" in first.customer_proof_decision_pack["decision_options"]
    assert first.executive_command["money"]["verified_payment_state"] == "UNKNOWN_NOT_EVIDENCE_BACKED"
    assert first.customer_proof_decision_pack["payment_evidence_state"]["status"] == (
        "UNKNOWN_NOT_EVIDENCE_BACKED"
    )
    assert len(first.revenue_leak_map["top_interventions"]) <= 3
    print("PASS: deterministic buyer outputs runtime")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
