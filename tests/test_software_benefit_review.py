from scripts.ops.software_benefit_review import review_candidate


def candidate(**observation_overrides):
    observations = {
        "security_incidents": 0,
        "job_success_rate": 0.95,
        "founder_minutes_saved": 120,
        "cash_saved": 200,
        "cash_cost": 20,
        "maintenance_minutes": 15,
        "evidence_refs": ["receipt://observed"],
    }
    observations.update(observation_overrides)
    return {
        "candidate_id": "tool-1",
        "vulnerability_status": "CLEAR",
        "benefit_observations": observations,
    }


def test_seven_day_positive_value_keeps_canary() -> None:
    result = review_candidate(candidate(), window_days=7)
    assert result["decision"] == "KEEP_CANARY"
    assert result["counts_as_verified_value"] is True


def test_thirty_day_positive_value_promotes() -> None:
    result = review_candidate(candidate(), window_days=30)
    assert result["decision"] == "PROMOTE"


def test_security_incident_quarantines() -> None:
    result = review_candidate(candidate(security_incidents=1), window_days=7)
    assert result["decision"] == "QUARANTINE"


def test_low_reliability_demotes() -> None:
    result = review_candidate(candidate(job_success_rate=0.5), window_days=7)
    assert result["decision"] == "DEMOTE"


def test_cost_without_value_kills_at_thirty_days() -> None:
    result = review_candidate(
        candidate(founder_minutes_saved=0, cash_saved=0, cash_cost=100),
        window_days=30,
    )
    assert result["decision"] == "KILL"
