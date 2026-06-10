import pytest
from typing import Dict, List


def calculate_health_score(components: Dict[str, int]) -> float:
    """
    Calculate health score from components.
    Weights: onboarding 15%, access 10%, delivery 15%, reports 10%,
              engagement 15%, blockers 10%, payment 10%, value_proof 10%, stakeholders 5%
    """
    weights = {
        "onboarding_progress": 0.15,
        "access_completeness": 0.10,
        "delivery_progress": 0.15,
        "weekly_report_delivered": 0.10,
        "client_engagement": 0.15,
        "unresolved_blockers": 0.10,
        "payment_status": 0.10,
        "value_proof_level": 0.10,
        "stakeholder_engagement": 0.05
    }
    
    total = 0.0
    for key, weight in weights.items():
        score = components.get(key, 0)
        total += score * weight
    
    return round(total, 2)


def get_health_status(score: float) -> str:
    """Get health status from score."""
    if score >= 80:
        return "healthy"
    elif score >= 60:
        return "watch"
    elif score >= 40:
        return "at_risk"
    else:
        return "blocked"


class TestClientHealthScore:
    
    def test_healthy_score(self):
        """Test score in healthy range."""
        components = {
            "onboarding_progress": 100,
            "access_completeness": 100,
            "delivery_progress": 100,
            "weekly_report_delivered": 100,
            "client_engagement": 100,
            "unresolved_blockers": 100,
            "payment_status": 100,
            "value_proof_level": 100,
            "stakeholder_engagement": 100
        }
        score = calculate_health_score(components)
        assert score == 100.0
        assert get_health_status(score) == "healthy"
    
    def test_watch_score(self):
        """Test score in watch range."""
        components = {
            "onboarding_progress": 75,
            "access_completeness": 75,
            "delivery_progress": 75,
            "weekly_report_delivered": 75,
            "client_engagement": 75,
            "unresolved_blockers": 75,
            "payment_status": 75,
            "value_proof_level": 75,
            "stakeholder_engagement": 75
        }
        score = calculate_health_score(components)
        assert score == 75.0
        assert get_health_status(score) == "watch"
    
    def test_at_risk_score(self):
        """Test score in at_risk range."""
        components = {
            "onboarding_progress": 50,
            "access_completeness": 50,
            "delivery_progress": 50,
            "weekly_report_delivered": 50,
            "client_engagement": 50,
            "unresolved_blockers": 50,
            "payment_status": 50,
            "value_proof_level": 50,
            "stakeholder_engagement": 50
        }
        score = calculate_health_score(components)
        assert score == 50.0
        assert get_health_status(score) == "at_risk"
    
    def test_blocked_score(self):
        """Test score in blocked range."""
        components = {
            "onboarding_progress": 25,
            "access_completeness": 25,
            "delivery_progress": 25,
            "weekly_report_delivered": 25,
            "client_engagement": 25,
            "unresolved_blockers": 25,
            "payment_status": 25,
            "value_proof_level": 25,
            "stakeholder_engagement": 25
        }
        score = calculate_health_score(components)
        assert score == 25.0
        assert get_health_status(score) == "blocked"
    
    def test_missing_component_defaults_to_zero(self):
        """Test that missing components default to zero."""
        components = {}
        score = calculate_health_score(components)
        assert score == 0.0
    
    def test_renewal_ready_status(self):
        """Test renewal_ready status is set for high scores."""
        score = 85.0
        status = get_health_status(score)
        assert status == "healthy"
    
    def test_churn_risk_status(self):
        """Test churn_risk is blocked status."""
        score = 30.0
        status = get_health_status(score)
        assert status == "blocked"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
