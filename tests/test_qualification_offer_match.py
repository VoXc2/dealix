import pytest

from dealix.commercial.economic_cell import Sector
from dealix.commercial.qualification_offer_match import (
    QualificationInput,
    QualificationState,
    match_offers,
    qualify,
)


def test_research_signal_never_becomes_relationship_or_proposal() -> None:
    inp = QualificationInput(
        entity_id="research-1",
        sector=Sector.FINANCE_FINTECH_INSURANCE,
        problem="regulated_integration_readiness",
        market_signal_refs=["source::sama_open_banking"],
    )
    decision = qualify(inp)

    assert decision.state == QualificationState.SIGNAL
    assert decision.proposal_allowed is False
    assert decision.research_counts_as_relationship is False
    assert decision.public_contact_counts_as_consent is False
    assert match_offers(inp, decision) == []


def test_qualified_problem_requires_real_interaction_problem_impact_and_delivery_fit() -> None:
    inp = QualificationInput(
        entity_id="customer-1",
        sector=Sector.PROFESSIONAL_SERVICES,
        buyer_role="ceo",
        problem="revenue_leakage",
        real_interaction_refs=["gmail::thread-1"],
        problem_evidence_refs=["customer::problem-confirmed"],
        impact_evidence_refs=["customer::impact-described"],
        delivery_fit_refs=["dealix::delivery-fit-reviewed"],
    )
    decision = qualify(inp)

    assert decision.state == QualificationState.QUALIFIED_PROBLEM
    assert decision.proposal_allowed is True
    assert decision.proposal_basis == "QUALIFIED_PROBLEM"
    assert match_offers(inp, decision)


def test_explicit_customer_request_opens_proposal_gate_without_faking_qualified_problem() -> None:
    inp = QualificationInput(
        entity_id="customer-2",
        sector=Sector.TECHNOLOGY_SAAS_SI,
        buyer_role="ceo",
        problem="automation_need",
        real_interaction_refs=["email::request"],
        problem_evidence_refs=["email::request"],
        explicit_customer_proposal_request=True,
    )
    decision = qualify(inp)

    assert decision.state == QualificationState.REAL_INTERACTION
    assert decision.proposal_allowed is True
    assert decision.proposal_basis == "EXPLICIT_CUSTOMER_REQUEST"


def test_won_cannot_skip_proposal_evidence() -> None:
    inp = QualificationInput(
        entity_id="bad-win",
        sector=Sector.RETAIL_COMMERCE_ECOMMERCE,
        verified_won_refs=["manual::claimed-win"],
    )

    with pytest.raises(ValueError, match="cannot skip"):
        qualify(inp)
