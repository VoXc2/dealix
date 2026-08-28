#!/usr/bin/env python3
"""Regression proof that Founder/personal data cannot pollute Dealix company truth."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts/generate_morning_revenue_command.py"
UNKNOWN = "UNKNOWN_NOT_EVIDENCE_BACKED"


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"MORNING_REVENUE_AUTHORITY_SCOPE=FAIL reason={message}")
        raise SystemExit(1)


def load_generator():
    spec = importlib.util.spec_from_file_location("dealix_morning_revenue_command", GENERATOR)
    require(spec is not None and spec.loader is not None, "generator_import_spec_failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    module = load_generator()

    with tempfile.TemporaryDirectory(prefix="dealix-morning-authority-") as tmp:
        root = Path(tmp)

        write(
            root / "founder_personal.json",
            {
                "schema": "dealix.founder.personal.v1",
                "scope": "founder_personal",
                "pipeline": {
                    "real_contacts": 99,
                    "verified_relationships": 77,
                    "diagnostics_active": 66,
                },
                "money": {"verified_revenue_sar": 999999, "verified_paid_pilots": 55},
            },
        )
        write(
            root / "dealix_company_truth.json",
            {
                "schema": "dealix.company-commercial-truth.v1",
                "scope": "dealix_company",
                "money": {"verified_revenue_sar": 0, "verified_paid_pilots": 0},
                "pipeline": {
                    "real_interactions": 1,
                    "verified_relationships": 0,
                    "diagnostics_active": 0,
                },
            },
        )

        result = module.build(root)
        require(result["money"]["verified_revenue_sar"] == 0, "founder_revenue_polluted_company_truth")
        require(result["money"]["verified_paid_pilots"] == 0, "founder_paid_pilots_polluted_company_truth")
        require(result["pipeline"]["verified_relationships"] == 0, "founder_relationships_polluted_company_truth")
        require(result["pipeline"]["diagnostics_active"] == 0, "founder_diagnostics_polluted_company_truth")
        source = result["evidence_sources"]["verified_relationships"]
        require(isinstance(source, dict), "relationship_source_metadata_missing")
        require(source.get("schema") == "dealix.company-commercial-truth.v1", "relationship_source_schema_wrong")
        require(source.get("scope") == "dealix_company", "relationship_source_scope_wrong")
        require(source.get("key") == "verified_relationships", "relationship_source_key_wrong")
        require(bool(source.get("path")), "relationship_source_path_missing")

    with tempfile.TemporaryDirectory(prefix="dealix-morning-authority-unknown-") as tmp:
        root = Path(tmp)
        write(
            root / "founder_only.json",
            {
                "schema": "dealix.founder.personal.v1",
                "scope": "founder_personal",
                "pipeline": {"verified_relationships": 12},
                "money": {"verified_revenue_sar": 500000},
            },
        )
        result = module.build(root)
        require(result["money"]["verified_revenue_sar"] == UNKNOWN, "unscoped_company_revenue_must_be_unknown")
        require(result["pipeline"]["verified_relationships"] == UNKNOWN, "unscoped_relationships_must_be_unknown")
        require(result["evidence_sources"]["verified_relationships"] is None, "unknown_relationship_must_have_no_source")

    text = GENERATOR.read_text(encoding="utf-8")
    require('"real_contacts"' not in text, "generic_real_contacts_alias_reintroduced")
    require("find_key(" not in text, "generic_recursive_key_search_reintroduced")
    require("scope" in text and "schema" in text, "authority_metadata_missing")

    print("MORNING_REVENUE_AUTHORITY_SCOPE=PASS")
    print("FOUNDER_PERSONAL_CANNOT_PROMOTE_DEALIX_TRUTH=PASS")
    print("SOURCE_METADATA_SCHEMA_SCOPE_PATH_KEY=PASS")
    print("UNKNOWN_FAIL_CLOSED=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
