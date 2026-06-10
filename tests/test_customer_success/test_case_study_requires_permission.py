import pytest
from typing import Dict, Any


def validate_case_study(case_study: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate case study has permission.
    Returns dict with is_valid and errors.
    """
    errors = []
    
    # Named case study requires explicit permission
    if case_study.get("is_named", False):
        if not case_study.get("permission_granted", False):
            errors.append("Named case study requires permission_granted=True")
        
        if not case_study.get("permission_date"):
            errors.append("Named case study requires permission_date")
        
        if not case_study.get("permission_signed_by"):
            errors.append("Named case study requires permission_signed_by")
    
    # Anonymized case study requires accuracy check
    if case_study.get("is_anonymized", False):
        if not case_study.get("accuracy_verified", False):
            errors.append("Anonymized case study requires accuracy_verified=True")
    
    # All case studies require evidence_level
    if "evidence_level" not in case_study:
        errors.append("All case studies require evidence_level")
    elif case_study["evidence_level"] < 1 or case_study["evidence_level"] > 5:
        errors.append("evidence_level must be 1-5")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


def can_publish_case_study(case_study: Dict[str, Any]) -> bool:
    """Check if case study can be published."""
    result = validate_case_study(case_study)
    
    if not result["is_valid"]:
        return False
    
    # Named needs explicit permission
    if case_study.get("is_named"):
        return case_study.get("permission_granted", False)
    
    # Anonymized needs accuracy verified
    if case_study.get("is_anonymized"):
        return case_study.get("accuracy_verified", False)
    
    return True


class TestCaseStudyRequiresPermission:
    
    def test_named_case_study_with_permission_passes(self):
        """Test named case study with permission passes."""
        case_study = {
            "title": "Client Success Story",
            "is_named": True,
            "client_name": "Real Client",
            "permission_granted": True,
            "permission_date": "2026-06-03",
            "permission_signed_by": "CEO",
            "evidence_level": 4,
            "accuracy_verified": True
        }
        result = validate_case_study(case_study)
        assert result["is_valid"] is True
        assert can_publish_case_study(case_study) is True
    
    def test_named_case_study_without_permission_fails(self):
        """Test named case study without permission fails."""
        case_study = {
            "title": "Client Success Story",
            "is_named": True,
            "client_name": "Real Client",
            "permission_granted": False,
            "evidence_level": 4
        }
        result = validate_case_study(case_study)
        assert result["is_valid"] is False
        assert "Named case study requires permission_granted=True" in result["errors"]
        assert can_publish_case_study(case_study) is False
    
    def test_anonymized_case_study_requires_accuracy(self):
        """Test anonymized case study requires accuracy verification."""
        case_study = {
            "title": "Industry Case Study",
            "is_anonymized": True,
            "client_name": "Confidential",
            "accuracy_verified": True,
            "evidence_level": 3
        }
        result = validate_case_study(case_study)
        assert result["is_valid"] is True
    
    def test_anonymized_without_accuracy_fails(self):
        """Test anonymized case study without accuracy fails."""
        case_study = {
            "title": "Industry Case Study",
            "is_anonymized": True,
            "client_name": "Confidential",
            "accuracy_verified": False,
            "evidence_level": 3
        }
        result = validate_case_study(case_study)
        assert result["is_valid"] is False
    
    def test_missing_evidence_level_fails(self):
        """Test missing evidence_level fails."""
        case_study = {
            "title": "Case Study",
            "is_named": False,
            "permission_granted": True,
            "evidence_level": None
        }
        result = validate_case_study(case_study)
        assert result["is_valid"] is False
        assert "All case studies require evidence_level" in result["errors"]
    
    def test_invalid_evidence_level_fails(self):
        """Test invalid evidence_level fails."""
        case_study = {
            "title": "Case Study",
            "is_named": False,
            "evidence_level": 6  # Invalid
        }
        result = validate_case_study(case_study)
        assert result["is_valid"] is False
        assert "evidence_level must be 1-5" in result["errors"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
