from __future__ import annotations

import pytest

from dealix.revenue_lab import CompanySignal, EvidenceReference, OutcomeEvent, run_revenue_lab


def make_signal() -> CompanySignal:
    return CompanySignal(
        tenant_id="dealix",
        account_id="acct-1",
        company_name="Source-backed Company",
        sector="operations",
        company_size="sme",
        department="sales",
        relationship="prospect",
        permission="warm",
        decision_maker_role="Operations director",
        offer_match="Revenue Proof Sprint",
        why_now="A dated source shows an operational change.",
        value_exchange="Bounded workflow proof.",
        pain_hypotheses=("Manual follow-up may be slow.",),
        unknowns=("Baseline cycle time",),
        evidence=(
            EvidenceReference(
                source_ref="https://example.com/company/news",
                source_type="company_website",
                observed_at="2026-07-15T00:00:00Z",
                quality="primary",
            ),
        ),
        strategic_fit=80,
        urgency=70,
    )


def test_revenue_lab_run_id_is_deterministic() -> None:
    first = run_revenue_lab([make_signal()])
    second = run_revenue_lab([make_signal()])

    assert first.run_id == second.run_id


def test_source_linked_outcome_is_not_customer_proof() -> None:
    outcome = OutcomeEvent(
        account_id="acct-1",
        outcome="meeting_booked",
        source_ref="crm:event-42",
        observed_at="2026-07-15T00:00:00Z",
    )

    bundle = run_revenue_lab([make_signal()], outcomes=[outcome])

    assert bundle.summary["verified_customer_outcomes"] == 0
    assert bundle.learning_recommendations[0].weight_change_applied is False


def test_customer_proof_requires_validation_and_delivery_evidence() -> None:
    outcome = OutcomeEvent(
        account_id="acct-1",
        outcome="value_confirmed",
        source_ref="crm:event-42",
        observed_at="2026-07-15T00:00:00Z",
        customer_validated=True,
        customer_validation_ref="crm:customer-confirmation-42",
        delivery_proof_ref="delivery:log-42",
    )

    bundle = run_revenue_lab([make_signal()], outcomes=[outcome])

    assert bundle.summary["verified_customer_outcomes"] == 1


def test_customer_validation_cannot_be_claimed_without_validation_reference() -> None:
    with pytest.raises(ValueError, match="customer_validation_ref"):
        OutcomeEvent(
            account_id="acct-1",
            outcome="value_confirmed",
            source_ref="crm:event-42",
            observed_at="2026-07-15T00:00:00Z",
            customer_validated=True,
        )
