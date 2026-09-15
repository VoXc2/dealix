#!/usr/bin/env python3
"""Fail-closed smoke verifier for the Brand & Growth Portfolio runtime."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial.brand_growth_portfolio import (  # noqa: E402
    FIXED_FIVE_AUTHORITY,
    LEGACY_ALIAS_SEMANTICS,
    LOGICAL_AGENT_AUTHORITY,
    RUNTIME_CAPACITY_AUTHORITY,
    ZERO_AUTHORITY,
    allocate_portfolio,
    build_content_opportunity,
    evaluate_proof_reuse,
    route_workload,
    validate_experiment,
    validate_source_signal,
)


def _signal() -> dict[str, object]:
    return {
        "signal_id": "runtime-smoke-1",
        "source_id": "FIRST_PARTY_OFFICIAL",
        "source_ref": "https://example.test/source/1",
        "provenance_ref": "receipt://source/1",
        "fresh_until": "2099-01-01T00:00:00+00:00",
        "evidence_refs": ["evidence://source/1"],
        "facts": ["source-bound fact"],
        "inferences": ["buyer problem hypothesis"],
        "unknowns": ["relationship and urgency"],
        "authority": dict(ZERO_AUTHORITY),
    }


def _check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    signal = _signal()
    _check(not validate_source_signal(signal), "valid source receipt rejected")

    opportunity = build_content_opportunity(
        signal,
        thesis="hypothesis",
        buyer_question="what should be verified?",
        audience="Saudi B2B",
        buying_stage="PROBLEM_AWARENESS",
        asset_type="MASTER_INSIGHT_DRAFT",
        channels=["website", "founder_linkedin"],
        cta="START_MINI_DIAGNOSTIC_OR_REQUEST_REVIEW",
        downstream_event="QUALIFIED_PROBLEM_OR_EXPLICIT_INBOUND",
    )
    _check(opportunity["status"] == "DRAFT_REVIEW_ONLY", "content draft gate failed")
    _check(not any(opportunity["authority"].values()), "content authority drift")

    proof = evaluate_proof_reuse(
        {
            "proof_id": "synthetic-1",
            "proof_class": "SYNTHETIC_OR_DEMO_PROOF",
            "evidence_refs": ["evidence://synthetic/1"],
            "limitations": ["synthetic"],
            "customer_validation_ref": "",
            "permission_state": "",
            "claim_units": [{"claim_id": "c1", "claim": "demo"}],
        }
    )
    _check(proof["status"] == "BLOCKED", "synthetic proof was reusable")

    allocation = allocate_portfolio(
        [
            {
                "item_id": "runtime-1",
                "arm": "MARKET_INTELLIGENCE_EXPERIMENTATION",
                "expected_verified_movement": 0.5,
                "evidence": 0.8,
                "urgency": 0.7,
                "reuse": 0.6,
                "founder_minutes": 10,
                "agent_tool_cost": 1,
                "risk": 0.2,
                "capacity": 1,
            }
        ]
    )
    _check(len(allocation["items"]) == 1, "allocation did not return bounded item")
    _check(not any(allocation["authority"].values()), "allocation authority drift")
    routed = route_workload("MARKET_INTELLIGENCE_EXPERIMENTATION")
    _check(routed["worker"] == "dealix-pm", "worker drift")
    _check(routed["worker_alias"] == "dealix-pm", "worker alias drift")
    _check(routed["worker_alias_semantics"] == LEGACY_ALIAS_SEMANTICS, "worker alias semantics drift")
    _check(routed["fixed_five_authority"] is False and FIXED_FIVE_AUTHORITY is False, "fixed-five authority must remain false")
    _check(routed["logical_agent_authority"] == LOGICAL_AGENT_AUTHORITY, "logical-agent authority drift")
    _check(routed["runtime_capacity_authority"] == RUNTIME_CAPACITY_AUTHORITY, "runtime capacity authority drift")

    _check(
        "SCALE_REQUIRES_VERIFIED_OUTCOME"
        in validate_experiment(
            {
                "experiment_id": "runtime-exp",
                "hypothesis": "test",
                "decision": "SCALE",
                "verified_outcome": False,
                "outcome_evidence_refs": [],
            }
        ),
        "experiment scale gate failed",
    )

    print("DEALIX_BRAND_GROWTH_PORTFOLIO_RUNTIME_VERDICT=PASS")
    print("RADAR_TO_CONTENT_OPPORTUNITY=DRAFT_ONLY")
    print("PROOF_REUSE=PERMISSION_AND_VALIDATION_GATED")
    print("PRESIDENT_ALLOCATION=BOUNDED_INTERNAL_PRIORITY")
    print("LEGACY_EXECUTOR_ALIASES_ONLY=PASS")
    print("FIXED_FIVE_AUTHORITY=FALSE")
    print("LOGICAL_AGENT_AUTHORITY=AGENTIC_HOLDING_REGISTRY")
    print("RUNTIME_CAPACITY=RESOURCE_GOVERNOR_PLUS_SESSION_FACTORY")
    print("EXTERNAL_AUTHORITY=BLOCKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
