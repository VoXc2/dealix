import pytest
from typing import Dict, Any, List


def validate_expansion_maps_to_delivered_value(expansion: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate expansion proposal maps to delivered value.
    Returns dict with is_valid and errors.
    """
    errors = []
    
    # Expansion must reference delivered value
    if "delivered_value_summary" not in expansion:
        errors.append("Expansion must include delivered_value_summary")
    elif not expansion["delivered_value_summary"]:
        errors.append("delivered_value_summary cannot be empty")
    
    # Must have evidence level
    if "evidence_level" not in expansion:
        errors.append("Expansion requires evidence_level")
    elif expansion["evidence_level"] not in ["L3", "L4", "L5"]:
        errors.append("evidence_level must be L3, L4, or L5 for expansion")
    
    # Must have expected outcomes
    if "expected_outcomes" not in expansion:
        errors.append("Expansion requires expected_outcomes")
    elif not expansion["expected_outcomes"]:
        errors.append("expected_outcomes cannot be empty")
    
    # Next workflow should be related to delivered value
    if "proposed_workflow" in expansion and "delivered_value_summary" in expansion:
        delivered = expansion["delivered_value_summary"].lower()
        proposed = expansion["proposed_workflow"].lower()
        # Basic check - should be related
        if not any(word in proposed for word in delivered.split() if len(word) > 3):
            errors.append("proposed_workflow should relate to delivered_value_summary")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


def can_proceed_to_expansion(expansion: Dict[str, Any]) -> bool:
    """Check if expansion can proceed based on evidence level."""
    result = validate_expansion_maps_to_delivered_value(expansion)
    
    if not result["is_valid"]:
        return False
    
    # Must have L3+ evidence to proceed
    evidence = expansion.get("evidence_level", "")
    return evidence in ["L3", "L4", "L5"]


class TestExpansionMapsToDeliveredValue:
    
    def test_expansion_with_complete_mapping_passes(self):
        """Test expansion with complete mapping passes."""
        expansion = {
            "expansion_id": "exp_001",
            "engagement_id": "E001",
            "delivered_value_summary": "Improved response time by 50%",
            "evidence_level": "L4",
            "expected_outcomes": [
                {"outcome": "Faster resolution", "metric": "time", "expected_value": "30% improvement"}
            ],
            "proposed_workflow": "Implement response time optimization"
        }
        result = validate_expansion_maps_to_delivered_value(expansion)
        assert result["is_valid"] is True
        assert can_proceed_to_expansion(expansion) is True
    
    def test_expansion_without_delivered_value_fails(self):
        """Test expansion without delivered_value_summary fails."""
        expansion = {
            "expansion_id": "exp_001",
            "engagement_id": "E001",
            "evidence_level": "L4",
            "expected_outcomes": [{"outcome": "Better results"}]
        }
        result = validate_expansion_maps_to_delivered_value(expansion)
        assert result["is_valid"] is False
        assert "Expansion must include delivered_value_summary" in result["errors"]
    
    def test_expansion_low_evidence_fails_proceed(self):
        """Test expansion with low evidence cannot proceed."""
        expansion = {
            "expansion_id": "exp_001",
            "engagement_id": "E001",
            "delivered_value_summary": "Some improvement",
            "evidence_level": "L2",  # Too low
            "expected_outcomes": [{"outcome": "Better results"}]
        }
        result = validate_expansion_maps_to_delivered_value(expansion)
        assert result["is_valid"] is False
        assert "evidence_level must be L3, L4, or L5" in result["errors"]
        assert can_proceed_to_expansion(expansion) is False
    
    def test_expansion_without_outcomes_fails(self):
        """Test expansion without expected_outcomes fails."""
        expansion = {
            "expansion_id": "exp_001",
            "engagement_id": "E001",
            "delivered_value_summary": "Improved response time",
            "evidence_level": "L4"
        }
        result = validate_expansion_maps_to_delivered_value(expansion)
        assert result["is_valid"] is False
        assert "Expansion requires expected_outcomes" in result["errors"]
    
    def test_expansion_with_l3_evidence_can_proceed(self):
        """Test expansion with L3 evidence can proceed."""
        expansion = {
            "expansion_id": "exp_001",
            "engagement_id": "E001",
            "delivered_value_summary": "Demonstrated improvement in pilot",
            "evidence_level": "L3",
            "expected_outcomes": [{"outcome": "Scaled results"}]
        }
        assert can_proceed_to_expansion(expansion) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
