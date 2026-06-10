"""
Test: Proposal Requires Qualified Opportunity
Ensures no proposal can be sent without a qualified opportunity with discovery.
"""
import json
from pathlib import Path


def test_qualification_required_for_proposal():
    """Proposal schema must require qualified opportunity fields."""
    with open("schemas/commercial_proposal.schema.json", encoding="utf-8") as f:
        schema = json.load(f)

    required_fields = schema.get("required", [])
    assert "opportunity_id" in required_fields, "Proposal must require opportunity_id"
    assert "client_name" in required_fields
    assert "scope" in required_fields
    assert "deliverables" in required_fields
    assert "timeline_days" in required_fields
    assert "price_sar" in required_fields
    assert "approval_level" in required_fields
    assert "evidence_level" in required_fields


def test_proposal_evidence_level_required():
    """Every proposal must have evidence level (0-5)."""
    with open("schemas/commercial_proposal.schema.json", encoding="utf-8") as f:
        schema = json.load(f)

    props = schema["properties"]
    assert "evidence_level" in props
    ev_props = props["evidence_level"]
    assert ev_props.get("minimum") == 0
    assert ev_props.get("maximum") == 5


def test_approval_levels_valid():
    """Approval levels must be L1-L5."""
    with open("schemas/commercial_proposal.schema.json", encoding="utf-8") as f:
        schema = json.load(f)

    approval_enum = schema["properties"]["approval_level"]["enum"]
    for level in ["L1", "L2", "L3", "L4", "L5"]:
        assert level in approval_enum, f"Missing approval level: {level}"


def test_opportunity_schema_has_qualification():
    """Opportunity schema must include qualification fields."""
    with open("schemas/opportunity.schema.json", encoding="utf-8") as f:
        schema = json.load(f)

    props = schema["properties"]
    assert "qualification" in props, "Opportunity must have qualification object"
    qual_props = props["qualification"]["properties"]
    assert "score" in qual_props
    assert "tier" in qual_props
    assert "compliance_passed" in qual_props


def test_discovery_note_required_fields():
    """Discovery note must have pain + next step."""
    with open("schemas/discovery_note.schema.json", encoding="utf-8") as f:
        schema = json.load(f)

    required = schema.get("required", [])
    assert "pain_categories" in required
    assert "next_step" in required
    assert "date" in required
    assert "attendees" in required


def test_proposal_5_question_filter_documented():
    """Proposal strategy must enforce 5-question filter."""
    content = Path("docs/commercial/PROPOSAL_STRATEGY_AR.md").read_text(encoding="utf-8")
    assert "discovery" in content.lower()
    assert "pain" in content.lower()
    assert "approval" in content.lower() or "موافقة" in content


def test_no_proposal_without_discovery_in_docs():
    """The proposal strategy should explicitly state no proposal without discovery."""
    content = Path("docs/commercial/PROPOSAL_STRATEGY_AR.md").read_text(encoding="utf-8")
    # Look for explicit language
    assert "no proposal without" in content.lower() or "لا proposal" in content or "5-Question" in content or "5-Question Filter" in content


if __name__ == "__main__":
    test_qualification_required_for_proposal()
    test_proposal_evidence_level_required()
    test_approval_levels_valid()
    test_opportunity_schema_has_qualification()
    test_discovery_note_required_fields()
    test_proposal_5_question_filter_documented()
    test_no_proposal_without_discovery_in_docs()
    print("All proposal requires qualified opportunity tests passed")
