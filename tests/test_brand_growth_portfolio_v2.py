from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from dealix.commercial.brand_growth_portfolio import (
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
    assert result["items"][0]["priority_semantics"].endswith("NOT_PURCHASE_PROBABILITY")
    assert result["items"][0]["worker"] == "dealix-sales"
    assert not any(result["authority"].values())
    assert "purchase_probability" in score_portfolio_item(
        {**items[0], "purchase_probability": 0.99}
    )["errors"]


def test_workloads_reuse_the_five_canonical_workers() -> None:
    assert route_workload("DEEP_TECHNICAL_DEMAND")["worker"] == "dealix-engineer"
    assert route_workload("PROOF_ADVOCACY_REFERRAL")["worker"] == "dealix-delivery"
    assert route_workload("UNKNOWN")["status"] == "BLOCKED"


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
