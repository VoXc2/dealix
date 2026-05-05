#!/usr/bin/env python3
"""Verify the v10 Reference Library YAML.

Run:
    python scripts/verify_reference_library_70.py
    python scripts/verify_reference_library_70.py --json

Exit 0 on pass, 1 on fail.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
YAML_PATH = REPO_ROOT / "docs" / "v10" / "REFERENCE_LIBRARY_70.yaml"

REQUIRED_KEYS = {
    "id", "name", "repo", "category", "dealix_value",
    "patterns_to_adapt", "modules_impacted", "tier", "priority",
    "status", "risks", "safety_concerns", "cost_concerns",
    "license_to_verify", "integration_complexity",
    "founder_decision_required", "notes",
}

VALID_TIERS = {"inspiration_only", "native_pattern", "optional_adapter", "real_dependency"}
VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}
VALID_STATUSES = {"reviewed", "selected", "shipped", "deferred", "rejected"}

VALID_CATEGORIES = {
    "ai_workforce", "workflow_durability", "crm_revops",
    "customer_inbox", "growth_analytics", "knowledge_rag",
    "llm_gateway", "observability", "safety_evals",
    "platform_auth", "designops_artifacts", "founder_command_center",
}

# Tools with these tokens in their name/dealix_value/patterns must default-block
SCRAPING_KEYWORDS = {"scrape", "scraping"}
COLD_OUTREACH_KEYWORDS = {"cold whatsapp", "cold email", "linkedin automation"}


def load_yaml() -> dict:
    if not YAML_PATH.exists():
        raise FileNotFoundError(f"missing: {YAML_PATH}")
    with YAML_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def check(data: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    projects = data.get("projects") or []
    total_count = len(projects)

    if total_count < 70:
        errors.append(f"need >= 70 projects, got {total_count}")

    # uniqueness
    ids = [p.get("id") for p in projects]
    dup_ids = [i for i, c in Counter(ids).items() if c > 1]
    if dup_ids:
        errors.append(f"duplicate ids: {dup_ids}")

    names = [p.get("name") for p in projects]
    dup_names = [n for n, c in Counter(names).items() if c > 1]
    if dup_names:
        errors.append(f"duplicate names: {dup_names}")

    # required keys + valid enums
    for p in projects:
        pid = p.get("id", "<no-id>")
        missing = REQUIRED_KEYS - set(p.keys())
        if missing:
            errors.append(f"{pid}: missing keys {missing}")
            continue
        if p["tier"] not in VALID_TIERS:
            errors.append(f"{pid}: invalid tier {p['tier']!r}")
        if p["priority"] not in VALID_PRIORITIES:
            errors.append(f"{pid}: invalid priority {p['priority']!r}")
        if p["status"] not in VALID_STATUSES:
            errors.append(f"{pid}: invalid status {p['status']!r}")
        if p["category"] not in VALID_CATEGORIES:
            errors.append(
                f"{pid}: invalid category {p['category']!r} "
                f"(valid: {sorted(VALID_CATEGORIES)})"
            )

        # safety policy: real_dependency without founder decision is forbidden
        if p["tier"] == "real_dependency" and not p.get("founder_decision_required"):
            errors.append(
                f"{pid}: tier=real_dependency requires founder_decision_required=true"
            )

        # safety policy: any tool whose dealix_value/patterns mention scraping/
        # cold-outreach/linkedin-automation must NOT default to real_dependency
        haystack = " ".join([
            str(p.get("dealix_value", "")),
            " ".join(p.get("patterns_to_adapt") or []),
        ]).lower()
        if any(k in haystack for k in SCRAPING_KEYWORDS) and p["tier"] == "real_dependency":
            errors.append(
                f"{pid}: scraping-capable tool cannot default to real_dependency"
            )

        if "linkedin automation" in haystack and p["tier"] == "real_dependency":
            errors.append(
                f"{pid}: linkedin automation tool cannot default to real_dependency"
            )

    # by-category counts
    by_cat = Counter(p.get("category") for p in projects)
    by_tier = Counter(p.get("tier") for p in projects)
    by_priority = Counter(p.get("priority") for p in projects)
    by_status = Counter(p.get("status") for p in projects)

    # top-10 P0 picks
    p0_picks = [
        p for p in projects
        if p.get("priority") == "P0" and p.get("status") in {"shipped", "selected"}
    ]
    if len(p0_picks) < 5:
        warnings.append(f"only {len(p0_picks)} P0 picks selected/shipped (expected ~10)")

    return {
        "total_count": total_count,
        "errors": errors,
        "warnings": warnings,
        "by_category": dict(by_cat),
        "by_tier": dict(by_tier),
        "by_priority": dict(by_priority),
        "by_status": dict(by_status),
        "p0_picks": [p["id"] for p in p0_picks],
        "ok": len(errors) == 0,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Verify v10 reference library YAML.")
    p.add_argument("--json", action="store_true", help="emit JSON")
    args = p.parse_args(argv)

    try:
        data = load_yaml()
    except Exception as exc:  # noqa: BLE001
        msg = f"YAML load failed: {exc}"
        if args.json:
            print(json.dumps({"ok": False, "error": msg}, indent=2))
        else:
            print(f"FAIL: {msg}", file=sys.stderr)
        return 1

    report = check(data)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Total projects: {report['total_count']}")
        print(f"By category: {report['by_category']}")
        print(f"By tier: {report['by_tier']}")
        print(f"By priority: {report['by_priority']}")
        print(f"By status: {report['by_status']}")
        print(f"P0 picks ({len(report['p0_picks'])}): {report['p0_picks']}")
        if report["warnings"]:
            print("\nWarnings:")
            for w in report["warnings"]:
                print(f"  ⚠️  {w}")
        if report["errors"]:
            print("\nErrors:")
            for e in report["errors"]:
                print(f"  ❌ {e}")
            print(f"\nFAIL ({len(report['errors'])} errors)")
        else:
            print("\n✅ PASS — verifier clean")

    return 0 if report["ok"] else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
