from __future__ import annotations

from dealix.revenue_lab.engine import RevenueLabEngine
from dealix.revenue_lab.models import CompanySignal, EvidenceReference


def _signal() -> CompanySignal:
    return CompanySignal(
        tenant_id="tenant-test",
        account_id="account-test",
        company_name="Example Co",
        sector="b2b_services",
        company_size="20-200",
        department="sales",
        relationship="prospect",
        permission="warm",
        decision_maker_role="Founder",
        offer_match="REVENUE_COMMAND_PILOT",
        why_now="A source-backed follow-up gap was observed.",
        value_exchange="Reduce decision-to-outcome leakage with governed proof.",
        pain_hypotheses=("Qualified opportunities are stalling between follow-up and decision.",),
        unknowns=("customer baseline",),
        evidence=(
            EvidenceReference(
                source_ref="internal:test-evidence-1",
                source_type="internal",
                observed_at="2026-08-29T09:00:00+00:00",
                title="Source-backed test evidence",
                quality="internal",
            ),
        ),
        strategic_fit=80,
        urgency=70,
    )


def test_revenue_lab_uses_internal_planning_seed_without_fixed_customer_duration_authority() -> None:
    bundle = RevenueLabEngine().run([_signal()])

    assert len(bundle.proposals) == 1
    assert len(bundle.delivery_plans) == 1

    proposal = bundle.proposals[0]
    delivery = bundle.delivery_plans[0]
    strategy = bundle.strategies[0]

    assert proposal.timeline_days == 30
    assert delivery.timeline_days == 30
    assert proposal.external_action_allowed is False
    assert proposal.approval_status == "approval_required"
    assert "26-30" == delivery.phases[-1]["days"]

    joined_principles = " ".join(strategy.response_principles).casefold()
    assert "customer-specific pilot with customer-specific duration" in joined_principles
    assert "fixed public offer" in joined_principles

    joined_assumptions = " ".join(proposal.assumptions).casefold()
    assert "internal planning seed only" in joined_assumptions
    assert "qualified discovery" in joined_assumptions
    assert "customer-specific quote authority" in joined_assumptions


def test_revenue_lab_keeps_external_execution_zero() -> None:
    bundle = RevenueLabEngine().run([_signal()])
    assert bundle.summary["external_actions_executed"] == 0
    assert bundle.summary["production_changes"] == 0
