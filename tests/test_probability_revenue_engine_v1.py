import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "config/commercial/probability_revenue_engine_v1.json"
ENGINE = ROOT / "scripts/commercial/run_probability_revenue_engine_v1.py"


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def load_engine():
    spec = importlib.util.spec_from_file_location("probability_revenue_engine_v1", ENGINE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def test_deep_wip_requires_attributable_evidence():
    engine = load_engine()
    weak = {
        "company_name": "Weak hypothesis",
        "source": "manual-score-only",
        "evidence_score": 100,
        "fit_score": 100,
        "urgency_score": 100,
        "access_score": 100,
        "risk_score": 0,
    }
    strong = {
        "company_name": "Evidence-backed target",
        "source": "https://example.test/tender",
        "fit_score": 80,
        "urgency_score": 80,
        "evidence_score": 80,
        "access_score": 40,
        "risk_score": 20,
    }
    ranked = engine.rank_targets([weak, strong], deep_wip=3)
    by_name = {row["company_name"]: row for row in ranked}
    assert by_name["Weak hypothesis"]["deep_wip_candidate"] is False
    assert by_name["Weak hypothesis"]["truth"]["source_attributable"] is False
    assert by_name["Evidence-backed target"]["deep_wip_candidate"] is True
    assert by_name["Evidence-backed target"]["truth"]["source_attributable"] is True


def test_explicit_evidence_reference_can_make_non_url_source_attributable():
    engine = load_engine()
    target = {
        "company_name": "Evidence-ref target",
        "source": "Etimad export",
        "evidence_refs": ["etimad:tender:123"],
        "fit_score": 80,
        "urgency_score": 90,
        "evidence_score": 90,
        "access_score": 30,
        "risk_score": 20,
    }
    row = engine.rank_targets([target], deep_wip=3)[0]
    assert row["truth"]["source_attributable"] is True
    assert row["deep_wip_candidate"] is True


def test_known_ev_without_evidence_is_blocked_from_deep_wip():
    engine = load_engine()
    target = {
        "company_name": "Synthetic certainty",
        **{key: 0.9 for key in engine.PROBABILITY_KEYS},
        **{key: 10 for key in engine.VALUE_KEYS},
        **{key: 1 for key in engine.COST_RISK_KEYS},
    }
    row = engine.rank_targets([target], deep_wip=3)[0]
    assert row["expected_value"] is not None
    assert row["disposition"] == "EV_BLOCKED_EVIDENCE_GAP"
    assert row["deep_wip_candidate"] is False


def test_duplicate_company_records_cannot_consume_multiple_deep_wip_slots():
    engine = load_engine()
    first = {
        "company_name": "ACME Saudi Co.",
        "source": "https://example.test/acme/1",
        "fit_score": 90,
        "urgency_score": 90,
        "evidence_score": 90,
        "access_score": 50,
        "risk_score": 10,
    }
    duplicate = {
        "company_name": "acme saudi co",
        "source": "https://example.test/acme/2",
        "fit_score": 85,
        "urgency_score": 85,
        "evidence_score": 85,
        "access_score": 45,
        "risk_score": 15,
    }
    other = {
        "company_name": "Other Company",
        "source": "https://example.test/other",
        "fit_score": 80,
        "urgency_score": 80,
        "evidence_score": 80,
        "access_score": 40,
        "risk_score": 20,
    }
    ranked = engine.rank_targets([first, duplicate, other], deep_wip=3)
    active = [row for row in ranked if row["deep_wip_candidate"]]
    assert len(active) == 2
    assert len({row["company_key"] for row in active}) == 2
    duplicate_rows = [row for row in ranked if row["company_key"] == engine.canonical_company_key("ACME Saudi Co.")]
    assert sum(1 for row in duplicate_rows if row["deep_wip_candidate"]) == 1
    assert any(row["duplicate_deep_wip_company"] for row in duplicate_rows)


def test_runtime_limit_is_clamped_to_contract_ceiling():
    text = ENGINE.read_text(encoding="utf-8")
    assert 'raw_signal_ceiling = int(contract["capacity_ceiling_per_operating_day"]["raw_signal_refresh"])' in text
    assert "effective_limit = min(requested_limit, raw_signal_ceiling)" in text
    assert '"effective_limit": effective_limit' in text
