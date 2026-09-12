from scripts.ops.software_benefit_review import review_candidate


def candidate(**observation_overrides):
    observations = {
        "security_incidents": 0,
        "policy_incidents": 0,
        "unexpected_data_egress_incidents": 0,
        "job_success_rate": 0.95,
        "founder_minutes_saved": 120,
        "cash_saved": 200,
        "cash_cost": 20,
        "maintenance_minutes": 15,
        "rollback_tested": True,
        "rollback_evidence_refs": ["receipt://rollback"],
        "duplicate_stack_creep": False,
        "economic_reason_to_keep": "verified founder-time and cash benefit",
        "evidence_refs": ["receipt://observed"],
    }
    observations.update(observation_overrides)
    return {
        "candidate_id": "tool-1",
        "vulnerability_status": "CLEAR",
        "cisa_kev_match": False,
        "benefit_observations": observations,
    }


def test_seven_day_positive_value_keeps_canary() -> None:
    result = review_candidate(candidate(), window_days=7)
    assert result["decision"] == "KEEP_CANARY"
    assert result["counts_as_verified_value"] is True


def test_thirty_day_positive_value_promotes_only_with_rollback_and_policy_safety() -> None:
    result = review_candidate(candidate(), window_days=30)
    assert result["decision"] == "PROMOTE"
    assert result["rollback_evidence_refs"] == ["receipt://rollback"]


def test_thirty_day_without_rollback_proof_does_not_promote() -> None:
    result = review_candidate(
        candidate(rollback_tested=False, rollback_evidence_refs=[]),
        window_days=30,
    )
    assert result["decision"] == "HOLD_MEASURE"


def test_cisa_kev_match_quarantines_even_when_value_is_positive() -> None:
    item = candidate()
    item["cisa_kev_match"] = True
    result = review_candidate(item, window_days=30)
    assert result["decision"] == "QUARANTINE"


def test_security_incident_quarantines() -> None:
    result = review_candidate(candidate(security_incidents=1), window_days=7)
    assert result["decision"] == "QUARANTINE"


def test_policy_or_data_egress_incident_quarantines() -> None:
    assert review_candidate(candidate(policy_incidents=1), window_days=7)["decision"] == "QUARANTINE"
    assert (
        review_candidate(candidate(unexpected_data_egress_incidents=1), window_days=7)["decision"]
        == "QUARANTINE"
    )


def test_low_reliability_demotes() -> None:
    result = review_candidate(candidate(job_success_rate=0.5), window_days=7)
    assert result["decision"] == "DEMOTE"


def test_duplicate_stack_creep_demotes_at_thirty_days() -> None:
    result = review_candidate(candidate(duplicate_stack_creep=True), window_days=30)
    assert result["decision"] == "DEMOTE"


def test_cost_without_value_kills_at_thirty_days() -> None:
    result = review_candidate(
        candidate(founder_minutes_saved=0, cash_saved=0, cash_cost=100),
        window_days=30,
    )
    assert result["decision"] == "KILL"
