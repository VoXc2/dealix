#!/usr/bin/env python3
"""Verify an evidence-bound Dealix Slack Founder Room bridge receipt."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "data" / "ops" / "dealix_slack_founder_room_v1.json"
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
SLACK_REF_RE = re.compile(r"^slack:[CG][A-Z0-9]+:[0-9]+(?:\.[0-9]+)?$")
SECRET_PATTERNS = (
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{8,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{10,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{10,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
)

REQUIRED_FIELDS = {
    "schema_version",
    "timestamp",
    "system_id",
    "workload_id",
    "agent",
    "runner",
    "source_sha",
    "trigger",
    "input_evidence_refs",
    "state_before",
    "action",
    "execution_boundary",
    "authority_class",
    "result",
    "output_evidence_refs",
    "next_evidence",
    "next_action",
    "idempotency_key",
    "founder_minutes",
    "agent_minutes",
    "elapsed_ms",
    "ai_cost",
    "tool_cost",
    "risk_class",
    "economic_delta",
    "learning_signal",
    "state_after",
}

ALLOWED_RESULTS = {"EXECUTED", "FAILED", "DEGRADED", "APPROVAL_REQUIRED"}
ALLOWED_BOUNDARIES = {"L0-L4_INTERNAL_FAIL_CLOSED", "L5_BLOCKED"}
ALLOWED_AUTHORITY = {"L0_L4", "APPROVAL_REQUIRED"}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return value


def assert_no_secret_material(value: object) -> None:
    rendered = json.dumps(value, ensure_ascii=False)
    for pattern in SECRET_PATTERNS:
        assert not pattern.search(rendered), "receipt contains secret-like material"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--expected-source-sha", default="")
    args = parser.parse_args()

    contract = load_json(CONTRACT_PATH)
    receipt = load_json(args.receipt)
    missing = sorted(REQUIRED_FIELDS - set(receipt))
    assert not missing, f"missing required receipt fields: {missing}"

    assert receipt["schema_version"] == "1.0"
    assert receipt["system_id"] == "command_os"
    assert receipt["agent"] == "dealix-pm"
    assert receipt["trigger"] == "slack-founder-room"
    assert receipt["state_before"] == "FOUNDER_COMMAND_RECEIVED"
    assert receipt["runner"] == contract["bridge"].get(
        "canonical_autopilot", "/opt/dealix/control/bin/dealix_company_autopilot.sh"
    ) or str(receipt["runner"]).endswith("/dealix_company_autopilot.sh")

    workload_id = receipt["workload_id"]
    assert isinstance(workload_id, str) and re.fullmatch(r"slack-[0-9a-f]{20}", workload_id)
    assert receipt["idempotency_key"] == workload_id

    source_sha = receipt["source_sha"]
    assert isinstance(source_sha, str) and SHA_RE.fullmatch(source_sha), "invalid source_sha"
    if args.expected_source_sha:
        assert SHA_RE.fullmatch(args.expected_source_sha), "invalid --expected-source-sha"
        assert source_sha == args.expected_source_sha, (
            f"source_sha mismatch: receipt={source_sha} expected={args.expected_source_sha}"
        )

    input_refs = receipt["input_evidence_refs"]
    assert isinstance(input_refs, list) and len(input_refs) == 1
    assert SLACK_REF_RE.fullmatch(str(input_refs[0])), "invalid Slack evidence ref"

    output_refs = receipt["output_evidence_refs"]
    assert isinstance(output_refs, list) and len(output_refs) >= 1
    expected_receipt_dir = contract["bridge"]["receipt_dir"].rstrip("/") + "/"
    assert str(output_refs[0]).startswith(expected_receipt_dir)
    assert str(output_refs[0]).endswith(f"/{workload_id}.json")

    assert receipt["execution_boundary"] in ALLOWED_BOUNDARIES
    assert receipt["authority_class"] in ALLOWED_AUTHORITY
    assert receipt["result"] in ALLOWED_RESULTS
    assert isinstance(receipt["elapsed_ms"], int) and receipt["elapsed_ms"] >= 0
    assert receipt["learning_signal"] == "slack_founder_command"

    if receipt["authority_class"] == "APPROVAL_REQUIRED":
        assert receipt["execution_boundary"] == "L5_BLOCKED"
        assert receipt["result"] == "APPROVAL_REQUIRED"
        assert receipt["state_after"] == "BLOCKED_AT_AUTHORITY_GATE"
    else:
        assert receipt["execution_boundary"] == "L0-L4_INTERNAL_FAIL_CLOSED"
        if receipt["result"] == "EXECUTED":
            assert receipt["state_after"] == "CANONICAL_AUTOPILOT_COMPLETED"
            assert receipt.get("runner_rc") == 0
            assert receipt.get("source_branch") == "main"
            assert receipt.get("origin_main_sha") == source_sha
            assert receipt.get("source_clean") is True
            assert receipt.get("source_canonical") is True
            assert len(output_refs) >= 2, "executed receipt must bind a runner log"
            assert str(output_refs[1]).startswith(expected_receipt_dir)
            assert str(output_refs[1]).endswith(f"/{workload_id}.runner.log")
            assert HASH_RE.fullmatch(str(receipt.get("runner_log_sha256", ""))), (
                "executed receipt must bind a SHA-256 runner log digest"
            )
        elif receipt["result"] == "FAILED":
            assert receipt["state_after"] in {"CANONICAL_AUTOPILOT_FAILED", "FAILED"}
        elif receipt["result"] == "DEGRADED":
            assert receipt["state_after"] == "DEGRADED_TIMEOUT"

    for metric in (
        "founder_minutes",
        "agent_minutes",
        "ai_cost",
        "tool_cost",
        "economic_delta",
    ):
        value = receipt[metric]
        assert value == UNKNOWN or isinstance(value, (int, float)), (
            f"{metric} must remain UNKNOWN_NOT_EVIDENCE_BACKED or numeric"
        )

    assert_no_secret_material(receipt)

    print("DEALIX_SLACK_FOUNDER_BRIDGE_RECEIPT=PASS")
    print(f"workload_id={workload_id}")
    print(f"source_sha={source_sha}")
    print(f"result={receipt['result']}")
    print(f"authority_class={receipt['authority_class']}")
    print(f"receipt={args.receipt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
