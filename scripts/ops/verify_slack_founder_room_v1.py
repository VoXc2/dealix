#!/usr/bin/env python3
"""Verify the Dealix Slack Founder Room V1 contract.

This verifier is intentionally deterministic and offline. It validates that Slack
remains a Founder command/decision/proof mirror, that the known command channel
is pinned, that unknown identifiers stay explicit, and that Slack does not raise
Dealix external authority or introduce a parallel scheduler/fleet.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLACK_CONTRACT = ROOT / "data" / "ops" / "dealix_slack_founder_room_v1.json"
MACHINE_CONTRACT = ROOT / "data" / "ops" / "dealix_autonomous_company_machine_v2.json"

EXPECTED_TEAM_ID = "T0AV61YPQ9X"
EXPECTED_COMMAND_CHANNEL_ID = "C0BTMAWR3NY"
EXPECTED_FOUNDER_SURFACE = ["CASH", "DECISIONS", "RISKS", "APPROVALS", "NEXT_ACTION"]
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    slack = load_json(SLACK_CONTRACT)
    machine = load_json(MACHINE_CONTRACT)

    assert slack["schema_version"] == "1.1"
    assert slack["surface_id"] == "dealix_slack_founder_room_v1"
    assert slack["workspace"]["name"] == "Dealix"
    assert slack["workspace"]["team_id"] == EXPECTED_TEAM_ID
    assert slack["workspace"]["domain"] == "dealixworkspace.slack.com"
    assert slack["role"] == "FOUNDER_COMMAND_DECISION_PROOF_MIRROR_NOT_TRUTH_OWNER"

    command = slack["channels"]["dealix-command"]
    assert command["id"] == EXPECTED_COMMAND_CHANNEL_ID

    for channel_name in (
        "dealix-decisions",
        "dealix-proof-log",
        "dealix-revenue",
        "dealix-build",
    ):
        channel_id = slack["channels"][channel_name]["id"]
        assert channel_id == UNKNOWN or (
            isinstance(channel_id, str) and channel_id.startswith(("C", "G"))
        ), f"{channel_name} has an invalid channel id"

    bridge = slack["bridge"]
    assert bridge["transport"] == "slack_socket_mode"
    assert bridge["scheduler_created"] is False
    assert bridge["parallel_agent_fleet_created"] is False
    assert bridge["source_sha_policy"] == "RECEIPT_MUST_MATCH_RUNTIME_EXACT_HEAD"
    acceptance = " ".join(bridge["acceptance"]["required"])
    assert "workload_id" in acceptance
    assert "source_sha" in acceptance
    assert "receipt" in acceptance
    assert "runtime_exact_head" in acceptance

    authority = slack["authority"]
    for key in (
        "customer_send",
        "public_publish",
        "paid_spend",
        "live_payment_or_refund",
        "contract_or_legal_commitment",
        "named_quote_commitment",
        "production_mutation",
        "dns_db_secret_mutation",
        "main_merge",
    ):
        assert authority[key] is False, f"Slack must not raise authority: {key}"

    assert slack["founder_surface"] == EXPECTED_FOUNDER_SURFACE
    assert machine["founder_surface"] == EXPECTED_FOUNDER_SURFACE
    assert machine["portfolio_objective"] == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY"
    assert machine["external_effect_defaults"]["customer_send"] is False
    assert machine["external_effect_defaults"]["main_merge"] is False
    assert machine["canonical_scheduler"]["parallel_company_scheduler_allowed"] is False

    truth = set(slack["truth_firewall"])
    required_truth = {
        "slack_message!=execution",
        "draft!=sent",
        "proposal!=revenue",
        "invoice!=payment",
        "research!=relationship",
        "public_contact_data!=consent",
        "synthetic!=customer_proof",
    }
    assert required_truth.issubset(truth)

    assert slack["pro_trial"]["critical_runtime_dependency_allowed"] is False
    assert slack["pro_trial"]["free_fallback_required"] is True

    print("DEALIX_SLACK_FOUNDER_ROOM_V1=PASS")
    print(f"workspace_team_id={EXPECTED_TEAM_ID}")
    print(f"command_channel_id={EXPECTED_COMMAND_CHANNEL_ID}")
    print("slack_truth_owner=false")
    print("parallel_scheduler=false")
    print("parallel_agent_fleet=false")
    print("source_sha_policy=RUNTIME_EXACT_HEAD")
    print("external_effects=FAIL_CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
