from __future__ import annotations

from auto_client_acquisition.agents.intake import Lead, LeadSource, LeadStatus
from auto_client_acquisition.revenue_os.crm_mirror_policy import evaluate_hubspot_mirror


def _lead(**overrides):
    values = {
        "id": "lead_test",
        "source": LeadSource.MANUAL,
        "company_name": "Example Co",
        "contact_name": "Buyer",
        "contact_email": "buyer@example.com",
        "status": LeadStatus.QUALIFIED,
        "metadata": {},
    }
    values.update(overrides)
    return Lead(**values)


def _verified_metadata(**overrides):
    values = {
        "authority_verified": True,
        "truth_class": "REAL",
        "relationship_state": "qualified",
        "evidence_id": "ev_123",
        "opportunity_id": "opp_123",
        "consent_state": "consented",
    }
    values.update(overrides)
    return values


def test_research_record_is_not_mirrored() -> None:
    decision = evaluate_hubspot_mirror(
        _lead(metadata={"truth_class": "RESEARCH_ONLY", "relationship_state": "active_research"})
    )
    assert decision.allow_contact is False
    assert decision.allow_deal is False
    assert "AUTHORITY_NOT_VERIFIED" in decision.reasons
    assert "TRUTH_CLASS_NOT_REAL" in decision.reasons


def test_fit_or_qualified_status_alone_does_not_create_crm_truth() -> None:
    lead = _lead(status=LeadStatus.QUALIFIED, fit_score=0.99, metadata={})
    decision = evaluate_hubspot_mirror(lead)
    assert decision.allow_contact is False
    assert decision.allow_deal is False


def test_real_contact_requires_actual_identifier() -> None:
    lead = _lead(contact_email=None, contact_phone=None, metadata=_verified_metadata())
    decision = evaluate_hubspot_mirror(lead)
    assert decision.allow_contact is False
    assert "NO_REAL_CONTACT_IDENTIFIER" in decision.reasons


def test_verified_relationship_can_mirror_contact_without_deal() -> None:
    lead = _lead(
        status=LeadStatus.NEW,
        metadata=_verified_metadata(
            relationship_state="real_relationship",
            opportunity_id="",
        ),
    )
    decision = evaluate_hubspot_mirror(lead)
    assert decision.allow_contact is True
    assert decision.allow_deal is False
    assert "OPPORTUNITY_NOT_QUALIFIED" in decision.reasons


def test_qualified_opportunity_can_mirror_deal() -> None:
    decision = evaluate_hubspot_mirror(_lead(metadata=_verified_metadata()))
    assert decision.allow_contact is True
    assert decision.allow_deal is True


def test_won_requires_payment_evidence() -> None:
    decision = evaluate_hubspot_mirror(
        _lead(status=LeadStatus.WON, metadata=_verified_metadata())
    )
    assert decision.allow_contact is True
    assert decision.allow_deal is False
    assert "WON_WITHOUT_PAYMENT_EVIDENCE" in decision.reasons


def test_won_with_verified_payment_can_mirror_closedwon() -> None:
    decision = evaluate_hubspot_mirror(
        _lead(
            status=LeadStatus.WON,
            metadata=_verified_metadata(
                relationship_state="paid",
                payment_verified=True,
                payment_evidence_id="pay_123",
            ),
        )
    )
    assert decision.allow_contact is True
    assert decision.allow_deal is True
    assert decision.payment_verified is True


def test_budget_is_not_automatically_crm_amount() -> None:
    decision = evaluate_hubspot_mirror(
        _lead(budget=50000, metadata=_verified_metadata())
    )
    assert decision.approved_quote_amount_sar is None


def test_quote_amount_requires_quote_evidence() -> None:
    decision = evaluate_hubspot_mirror(
        _lead(
            metadata=_verified_metadata(
                approved_quote_amount_sar=25000,
                quote_evidence_id="quote_123",
            )
        )
    )
    assert decision.approved_quote_amount_sar == 25000.0


def test_self_test_is_always_blocked() -> None:
    decision = evaluate_hubspot_mirror(
        _lead(metadata=_verified_metadata(self_test=True))
    )
    assert decision.allow_contact is False
    assert decision.allow_deal is False
    assert "SELF_TEST" in decision.reasons
