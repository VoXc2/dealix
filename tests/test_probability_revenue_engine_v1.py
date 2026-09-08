import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "config/commercial/probability_revenue_engine_v1.json"


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_material_authority_fail_closed():
    data = load_contract()
    authority = data["authority"]
    for key in (
        "external_send",
        "public_publish",
        "paid_spend",
        "payment_execution",
        "production_mutation",
        "dns_mutation",
        "db_mutation",
        "secret_mutation",
        "identity_mutation",
    ):
        assert authority[key] is False


def test_exactly_five_permanent_agents():
    data = load_contract()
    assert set(data["owners"].values()) == {
        "dealix-pm",
        "dealix-sales",
        "dealix-delivery",
        "dealix-engineer",
        "dealix-content",
    }


def test_high_volume_research_does_not_expand_deep_wip():
    data = load_contract()
    capacity = data["capacity_ceiling_per_operating_day"]
    assert capacity["raw_signal_refresh"] >= 1000
    assert capacity["deep_commercial_wip"] <= 3
    assert capacity["material_action_packets"] <= 1


def test_probability_unknowns_are_not_invented():
    data = load_contract()
    assert data["unknown_probability_policy"] == "UNKNOWN_NOT_EVIDENCE_BACKED"
    assert "unknown_probability != evidence" in data["truth_firewall"]


def test_suppression_and_eligibility_override_allocation():
    data = load_contract()
    prohibited = set(data["allocation_policy"]["prohibited_overrides"])
    assert {"suppression", "opt_out", "channel_ineligibility"}.issubset(prohibited)


def test_revenue_truth_requires_real_outcomes():
    data = load_contract()
    outcomes = set(data["real_outcome_updates"])
    assert "verified_payment" in outcomes
    assert "delivery_acceptance" in outcomes
    assert "permissioned_customer_proof" in outcomes
