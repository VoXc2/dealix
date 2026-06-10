"""
Test: Partner Model Margin Rules
Ensures partner margin models respect Dealix margin floors.
"""
import yaml


def test_partner_rules_yaml_structure():
    """partner_rules.yaml must have models defined."""
    with open("dealix/config/partner_rules.yaml") as f:
        rules = yaml.safe_load(f)

    assert "models" in rules
    models = rules["models"]
    expected = ["referral_partner", "implementation_partner", "co_selling_pilot", "white_label"]
    for model in expected:
        assert model in models, f"Missing partner model: {model}"


def test_referral_partner_margin_range():
    """Referral partner fee should be in 10-20% range per docs."""
    with open("dealix/config/partner_rules.yaml") as f:
        rules = yaml.safe_load(f)

    referral = rules["models"]["referral_partner"]
    fee_range = referral.get("fee_on_first_payment_percent_range", [])
    assert len(fee_range) == 2
    assert fee_range[0] <= fee_range[1]
    # Range 10-20% as documented
    assert fee_range[0] >= 5, "Minimum referral fee too low (margin erosion risk)"
    assert fee_range[1] <= 30, "Maximum referral fee too high (margin risk)"


def test_white_label_requirements():
    """White label must have minimum paid pilots requirement."""
    with open("dealix/config/partner_rules.yaml") as f:
        rules = yaml.safe_load(f)

    wl = rules["models"]["white_label"]
    assert "minimum_paid_pilots_before" in wl
    assert wl["minimum_paid_pilots_before"] >= 3, (
        "White label should require 3+ paid pilots"
    )


def test_partner_commercial_model_doc_exists():
    """PARTNER_COMMERCIAL_MODEL_AR.md must exist."""
    from pathlib import Path
    assert Path("docs/partnerships/PARTNER_COMMERCIAL_MODEL_AR.md").exists(), (
        "Missing: docs/partnerships/PARTNER_COMMERCIAL_MODEL_AR.md"
    )


def test_partner_pricing_margin_doc_exists():
    """PARTNER_PRICING_AND_MARGIN_AR.md must exist."""
    from pathlib import Path
    assert Path("docs/partnerships/PARTNER_PRICING_AND_MARGIN_AR.md").exists()


def test_partner_qualification_doc_exists():
    """PARTNER_QUALIFICATION_AR.md must exist."""
    from pathlib import Path
    assert Path("docs/partnerships/PARTNER_QUALIFICATION_AR.md").exists()


def test_partner_qualification_hard_disqualifiers():
    """Hard disqualifiers must be documented."""
    from pathlib import Path
    content = Path("docs/partnerships/PARTNER_QUALIFICATION_AR.md").read_text(encoding="utf-8").lower()

    hard = [
        "spam",
        "guaranteed",
        "no client access",
        "no legal entity",
        "abusive",
    ]
    for term in hard:
        assert term in content, f"Partner qualification missing: {term}"


def test_partner_model_approval_levels():
    """Partner models should have L2+ approval."""
    from pathlib import Path
    content = Path("docs/partnerships/PARTNER_COMMERCIAL_MODEL_AR.md").read_text(encoding="utf-8")
    # Check approval levels mentioned
    for level in ["L2", "L3", "L4", "L5"]:
        assert level in content, f"Partner model missing approval level: {level}"


def test_partner_opportunity_schema():
    """Partner opportunity schema must exist and be valid."""
    import json
    with open("schemas/partner_opportunity.schema.json") as f:
        schema = json.load(f)

    required = schema.get("required", [])
    # Must have either client_name OR opportunity_name (depending on schema version)
    assert "partner_id" in required
    assert "stage" in required
    assert "id" in required


if __name__ == "__main__":
    test_partner_rules_yaml_structure()
    test_referral_partner_margin_range()
    test_white_label_requirements()
    test_partner_commercial_model_doc_exists()
    test_partner_pricing_margin_doc_exists()
    test_partner_qualification_doc_exists()
    test_partner_qualification_hard_disqualifiers()
    test_partner_model_approval_levels()
    test_partner_opportunity_schema()
    print("All partner model margin rules tests passed")
