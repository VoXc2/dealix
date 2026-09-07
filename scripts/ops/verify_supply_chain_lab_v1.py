#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "config" / "oss" / "supply_chain_lab_v1.json"

REQUIRED_COMPONENTS = {"osv-scanner", "syft", "grype", "github-artifact-attestations"}
REQUIRED_CLASSIFICATIONS = {
    "scanner_execution_failure",
    "findings_present",
    "no_findings_observed",
    "tool_unavailable",
    "unknown_not_evidence_backed",
}


def fail(message: str) -> None:
    raise SystemExit(f"DEALIX_SUPPLY_CHAIN_LAB_V1=FAIL: {message}")


def main() -> None:
    if not MANIFEST.is_file():
        fail("manifest missing")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        fail("schema_version must be 1")

    authority = data.get("authority") or {}
    must_true = {
        "isolated_lab_only",
        "promotion_requires_benchmark",
        "reject_duplicate_by_default",
    }
    must_false = {
        "production_runtime",
        "production_mutation",
        "deployment_authority",
        "network_target_scanning",
        "customer_effects",
    }
    for key in must_true:
        if authority.get(key) is not True:
            fail(f"{key} must remain true")
    for key in must_false:
        if authority.get(key) is not False:
            fail(f"{key} must remain false")

    components = data.get("components") or []
    ids = {component.get("id") for component in components if isinstance(component, dict)}
    if ids != REQUIRED_COMPONENTS:
        fail(f"component drift: {sorted(ids)}")

    for component in components:
        for field in (
            "id",
            "source",
            "version",
            "license",
            "classification",
            "purpose",
            "install_surface",
            "verification",
            "promotion_gate",
        ):
            if not component.get(field):
                fail(f"{component.get('id')} missing {field}")

    classifications = data.get("classification") or {}
    if set(classifications) != REQUIRED_CLASSIFICATIONS:
        fail(f"classification drift: {sorted(classifications)}")
    if not all(isinstance(classifications[key], str) and classifications[key].strip() for key in REQUIRED_CLASSIFICATIONS):
        fail("classification definitions must be non-empty strings")

    rules = "\n".join(str(rule) for rule in (data.get("rules") or [])).lower()
    for phrase in (
        "not automatically exploitable",
        "one canonical risk record",
        "never self-authorize dependency mutation",
        "not production green authority",
        "third-party system",
        "secrets",
        "pii",
    ):
        if phrase not in rules:
            fail(f"missing truth rule: {phrase}")

    contract = data.get("evidence_contract") or {}
    if contract.get("production_mutation") is not False:
        fail("evidence runner may not mutate Production")
    if contract.get("customer_effects") is not False:
        fail("evidence runner may not create customer effects")

    required_fields = set(contract.get("required_fields") or [])
    for field in (
        "source_sha",
        "tool",
        "tool_version",
        "target_kind",
        "target_identity",
        "started_at",
        "completed_at",
        "exit_code",
        "result_digest",
        "production_mutation",
        "customer_effects",
    ):
        if field not in required_fields:
            fail(f"evidence contract missing {field}")

    print("DEALIX_SUPPLY_CHAIN_LAB_V1=PASS")
    print("production_mutation=false")
    print("customer_effects=false")
    print("auto_remediation=false")
    print("scanner_finding_is_not_exploitability=true")
    print("duplicate_scanner_findings_dedupe_to_one_risk=true")


if __name__ == "__main__":
    main()
