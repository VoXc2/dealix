#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "config" / "oss" / "supply_chain_lab_v1.json"

REQUIRED_COMPONENTS = {"osv-scanner", "syft", "grype", "github-artifact-attestations"}


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

    contract = data.get("evidence_contract") or {}
    if contract.get("production_mutation") is not False:
        fail("evidence runner may not mutate Production")
    if contract.get("customer_effects") is not False:
        fail("evidence runner may not create customer effects")

    print("DEALIX_SUPPLY_CHAIN_LAB_V1=PASS")
    print("production_mutation=false")
    print("customer_effects=false")
    print("auto_remediation=false")


if __name__ == "__main__":
    main()
