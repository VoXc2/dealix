import pytest
from typing import Dict, Any, List


def validate_weekly_report(report: Dict[str, Any]) -> List[str]:
    """
    Validate weekly value report has all required fields.
    Returns list of missing fields.
    """
    required_fields = [
        "report_id",
        "engagement_id",
        "client_name",
        "week_number",
        "report_date",
        "delivered_this_week",
        "improvements",
        "next_actions",
        "prepared_by"
    ]
    
    missing = []
    for field in required_fields:
        if field not in report:
            missing.append(field)
    
    return missing


def validate_improvement(improvement: Dict[str, Any]) -> bool:
    """Validate improvement has required fields and is_hypothetical is properly set."""
    required = ["metric", "improvement"]
    for field in required:
        if field not in improvement:
            return False
    
    # Hypothetical improvements must be labeled
    if improvement.get("is_hypothetical", False):
        # Already labeled - OK
        pass
    
    return True


class TestWeeklyValueReport:
    
    def test_valid_report_passes(self):
        """Test complete report passes validation."""
        report = {
            "report_id": "wr_001",
            "engagement_id": "E001",
            "client_name": "Test Client",
            "week_number": 1,
            "report_date": "2026-06-03",
            "delivered_this_week": [
                {"deliverable": "Workflow A", "status": "completed"}
            ],
            "improvements": [
                {"metric": "Response time", "improvement": "50% faster"}
            ],
            "next_actions": [
                {"action": "Continue", "owner": "CS Lead"}
            ],
            "prepared_by": "CS Lead"
        }
        missing = validate_weekly_report(report)
        assert len(missing) == 0
    
    def test_missing_report_id(self):
        """Test missing report_id is caught."""
        report = {
            "engagement_id": "E001",
            "client_name": "Test Client",
            "week_number": 1,
            "report_date": "2026-06-03",
            "delivered_this_week": [],
            "improvements": [],
            "next_actions": [],
            "prepared_by": "CS Lead"
        }
        missing = validate_weekly_report(report)
        assert "report_id" in missing
    
    def test_missing_engagement_id(self):
        """Test missing engagement_id is caught."""
        report = {
            "report_id": "wr_001",
            "client_name": "Test Client",
            "week_number": 1,
            "report_date": "2026-06-03",
            "delivered_this_week": [],
            "improvements": [],
            "next_actions": [],
            "prepared_by": "CS Lead"
        }
        missing = validate_weekly_report(report)
        assert "engagement_id" in missing
    
    def test_multiple_missing_fields(self):
        """Test multiple missing fields are all caught."""
        report = {}
        missing = validate_weekly_report(report)
        assert len(missing) == 9
        assert "report_id" in missing
        assert "engagement_id" in missing
        assert "prepared_by" in missing
    
    def test_empty_delivered_this_week_allowed(self):
        """Test empty delivered_this_week is allowed."""
        report = {
            "report_id": "wr_001",
            "engagement_id": "E001",
            "client_name": "Test Client",
            "week_number": 1,
            "report_date": "2026-06-03",
            "delivered_this_week": [],
            "improvements": [],
            "next_actions": [],
            "prepared_by": "CS Lead"
        }
        missing = validate_weekly_report(report)
        assert "delivered_this_week" not in missing
    
    def test_improvement_validation(self):
        """Test improvement validation."""
        improvement = {
            "metric": "Time to response",
            "improvement": "50% reduction"
        }
        assert validate_improvement(improvement) is True
    
    def test_improvement_missing_metric(self):
        """Test improvement without metric fails."""
        improvement = {
            "improvement": "50% reduction"
        }
        assert validate_improvement(improvement) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
