"""
Test: Commercial Offer Mapping
Ensures every pain category has a mapped offer, and every offer has a pain category.
"""
import json
import yaml
from pathlib import Path


def test_pain_to_offer_coverage():
    """Every pain category must have at least one offer."""
    with open("data/commercial/pain_to_offer.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    pain_categories = {
        "lead_leakage",
        "follow_up_chaos",
        "crm_data_disorder",
        "proposal_delay",
        "weak_reporting",
        "sales_team_inconsistency",
        "support_overload",
        "no_proof_case_study_system",
        "slow_onboarding",
        "weak_renewal_upsell",
    }

    mapped_pains = {p["pain"] for p in data.get("primary_mapping", [])}
    missing = pain_categories - mapped_pains
    assert not missing, f"Missing pain categories in offer mapping: {missing}"


def test_offer_has_pain_category():
    """Every offer in product_catalog must be referenced by a pain or bundle."""
    with open("data/commercial/product_catalog.yaml", encoding="utf-8") as f:
        catalog = yaml.safe_load(f)

    with open("data/commercial/pain_to_offer.yaml", encoding="utf-8") as f:
        mapping = yaml.safe_load(f)

    offer_ids = {o["id"] for o in catalog.get("offers", [])}
    mapped_offers = {p["offer"] for p in mapping.get("primary_mapping", [])}
    bundle_offers = {b.get("primary_offer") for b in mapping.get("bundles", []) if b.get("primary_offer")}
    all_mapped = mapped_offers | bundle_offers

    # readiness_scan is the entry (no pain needed)
    # custom_company_os is custom (per SOW, no fixed pain)
    # monthly_optimization_retainer is post-delivery (mapped to weak_renewal_upsell)
    excluded = {"readiness_scan", "custom_company_os"}
    expected_min = offer_ids - excluded
    missing = expected_min - all_mapped
    assert not missing, f"Offers not mapped to any pain or bundle: {missing}"


def test_bundle_offers_exist():
    """All bundle offers must exist in product catalog OR be sub-modules."""
    with open("data/commercial/product_catalog.yaml", encoding="utf-8") as f:
        catalog = yaml.safe_load(f)

    with open("data/commercial/pain_to_offer.yaml", encoding="utf-8") as f:
        mapping = yaml.safe_load(f)

    catalog_ids = {o["id"] for o in catalog.get("offers", [])}
    # Sub-modules (referenced in pain matrix as components of larger offers)
    sub_modules = {
        "proposal_factory",
        "weekly_revenue_command",
        "support_triage_draft_os",
        "proof_pack_factory",
    }
    valid_ids = catalog_ids | sub_modules

    for bundle in mapping.get("bundles", []):
        assert bundle["primary_offer"] in valid_ids, (
            f"Bundle references unknown offer: {bundle['primary_offer']}"
        )


def test_anti_patterns_have_action():
    """Every anti-pattern must have a risk + action."""
    with open("data/commercial/pain_to_offer.yaml", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    for anti in data.get("anti_patterns", []):
        assert "scenario" in anti, f"Anti-pattern missing scenario: {anti}"
        assert "action" in anti, f"Anti-pattern missing action: {anti}"


def test_vertical_pain_priority_consistent():
    """Each ICP in icp_segments must have a pain priority in pain_to_offer."""
    with open("data/commercial/icp_segments.yaml", encoding="utf-8") as f:
        icp = yaml.safe_load(f)

    with open("data/commercial/pain_to_offer.yaml", encoding="utf-8") as f:
        pain = yaml.safe_load(f)

    icp_ids = {s["id"] for s in icp.get("segments", [])}
    pain_segments = set(pain.get("vertical_pain_priority", {}).keys())

    missing = icp_ids - pain_segments
    assert not missing, f"ICPs without pain priority: {missing}"


if __name__ == "__main__":
    test_pain_to_offer_coverage()
    test_offer_has_pain_category()
    test_bundle_offers_exist()
    test_anti_patterns_have_action()
    test_vertical_pain_priority_consistent()
    print("All commercial offer mapping tests passed")
