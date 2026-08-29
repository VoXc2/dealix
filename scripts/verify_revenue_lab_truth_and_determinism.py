#!/usr/bin/env python3
"""Fail-closed verifier for Revenue Lab identity and proof truth."""

from __future__ import annotations

from dealix.revenue_lab import CompanySignal, EvidenceReference, OutcomeEvent, run_revenue_lab


def _signal() -> CompanySignal:
    return CompanySignal(
        tenant_id="dealix",
        account_id="verification-account",
        company_name="Verification Account",
        sector="operations",
        company_size="sme",
        department="sales",
        relationship="prospect",
        permission="warm",
        decision_maker_role="Operations director",
        offer_match="Revenue Proof Sprint",
        why_now="A dated source exists.",
        value_exchange="Bounded workflow proof.",
        pain_hypotheses=("A workflow may be slow.",),
        unknowns=("Customer-approved baseline",),
        evidence=(
            EvidenceReference(
                source_ref="verification:source",
                source_type="internal",
                observed_at="2026-07-15T00:00:00Z",
                quality="primary",
            ),
        ),
        strategic_fit=80,
        urgency=70,
    )


def main() -> int:
    outcome = OutcomeEvent(
        account_id="verification-account",
        outcome="value_confirmed",
        source_ref="verification:outcome",
        observed_at="2026-07-15T00:00:00Z",
        customer_validated=True,
        customer_validation_ref="verification:customer-confirmation",
        delivery_proof_ref="verification:delivery-proof",
    )
    first = run_revenue_lab([_signal()], outcomes=[outcome])
    second = run_revenue_lab([_signal()], outcomes=[outcome])

    assert first.run_id == second.run_id
    assert first.summary["verified_customer_outcomes"] == 1
    assert first.summary["external_actions_executed"] == 0
    assert first.summary["production_changes"] == 0
    print("PASS: Revenue Lab truth and determinism")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
