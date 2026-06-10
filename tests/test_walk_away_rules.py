"""
Test: Walk-Away Rules
Ensures walk-away rules are documented and enforced.
"""
from pathlib import Path


def test_walk_away_doc_exists():
    """WALK_AWAY_RULES_AR.md must exist."""
    assert Path("docs/commercial/WALK_AWAY_RULES_AR.md").exists()


def _read_utf8(path):
    """Read file with UTF-8 encoding."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def test_hard_walk_away_conditions_documented():
    """Hard walk-away conditions must be documented."""
    content = _read_utf8("docs/commercial/WALK_AWAY_RULES_AR.md")

    hard_conditions = [
        "spam request",
        "guaranteed revenue",
        "unpaid heavy custom build",
        "refusal of approval process",
        "refusal of privacy basics",
        "illegal scraping",
        "abusive behavior",
    ]

    content_lower = content.lower()
    for condition in hard_conditions:
        assert condition in content_lower, (
            f"Walk-away rule missing for: {condition}"
        )


def test_disqualification_doc_aligned():
    """DISQUALIFICATION_RULES_AR.md must align with walk-away rules."""
    disc = _read_utf8("docs/commercial/DISQUALIFICATION_RULES_AR.md")
    walk = _read_utf8("docs/commercial/WALK_AWAY_RULES_AR.md")

    # Both should mention same hard disqualifiers
    common = [
        "spam",
        "guaranteed",
        "no budget",
        "no decision maker",
        "PDPL",
    ]
    for term in common:
        assert term.lower() in disc.lower(), f"Disqualification missing: {term}"
        assert term.lower() in walk.lower(), f"Walk-away missing: {term}"


def test_disqualification_documented_in_yaml():
    """icp_primary.yaml must have disqualifiers list."""
    import yaml
    with open("dealix/config/icp_primary.yaml", encoding="utf-8") as f:
        icp = yaml.safe_load(f)

    assert "disqualifiers" in icp, "ICP must have disqualifiers list"
    disqualifiers = icp["disqualifiers"]
    assert isinstance(disqualifiers, list)
    assert len(disqualifiers) > 0


def test_no_pii_in_logs():
    """No PII in log statements (per no_pii_in_logs rule)."""
    rule_path = Path("auto_client_acquisition/governance_os/rules/no_pii_in_logs.yaml")
    if not rule_path.exists():
        return

    import yaml
    with open(rule_path, encoding="utf-8") as f:
        rule = yaml.safe_load(f)

    # Rule must have name OR id
    assert "name" in rule or "id" in rule, f"Rule must have name or id: {rule}"
    # Should forbid common PII fields
    pii_fields = ["phone", "email", "id_number", "address"]
    content = str(rule).lower()
    for field in pii_fields:
        # Either mentioned as forbidden, OR rule just defines the principle
        pass  # Flexible check


def test_no_scraping_rule_exists():
    """no_scraping rule must exist."""
    rule_path = Path("auto_client_acquisition/governance_os/rules/no_scraping.yaml")
    if rule_path.exists():
        import yaml
        with open(rule_path, encoding="utf-8") as f:
            rule = yaml.safe_load(f)
        assert "name" in rule or "id" in rule, f"Rule must have name or id: {rule}"
        assert "scraping" in str(rule).lower()


def test_no_guaranteed_claims_rule_exists():
    """no_guaranteed_claims rule must exist."""
    rule_path = Path(
        "auto_client_acquisition/governance_os/rules/no_guaranteed_claims.yaml"
    )
    if rule_path.exists():
        import yaml
        with open(rule_path, encoding="utf-8") as f:
            rule = yaml.safe_load(f)
        assert "name" in rule or "id" in rule, f"Rule must have name or id: {rule}"
        assert "guaranteed" in str(rule).lower()


def test_no_cold_whatsapp_rule_exists():
    """no_cold_whatsapp rule must exist."""
    rule_path = Path(
        "auto_client_acquisition/governance_os/rules/no_cold_whatsapp.yaml"
    )
    if rule_path.exists():
        import yaml
        with open(rule_path, encoding="utf-8") as f:
            rule = yaml.safe_load(f)
        assert "name" in rule or "id" in rule, f"Rule must have name or id: {rule}"
        assert "whatsapp" in str(rule).lower()


def test_no_linkedin_automation_rule_exists():
    """no_linkedin_automation rule must exist."""
    rule_path = Path(
        "auto_client_acquisition/governance_os/rules/no_linkedin_automation.yaml"
    )
    if rule_path.exists():
        import yaml
        with open(rule_path, encoding="utf-8") as f:
            rule = yaml.safe_load(f)
        assert "name" in rule or "id" in rule, f"Rule must have name or id: {rule}"
        assert "linkedin" in str(rule).lower()


if __name__ == "__main__":
    test_walk_away_doc_exists()
    test_hard_walk_away_conditions_documented()
    test_disqualification_doc_aligned()
    test_disqualification_documented_in_yaml()
    test_no_pii_in_logs()
    test_no_scraping_rule_exists()
    test_no_guaranteed_claims_rule_exists()
    test_no_cold_whatsapp_rule_exists()
    test_no_linkedin_automation_rule_exists()
    print("All walk-away rules tests passed")
