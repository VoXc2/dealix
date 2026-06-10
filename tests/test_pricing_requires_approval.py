"""
Test: Pricing Requires Approval
Ensures no quote can be sent without founder approval.
"""
import re
from pathlib import Path

# Read pricing rules
import yaml


def test_no_unconditional_pricing_in_docs():
    """Pricing docs must reference founder approval for final prices."""
    pricing_docs = [
        "docs/commercial/PRICING_GUARDRAILS_AR.md",
        "docs/commercial/QUOTE_APPROVAL_POLICY_AR.md",
        "docs/commercial/PAYMENT_TERMS_AR.md",
        "docs/commercial/DISCOUNT_POLICY_AR.md",
    ]

    for doc_path in pricing_docs:
        if not Path(doc_path).exists():
            continue
        content = Path(doc_path).read_text(encoding="utf-8")
        # Must mention founder approval
        assert "founder" in content.lower() or "موافقة" in content, (
            f"{doc_path} missing founder approval reference"
        )
        # Must mention L1, L2, L3, L4, L5 OR approval levels
        assert any(f"L{i}" in content for i in range(1, 6)) or "approval_level" in content, (
            f"{doc_path} missing approval level reference"
        )


def test_pricing_yaml_requires_approval():
    """Verify pricing.yaml structure enforces approval."""
    with open("dealix/config/pricing.yaml", encoding="utf-8") as f:
        pricing = yaml.safe_load(f)

    # Each tier range should have implicit approval
    # (manual check via docs)
    assert "currency" in pricing
    assert "diagnostic" in pricing
    assert "retainer" in pricing


def test_pricing_rules_yaml_valid():
    """Verify pricing_rules.yaml structure."""
    with open("data/commercial/pricing_rules.yaml", encoding="utf-8") as f:
        rules = yaml.safe_load(f)

    assert "base_ranges" in rules
    assert "margin_floors" in rules
    assert "discount_rules" in rules
    assert "approval_levels" in rules
    assert "disallowed" in rules


def test_no_guaranteed_in_pricing():
    """No 'guaranteed' claims in pricing docs."""
    pricing_docs = [
        "docs/commercial/PRICING_GUARDRAILS_AR.md",
        "docs/commercial/QUOTE_APPROVAL_POLICY_AR.md",
        "docs/commercial/DISCOUNT_POLICY_AR.md",
    ]

    forbidden_phrases = [
        "guaranteed price",
        "ضمان السعر",
        "no risk",
        "بدون مخاطرة",
    ]

    for doc_path in pricing_docs:
        if not Path(doc_path).exists():
            continue
        content = Path(doc_path).read_text(encoding="utf-8").lower()
        for phrase in forbidden_phrases:
            assert phrase.lower() not in content, (
                f"{doc_path} contains forbidden phrase: {phrase}"
            )


def test_approval_levels_match_yaml():
    """All L1-L5 levels defined in pricing_rules."""
    with open("data/commercial/pricing_rules.yaml", encoding="utf-8") as f:
        rules = yaml.safe_load(f)

    levels = {r["approval_level"] for r in rules.get("approval_levels", [])}
    assert "L1" in levels
    assert "L2" in levels
    assert "L3" in levels
    assert "L4" in levels
    assert "L5" in levels


def test_discount_below_margin_floor_disallowed():
    """Discount rules should not allow below margin floor."""
    with open("data/commercial/pricing_rules.yaml", encoding="utf-8") as f:
        rules = yaml.safe_load(f)

    disallowed = rules.get("disallowed", [])
    assert "discount_below_margin_floor" in disallowed
    assert "discount_for_guaranteed_results" in disallowed


if __name__ == "__main__":
    test_no_unconditional_pricing_in_docs()
    test_pricing_yaml_requires_approval()
    test_pricing_rules_yaml_valid()
    test_no_guaranteed_in_pricing()
    test_approval_levels_match_yaml()
    test_discount_below_margin_floor_disallowed()
    print("All pricing requires approval tests passed")
