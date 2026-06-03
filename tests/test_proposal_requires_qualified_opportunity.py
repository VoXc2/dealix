"""A proposal requires a qualified opportunity."""

from core.safety.commercial import evaluate_proposal
from tests._fixtures import PRODUCT_CATALOG


def test_unqualified_opportunity_fails():
    proposal = {"product_id": "P1_SPRINT", "qualified_opportunity": False}
    res = evaluate_proposal(proposal, PRODUCT_CATALOG)
    assert res.allowed is False
    assert "proposal_requires_qualified_opportunity" in res.reasons


def test_qualified_opportunity_passes():
    proposal = {"product_id": "P1_SPRINT", "qualified_opportunity": True}
    res = evaluate_proposal(proposal, PRODUCT_CATALOG)
    assert "proposal_requires_qualified_opportunity" not in res.reasons
    assert res.allowed is True
