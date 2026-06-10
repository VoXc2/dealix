import pytest
from typing import Dict, Any, List


def validate_renewal_opportunity(renewal: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate renewal opportunity has value proof.
    Returns dict with is_valid and errors.
    """
    errors = []
    
    # Check required fields
    required_fields = ["renewal_id", "engagement_id", "client_name", "current_term_end"]
    for field in required_fields:
        if field not in renewal:
            errors.append(f"Missing required field: {field}")
    
    # Check value proof exists
    if "value_proof" not in renewal:
        errors.append("Missing value_proof field")
    elif not renewal["value_proof"]:
        errors.append("value_proof is empty")
    else:
        # Check each proof has evidence_level
        for proof in renewal["value_proof"]:
            if "evidence_level" not in proof:
                errors.append("value_proof entry missing evidence_level")
            elif proof["evidence_level"] < 1 or proof["evidence_level"] > 5:
                errors.append("evidence_level must be 1-5")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


def can_proceed_to_renewal(renewal: Dict[str, Any]) -> bool:
    """Check if renewal can proceed based on value proof."""
    result = validate_renewal_opportunity(renewal)
    
    if not result["is_valid"]:
        return False
    
    # Check at least one L3+ evidence
    for proof in renewal.get("value_proof", []):
        if proof.get("evidence_level", 0) >= 3:
            return True
    
    return False


class TestRenewalRequiresValueProof:
    
    def test_renewal_with_value_proof_passes(self):
        """Test renewal with value proof passes."""
        renewal = {
            "renewal_id": "rn_001",
            "engagement_id": "E001",
            "client_name": "Test Client",
            "current_term_end": "2026-12-31",
            "value_proof": [
                {
                    "metric": "Response time",
                    "result": "50% faster",
                    "evidence_level": 4
                }
            ]
        }
        result = validate_renewal_opportunity(renewal)
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_renewal_without_value_proof_fails(self):
        """Test renewal without value_proof fails."""
        renewal = {
            "renewal_id": "rn_001",
            "engagement_id": "E001",
            "client_name": "Test Client",
            "current_term_end": "2026-12-31"
        }
        result = validate_renewal_opportunity(renewal)
        assert result["is_valid"] is False
        assert "Missing value_proof field" in result["errors"]
    
    def test_renewal_with_empty_value_proof_fails(self):
        """Test renewal with empty value_proof fails."""
        renewal = {
            "renewal_id": "rn_001",
            "engagement_id": "E001",
            "client_name": "Test Client",
            "current_term_end": "2026-12-31",
            "value_proof": []
        }
        result = validate_renewal_opportunity(renewal)
        assert result["is_valid"] is False
        assert "value_proof is empty" in result["errors"]
    
    def test_renewal_with_low_evidence_fails_can_proceed(self):
        """Test renewal with low evidence does not pass can_proceed."""
        renewal = {
            "renewal_id": "rn_001",
            "engagement_id": "E001",
            "client_name": "Test Client",
            "current_term_end": "2026-12-31",
            "value_proof": [
                {
                    "metric": "Response time",
                    "result": "faster",
                    "evidence_level": 2
                }
            ]
        }
        result = validate_renewal_opportunity(renewal)
        assert result["is_valid"] is True  # Valid structure
        assert can_proceed_to_renewal(renewal) is False  # But can't proceed
    
    def test_renewal_with_l3_evidence_can_proceed(self):
        """Test renewal with L3 evidence can proceed."""
        renewal = {
            "renewal_id": "rn_001",
            "engagement_id": "E001",
            "client_name": "Test Client",
            "current_term_end": "2026-12-31",
            "value_proof": [
                {
                    "metric": "Response time",
                    "result": "50% faster",
                    "evidence_level": 3
                }
            ]
        }
        assert can_proceed_to_renewal(renewal) is True
    
    def test_missing_required_fields(self):
        """Test missing required fields are caught."""
        renewal = {}
        result = validate_renewal_opportunity(renewal)
        assert result["is_valid"] is False
        assert "Missing required field: renewal_id" in result["errors"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
