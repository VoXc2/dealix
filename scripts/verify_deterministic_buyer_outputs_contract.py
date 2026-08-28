#!/usr/bin/env python3
"""Fail-closed static verification for Dealix deterministic buyer outputs contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/deterministic_buyer_outputs_contract_v1.json"
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> int:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))

    require(data.get("schema_version") == "1.0.0", "unexpected schema version")
    require(data.get("unknown_semantics") == UNKNOWN, "unknown semantics must fail closed")
    require(
        data.get("north_star") == "FIRST_VERIFIED_PAID_DEALIX_PILOT",
        "north star drift",
    )

    outputs = data.get("outputs") or {}
    require(
        set(outputs) == {
            "revenue_leak_map",
            "customer_proof_decision_pack",
            "executive_command",
        },
        "buyer output set drift",
    )

    leak = outputs["revenue_leak_map"]
    require("unknowns" in leak["required_sections"], "Revenue Leak Map must expose unknowns")
    require("next_evidence" in leak["required_sections"], "Revenue Leak Map must expose next evidence")
    require(
        any("no invented ROI" in rule for rule in leak["hard_rules"]),
        "Revenue Leak Map must prohibit invented ROI",
    )

    pack = outputs["customer_proof_decision_pack"]
    require("payment_evidence_state" in pack["required_sections"], "Proof Pack must expose payment state")
    require("delivery_evidence_state" in pack["required_sections"], "Proof Pack must expose delivery state")
    require(UNKNOWN in pack["allowed_decisions"], "Proof Pack must support unknown decision state")
    require(
        any("invoice is not payment" in rule for rule in pack["hard_rules"]),
        "Proof Pack must preserve invoice/payment firewall",
    )

    command = outputs["executive_command"]
    require(
        command["required_sections"] == [
            "metadata",
            "money",
            "decisions",
            "risks",
            "approvals",
            "next_action",
        ],
        "President/Executive Command surface drift",
    )
    require(
        "economic_evidence_refs" in command["money_required_fields"],
        "money must be evidence-backed",
    )
    require(
        "action_fingerprint" in command["approval_required_fields"],
        "approvals must bind to action fingerprint",
    )

    shared = data.get("shared_metadata") or {}
    for field in (
        "schema_version",
        "generated_at",
        "source_sha",
        "input_evidence_refs",
        "freshness",
        "authority_ref",
    ):
        require(field in shared.get("required_fields", []), f"missing shared metadata field: {field}")

    determinism = data.get("determinism") or {}
    require(determinism.get("same_normalized_inputs_same_output") is True, "determinism must be explicit")
    require(determinism.get("unknown_value") == UNKNOWN, "determinism unknown value drift")
    require(
        "cannot create or promote commercial state" in determinism.get("llm_role", ""),
        "LLM must not own truth promotion",
    )

    evidence = data.get("evidence_contract") or {}
    require(evidence.get("research_is_not_relationship") is True, "research/relationship firewall missing")
    require(evidence.get("payment_proof_required_for_revenue") is True, "payment proof gate missing")
    require(evidence.get("delivery_proof_required_for_customer_value") is True, "delivery proof gate missing")

    scope = data.get("wip_and_scope") or {}
    for key in ("no_new_dashboard", "no_new_truth_store", "no_new_scheduler", "no_new_agent_fleet"):
        require(scope.get(key) is True, f"scope invariant missing: {key}")

    print("PASS: deterministic buyer outputs contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
