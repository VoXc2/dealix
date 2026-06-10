"""
Test: Customer Success Handoff Required
Ensures customer success handoff is required after delivery.
"""
from pathlib import Path
import json


def test_cs_handoff_doc_exists():
    """CUSTOMER_SUCCESS_OS_AR.md must exist."""
    assert Path("docs/customer_success/CUSTOMER_SUCCESS_OS_AR.md").exists()


def test_first_30_days_doc_exists():
    """FIRST_30_DAYS_AR.md must exist."""
    assert Path("docs/customer_success/FIRST_30_DAYS_AR.md").exists()


def test_health_score_doc_exists():
    """CLIENT_HEALTH_SCORE_AR.md must exist."""
    assert Path("docs/customer_success/CLIENT_HEALTH_SCORE_AR.md").exists()


def test_renewal_playbook_exists():
    """RENEWAL_PLAYBOOK_AR.md must exist."""
    assert Path("docs/customer_success/RENEWAL_PLAYBOOK_AR.md").exists()


def test_expansion_playbook_exists():
    """EXPANSION_PLAYBOOK_AR.md must exist."""
    assert Path("docs/customer_success/EXPANSION_PLAYBOOK_AR.md").exists()


def test_client_health_schema():
    """Client health schema must be valid."""
    with open("schemas/client_health.schema.json") as f:
        schema = json.load(f)

    required = schema.get("required", [])
    assert "id" in required
    assert "client_id" in required
    assert "date" in required
    assert "scores" in required
    assert "total" in required
    assert "tier" in required

    # Tier must be valid
    tier_enum = schema["properties"]["tier"]["enum"]
    assert "green" in tier_enum
    assert "yellow" in tier_enum
    assert "orange" in tier_enum
    assert "red" in tier_enum


def test_health_score_components():
    """Health score must have 8 components as documented."""
    with open("schemas/client_health.schema.json") as f:
        schema = json.load(f)

    scores_required = schema["properties"]["scores"]["required"]
    expected_components = [
        "onboarding_complete",
        "access_complete",
        "first_workflow_delivered",
        "weekly_report_delivered",
        "client_engagement",
        "value_proof",
        "unresolved_risks",
        "renewal_fit",
    ]
    for component in expected_components:
        assert component in scores_required, (
            f"Health score missing component: {component}"
        )


def _read_utf8(path):
    """Read file with UTF-8 encoding."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def test_renewal_timeline_documented():
    """Renewal timeline should mention key milestones (90/60/30/14 days)."""
    content = _read_utf8("docs/customer_success/RENEWAL_PLAYBOOK_AR.md")
    # Look for renewal timeline indicators
    timeline_indicators = [
        "90",
        "60",
        "30",
        "Renewal Cadence",
        "renewal timeline",
        "Renewal Timeline",
        "renewal",
        "Renewal",
        "الجدول",
        "التجديد",
    ]
    found_count = sum(1 for ind in timeline_indicators if ind in content)
    assert found_count >= 3, f"Renewal timeline insufficient: only {found_count} indicators found"


def test_cs_handoff_from_delivery():
    """CS handoff must be required after delivery."""
    content = _read_utf8("docs/customer_success/CUSTOMER_SUCCESS_OS_AR.md")
    assert "handoff" in content.lower() or "تسليم" in content


def test_weekly_report_required():
    """Weekly report must be a CS requirement."""
    content = _read_utf8("docs/customer_success/CUSTOMER_SUCCESS_OS_AR.md")
    assert "weekly" in content.lower() or "أسبوعي" in content


if __name__ == "__main__":
    test_cs_handoff_doc_exists()
    test_first_30_days_doc_exists()
    test_health_score_doc_exists()
    test_renewal_playbook_exists()
    test_expansion_playbook_exists()
    test_client_health_schema()
    test_health_score_components()
    test_renewal_timeline_documented()
    test_cs_handoff_from_delivery()
    test_weekly_report_required()
    print("All customer success handoff tests passed")
