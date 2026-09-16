from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from dealix.commercial.brand_growth_portfolio import (
    FIXED_FIVE_AUTHORITY,
    LEGACY_ALIAS_SEMANTICS,
    LEGACY_EXECUTOR_ALIASES,
    LOGICAL_AGENT_AUTHORITY,
    MAX_ACTIVE_GROWTH_BETS_SEMANTICS,
    RUNTIME_CAPACITY_AUTHORITY,
    allocate_portfolio,
    build_content_opportunity,
    evaluate_proof_reuse,
    route_workload,
    score_portfolio_item,
    validate_experiment,
    validate_source_signal,
)

ROOT = Path(__file__).resolve().parents[1]

AUTHORITY = {
    "relationship": False,
    "consent": False,
    "offer": False,
    "price": False,
    "quote": False,
    "contract": False,
    "external_send": False,
    "public_publish": False,
    "payment": False,
    "customer_proof": False,
    "execution": False,
    "production": False,
}


def source_signal(signal_id: str = "signal-1") -> dict[str, object]:
    return {
        "signal_id": signal_id,
        "source_id": "FIRST_PARTY_OFFICIAL",
        "source_ref": "https://example.test/source/1",
        "provenance_ref": "receipt://source/1",
        "fresh_until": "2026-09-05T00:00:00+00:00",
        "sector_family": "ICT",
        "business_archetype": "RECURRING_SAAS_OR_SERVICES",
        "evidence_refs": ["evidence://source/1"],
        "facts": ["A source-bound observation."],
        "inferences": ["A buyer problem hypothesis."],
        "unknowns": ["Which owner should validate this?"],
        "authority": dict(AUTHORITY),
    }


def test_source_validation_is_strict_and_research_only() -> None:
    signal = source_signal()
    assert validate_source_signal(signal, as_of="2026-08-30T00:00:00+00:00") == []
    signal["authority"] = {**AUTHORITY, "relationship": True}
    assert "SOURCE_RECEIPT_AUTHORITY_MUST_BE_ZERO" in validate_source_signal(signal)


def test_content_opportunity_is_source_bound_and_draft_only() -> None:
    result = build_content_opportunity(
        source_signal(),
        thesis="A sourced thesis that needs review.",
        buyer_question="Where does follow-up leakage become visible?",
        audience="Saudi B2B revenue leaders",
        buying_stage="PROBLEM_AWARENESS",
        asset_type="MASTER_INSIGHT_DRAFT",
        channels=["website", "founder_linkedin"],
        cta="START_MINI_DIAGNOSTIC_OR_REQUEST_REVIEW",
        downstream_event="QUALIFIED_PROBLEM_OR_EXPLICIT_INBOUND",
        as_of="2026-08-30T00:00:00+00:00",
    )
    assert result["status"] == "DRAFT_REVIEW_ONLY"
    assert result["source_signal_id"] == "signal-1"
    assert result["public_publish"] is False
    assert not any(result["authority"].values())
    assert result["opportunity_id"] == build_content_opportunity(
        source_signal(),
        thesis="A sourced thesis that needs review.",
        buyer_question="Where does follow-up leakage become visible?",
        audience="Saudi B2B revenue leaders",
        buying_stage="PROBLEM_AWARENESS",
        asset_type="MASTER_INSIGHT_DRAFT",
        channels=["website", "founder_linkedin"],
        cta="START_MINI_DIAGNOSTIC_OR_REQUEST_REVIEW",
        downstream_event="QUALIFIED_PROBLEM_OR_EXPLICIT_INBOUND",
        as_of="2026-08-30T00:00:00+00:00",
    )["opportunity_id"]


def test_stale_signal_cannot_become_content() -> None:
    signal = source_signal()
    signal["fresh_until"] = "2026-08-29T00:00:00+00:00"
    result = build_content_opportunity(
        signal,
        thesis="Stale thesis",
        buyer_question="Question",
        audience="Audience",
        buying_stage="PROBLEM_AWARENESS",
        asset_type="MASTER_INSIGHT_DRAFT",
        channels=["website"],
        cta="REVIEW",
        downstream_event="QUALIFIED_PROBLEM",
        as_of="2026-08-30T00:00:00+00:00",
    )
    assert result["status"] == "BLOCKED"
    assert "STALE_SIGNAL" in result["errors"]


def test_proof_reuse_requires_customer_validation_limits_and_permission() -> None:
    blocked = evaluate_proof_reuse(
        {
            "proof_id": "synthetic-1",
            "proof_class": "SYNTHETIC_OR_DEMO_PROOF",
            "evidence_refs": ["evidence://synthetic/1"],
            "limitations": ["synthetic only"],
            "customer_validation_ref": "",
            "permission_state": "",
            "claim_units": [{"claim_id": "c1", "claim": "demo claim"}],
        }
    )
    assert blocked["status"] == "BLOCKED"
    assert "PROOF_CLASS_NOT_CUSTOMER_VALIDATED" in blocked["errors"]
    assert not any(blocked["authority"].values())

    ready = evaluate_proof_reuse(
        {
            "proof_id": "customer-1",
            "proof_class": "CUSTOMER_OUTCOME_PROOF",
            "evidence_refs": ["evidence://customer/1"],
            "limitations": ["one workflow and one validated period"],
            "customer_validation_ref": "validation://customer/1",
            "permission_state": "PERMISSIONED",
            "permission_ref": "permission://customer/1",
            "claim_units": [{"claim_id": "c1", "claim": "Customer-supplied claim"}],
        }
    )
    assert ready["status"] == "REUSE_READY_PENDING_CHANNEL_APPROVAL"
    assert ready["public_customer_proof"] is False
    assert ready["reuse_destinations"]


def test_president_allocation_is_bounded_and_not_purchase_probability() -> None:
    items = [
        {
            "item_id": "event-1",
            "arm": "EVENT_FIELD_INTELLIGENCE",
            "expected_verified_movement": 0.9,
            "evidence": 0.8,
            "urgency": 1.0,
            "reuse": 0.6,
            "founder_minutes": 30,
            "agent_tool_cost": 1.0,
            "risk": 0.2,
            "capacity": 1.0,
            "next_action": "PREPARE_EVENT_QUESTIONS",
        },
        {
            "item_id": "content-1",
            "arm": "SEARCH_SEO_AEO",
            "expected_verified_movement": 0.4,
            "evidence": 0.9,
            "urgency": 0.4,
            "reuse": 0.9,
            "founder_minutes": 10,
            "agent_tool_cost": 0.5,
            "risk": 0.1,
            "capacity": 1.0,
        },
    ]
    result = allocate_portfolio(items, limit=1)
    assert result["status"] == "READ_ONLY"
    assert len(result["items"]) == 1
    assert result["items"][0]["item_id"] == "content-1"
    assert result["items"][0]["priority_semantics"].endswith("NOT_PURCHASE_PROBABILITY")
    assert result["items"][0]["worker"] == "dealix-content"
    assert not any(result["authority"].values())
    assert "PURCHASE_PROBABILITY_NOT_ALLOWED" in score_portfolio_item(
        {**items[0], "purchase_probability": 0.99}
    )["errors"]


def test_workloads_reuse_the_five_canonical_workers() -> None:
    routed = route_workload("DEEP_TECHNICAL_DEMAND")
    assert routed["worker"] == "dealix-engineer"
    assert routed["worker_alias"] == "dealix-engineer"
    assert routed["worker_alias_semantics"] == LEGACY_ALIAS_SEMANTICS
    assert routed["fixed_five_authority"] is False
    assert FIXED_FIVE_AUTHORITY is False
    assert routed["logical_agent_authority"] == LOGICAL_AGENT_AUTHORITY
    assert routed["runtime_capacity_authority"] == RUNTIME_CAPACITY_AUTHORITY
    assert set(LEGACY_EXECUTOR_ALIASES) == {
        "dealix-pm",
        "dealix-sales",
        "dealix-content",
        "dealix-delivery",
        "dealix-engineer",
    }
    assert route_workload("PROOF_ADVOCACY_REFERRAL")["worker_alias"] == "dealix-delivery"
    assert route_workload("UNKNOWN")["status"] == "BLOCKED"


def test_fixed_five_has_no_registry_or_capacity_authority() -> None:
    assert LOGICAL_AGENT_AUTHORITY == "dealix.agentic_holding.runtime.build_current_registry"
    assert RUNTIME_CAPACITY_AUTHORITY == "ResourceGovernor+Session Factory"
    assert MAX_ACTIVE_GROWTH_BETS_SEMANTICS == "ECONOMIC_FOCUS_HEURISTIC_ONLY_NOT_RUNTIME_CAPACITY"
    scored = score_portfolio_item(
        {
            "item_id": "alias-1",
            "arm": "SEARCH_SEO_AEO",
            "expected_verified_movement": 0.5,
            "evidence": 0.8,
            "urgency": 0.5,
            "reuse": 0.5,
            "founder_minutes": 10,
            "agent_tool_cost": 1,
            "risk": 0.2,
            "capacity": 1,
        }
    )
    assert scored["worker_alias_semantics"] == LEGACY_ALIAS_SEMANTICS
    assert scored["fixed_five_authority"] is False


def test_experiment_decisions_are_evidence_gated() -> None:
    assert "SCALE_REQUIRES_VERIFIED_OUTCOME" in validate_experiment(
        {
            "experiment_id": "exp-1",
            "hypothesis": "A useful hypothesis",
            "decision": "SCALE",
            "verified_outcome": False,
            "outcome_evidence_refs": [],
        }
    )
    assert validate_experiment(
        {
            "experiment_id": "exp-2",
            "hypothesis": "A useful hypothesis",
            "decision": "SCALE",
            "verified_outcome": True,
            "outcome_evidence_refs": ["outcome://2"],
            "vanity_metrics_only": False,
        }
    ) == []


def test_runner_compiles_a_fail_closed_snapshot(tmp_path: Path) -> None:
    payload = {
        "generated_at": "2026-08-30T00:00:00+00:00",
        "as_of": "2026-08-30T00:00:00+00:00",
        "signals": [source_signal()],
        "proof_candidates": [
            {
                "proof_id": "customer-1",
                "proof_class": "CUSTOMER_OUTCOME_PROOF",
                "evidence_refs": ["evidence://customer/1"],
                "limitations": ["one validated period"],
                "customer_validation_ref": "validation://customer/1",
                "permission_state": "PERMISSIONED",
                "permission_ref": "permission://customer/1",
                "claim_units": [{"claim_id": "c1", "claim": "Customer-supplied claim"}],
            }
        ],
        "allocation_items": [
            {
                "item_id": "event-1",
                "arm": "EVENT_FIELD_INTELLIGENCE",
                "expected_verified_movement": 0.8,
                "evidence": 0.8,
                "urgency": 0.9,
                "reuse": 0.5,
                "founder_minutes": 20,
                "agent_tool_cost": 1,
                "risk": 0.2,
                "capacity": 1,
            }
        ],
        "experiments": [],
    }
    input_path = tmp_path / "input.json"
    output_path = tmp_path / "output.json"
    input_path.write_text(json.dumps(payload), encoding="utf-8")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    result = subprocess.run(
        [
            sys.executable,
            "scripts/commercial/run_brand_growth_portfolio_v2.py",
            "--input",
            str(input_path),
            "--out",
            str(output_path),
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    output = json.loads(output_path.read_text(encoding="utf-8"))
    assert output["schema"] == "dealix.brand-growth-portfolio-run.v1"
    assert output["status"] == "PASS"
    assert output["admitted_signal_count"] == 1
    assert output["summary"]["draft_content_opportunities"] == 1
    assert output["summary"]["proof_reuse_ready"] == 1
    assert output["external_send_or_spend"] is False
    assert output["new_scheduler"] is False


def test_runtime_verifier_is_directly_invocable_without_pythonpath() -> None:
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, "scripts/verify_brand_growth_portfolio_runtime_v1.py"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DEALIX_BRAND_GROWTH_PORTFOLIO_RUNTIME_VERDICT=PASS" in result.stdout


def test_daily_ops_executes_growth_portfolio_step_fail_closed() -> None:
    source = (ROOT / "scripts" / "run_dealix_daily_ops.py").read_text(encoding="utf-8")
    assert "if step_growth_portfolio_runtime() != 0:" in source
    assert "DEALIX_MARKET_RADAR_SNAPSHOT" in source
    assert "no synthetic radar input" in source



def test_runner_consumes_canonical_ranked_research_signals_without_authority_promotion(tmp_path: Path) -> None:
    payload = {
        "admitted_signal_count": 1,
        "ranked_research_signals": [source_signal("radar-1")],
        "as_of": "2026-08-30T00:00:00+00:00",
    }
    input_path = tmp_path / "canonical-radar.json"
    output_path = tmp_path / "canonical-output.json"
    input_path.write_text(json.dumps(payload), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/commercial/run_brand_growth_portfolio_v2.py", "--input", str(input_path), "--out", str(output_path)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    output = json.loads(output_path.read_text(encoding="utf-8"))
    assert output["signal_input_mode"] == "CANONICAL_RANKED_RESEARCH_SIGNALS"
    assert output["admitted_signal_count"] == 1
    assert output["summary"]["draft_content_opportunities"] == 1
    assert output["adapted_signal_semantics"] == "RESEARCH_ONLY_CONTENT_OR_DIAGNOSTIC_HYPOTHESIS_ONLY"
    assert output["authority"] == AUTHORITY
    assert output["external_send_or_spend"] is False
    assert all(item["authority"] == AUTHORITY for item in output["content_opportunities"])


def test_runner_preserves_native_signals_input_mode(tmp_path: Path) -> None:
    payload = {"signals": [source_signal()], "as_of": "2026-08-30T00:00:00+00:00"}
    input_path = tmp_path / "native.json"
    output_path = tmp_path / "native-output.json"
    input_path.write_text(json.dumps(payload), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/commercial/run_brand_growth_portfolio_v2.py", "--input", str(input_path), "--out", str(output_path)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    output = json.loads(output_path.read_text(encoding="utf-8"))
    assert output["signal_input_mode"] == "NATIVE_SIGNALS"
    assert output["admitted_signal_count"] == 1


def test_runner_fails_closed_when_upstream_declares_admitted_signals_without_collection(tmp_path: Path) -> None:
    input_path = tmp_path / "broken-radar.json"
    input_path.write_text(json.dumps({"admitted_signal_count": 2, "ranked_research_signals": []}), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/commercial/run_brand_growth_portfolio_v2.py", "--input", str(input_path)],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 2
    assert "DEALIX_BRAND_GROWTH_PORTFOLIO_RUN=FAIL" in result.stdout
    assert "admitted signals declared" in result.stdout
