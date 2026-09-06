#!/usr/bin/env python3
"""Verify Dealix Autonomous Company Machine V2 against the exact source under test.

Structural doctrine is authoritative. Historical source/WIP metadata in the contract is
retained as provenance and classified as current or superseded; it must never make a
new exact-head acceptance falsely PASS or FAIL merely because Git advanced.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "data" / "ops" / "dealix_autonomous_company_machine_v2.json"
EXPECTED_SYSTEMS = {
    "command_os",
    "revenue_os",
    "proof_os",
    "client_os",
    "delivery_os",
    "support_os",
    "finance_os",
    "data_os",
    "governance_os",
    "academy_os",
    "partner_os",
    "venture_os",
}
EXPECTED_AGENTS = {
    "dealix-pm",
    "dealix-sales",
    "dealix-delivery",
    "dealix-engineer",
    "dealix-content",
}
FAIL_CLOSED = {
    "customer_send",
    "public_publish",
    "paid_spend",
    "live_payment_or_refund",
    "contract_or_legal_commitment",
    "named_quote_commitment",
    "production_mutation",
    "dns_db_secret_mutation",
    "main_merge",
}
EXPECTED_FOUNDER_SURFACE = ["CASH", "DECISIONS", "RISKS", "APPROVALS", "NEXT_ACTION"]
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _git_head() -> str:
    proc = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    value = proc.stdout.strip().lower()
    if proc.returncode != 0 or not _SHA_RE.fullmatch(value):
        raise ValueError("unable_to_resolve_exact_source_sha")
    return value


def resolve_source_sha(explicit: str | None = None) -> str:
    """Resolve the exact source being verified without consulting contract history."""
    candidate = (explicit or os.environ.get("DEALIX_SOURCE_SHA") or "").strip().lower()
    if not candidate:
        return _git_head()
    if not _SHA_RE.fullmatch(candidate):
        raise ValueError("invalid_source_sha")
    return candidate


def _metadata_status(data: dict[str, Any], source_sha: str) -> dict[str, str]:
    contract_source = str(data.get("source_main_sha") or "").strip().lower()
    source_metadata = "CURRENT" if contract_source == source_sha else "SUPERSEDED"
    return {
        "contract_source_sha": contract_source or "UNKNOWN_NOT_EVIDENCE_BACKED",
        "source_metadata": source_metadata,
        "active_wip_metadata": "NON_AUTHORITATIVE_HISTORICAL_PROVENANCE",
    }


def verify(source_sha: str) -> tuple[list[str], dict[str, str]]:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    errors: list[str] = []

    if data.get("schema_version") != "2.0":
        errors.append("schema_version")
    if data.get("portfolio_objective") != "CASH_READY_AUTONOMOUS_DEALIX_COMPANY":
        errors.append("portfolio_objective")
    if (data.get("canonical_scheduler") or {}).get("parallel_company_scheduler_allowed") is not False:
        errors.append("parallel_scheduler_must_be_false")
    if set(data.get("agent_roster") or {}) != EXPECTED_AGENTS:
        errors.append("agent_roster")

    systems = data.get("systems") or []
    ids = [row.get("id") for row in systems if isinstance(row, dict)]
    if len(ids) != len(set(ids)):
        errors.append("duplicate_system_id")
    if set(ids) != EXPECTED_SYSTEMS:
        errors.append("system_set")
    for row in systems:
        if not isinstance(row, dict):
            errors.append("system_not_object")
            continue
        sid = row.get("id")
        for key in ("phase", "owner", "state_machine", "workloads", "kpis"):
            if not row.get(key):
                errors.append(f"system_missing_{key}:{sid}")
        if len(row.get("state_machine") or []) < 5:
            errors.append(f"state_machine_too_small:{sid}")

    effects = data.get("external_effect_defaults") or {}
    for key in FAIL_CLOSED:
        if effects.get(key) is not False:
            errors.append(f"external_effect_not_fail_closed:{key}")

    firewall = set(data.get("truth_firewall") or [])
    for rule in {
        "research!=relationship",
        "public_contact_data!=consent",
        "proposal!=revenue",
        "quote!=invoice",
        "invoice!=payment",
        "synthetic!=customer_proof",
    }:
        if rule not in firewall:
            errors.append(f"truth_firewall_missing:{rule}")

    dev = data.get("development_factory") or {}
    if dev.get("max_unverified_prs_per_lane") != 1:
        errors.append("development_wip")
    if dev.get("random_feature_factory_allowed") is not False:
        errors.append("random_feature_factory")
    if (dev.get("sequence") or [])[-4:] != [
        "DRAFT_PR",
        "EXACT_HEAD_SOVEREIGN_VERIFICATION",
        "READY_DECISION",
        "LEARNING",
    ]:
        errors.append("development_factory_tail")

    learning = data.get("learning_factory") or {}
    if learning.get("may_change_authority") is not False:
        errors.append("learning_authority")
    if learning.get("may_change_legal_or_commercial_truth") is not False:
        errors.append("learning_governed_truth")
    if learning.get("requires_measurable_before_after") is not True:
        errors.append("learning_measurement")

    observability = data.get("observability") or {}
    if observability.get("new_observability_database_allowed_by_default") is not False:
        errors.append("observability_db_duplication")
    if observability.get("capture_prompt_or_customer_content_by_default") is not False:
        errors.append("sensitive_observability_default")

    if (data.get("runtime_controls") or {}).get("kill_switches_may_only_reduce_authority") is not True:
        errors.append("kill_switch_authority_ceiling")
    if data.get("founder_surface") != EXPECTED_FOUNDER_SURFACE:
        errors.append("founder_surface")

    # `active_wip` and `source_main_sha` are historical receipt metadata, not
    # timeless architecture doctrine. Preserve their shape/provenance but never
    # require old issue IDs or an old SHA to accept a newer exact source.
    active_wip = data.get("active_wip")
    if active_wip is not None and not isinstance(active_wip, dict):
        errors.append("active_wip_metadata_not_object")

    return errors, _metadata_status(data, source_sha)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-sha",
        help="Exact 40-hex source SHA. Defaults to DEALIX_SOURCE_SHA or git HEAD.",
    )
    args = parser.parse_args(argv)

    try:
        source_sha = resolve_source_sha(args.source_sha)
    except ValueError as exc:
        print("DEALIX_AUTONOMOUS_COMPANY_MACHINE_V2=FAIL")
        print(f"- {exc}")
        return 2

    errors, metadata = verify(source_sha)
    if errors:
        print("DEALIX_AUTONOMOUS_COMPANY_MACHINE_V2=FAIL")
        print(f"source_sha={source_sha}")
        for error in errors:
            print(f"- {error}")
        return 1

    print("DEALIX_AUTONOMOUS_COMPANY_MACHINE_V2=PASS")
    print(f"source_sha={source_sha}")
    print(f"contract_source_sha={metadata['contract_source_sha']}")
    print(f"source_metadata={metadata['source_metadata']}")
    print(f"active_wip_metadata={metadata['active_wip_metadata']}")
    print("systems=12")
    print("agents=5")
    print("portfolio_objective=CASH_READY_AUTONOMOUS_DEALIX_COMPANY")
    print("external_effects=FAIL_CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
