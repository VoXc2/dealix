"""A proposal must map to a real product/service in the catalog."""

from core.safety.commercial import evaluate_proposal
from tests._fixtures import PRODUCT_CATALOG


def test_proposal_without_mapping_fails():
    proposal = {"product_id": "MADE_UP_SKU", "qualified": True}
    res = evaluate_proposal(proposal, PRODUCT_CATALOG)
    assert res.allowed is False
    assert "proposal_not_mapped_to_catalog" in res.reasons


def test_proposal_with_valid_mapping_passes_mapping_check():
    proposal = {"product_id": "P1_SPRINT", "qualified": True}
    res = evaluate_proposal(proposal, PRODUCT_CATALOG)
    assert "proposal_not_mapped_to_catalog" not in res.reasons


def test_final_price_requires_approval():
    proposal = {"product_id": "P1_SPRINT", "qualified": True, "final_price": 5000}
    res = evaluate_proposal(proposal, PRODUCT_CATALOG)
    assert "final_price_requires_human_approval" in res.reasons
    assert res.allowed is False
