#!/usr/bin/env python3
"""Validate every data file against its JSON-Schema contract.

Uses jsonschema if installed, else the dependency-free validator in dealix.lib.
"""
import _bootstrap  # noqa: F401
from dealix.lib import ROOT, CheckResult, load_json, load_jsonl, load_yaml, validate

# (data_path, schema_name, yaml_list_key or None for jsonl)
CONTRACTS = [
    ("data/business_os_catalog/systems.yaml", "business_system", "systems"),
    ("data/business_need_intelligence/need_taxonomy_25.yaml", "need_taxonomy", "needs"),
    ("data/business_need_intelligence/specialized_sprint_library_50.yaml", "specialized_sprint", "sprints"),
    ("data/business_need_intelligence/sector_need_matrix_20.yaml", "sector_need_map", "sectors"),
    ("data/business_need_intelligence/need_to_system_router.yaml", "need_to_system_route", "routes"),
    ("data/account_intelligence/account_packs.jsonl", "account_intelligence_pack", None),
    ("data/contacts/contact_discovery.jsonl", "contact_discovery", None),
    ("data/outreach/email_drafts.jsonl", "email_draft", None),
    ("data/acquisition/call_briefs.jsonl", "call_brief", None),
    ("data/proposals/mini_proposals.jsonl", "mini_proposal", None),
    ("data/delivery/pipelines.jsonl", "delivery_pipeline", None),
    ("data/delivery/acceptance_gates.jsonl", "delivery_acceptance_gate", None),
    ("data/delivery/weekly_value_reports.jsonl", "weekly_value_report", None),
    ("data/finance/cash_priority_scores.jsonl", "cash_priority_score", None),
]


def main():
    r = CheckResult("schema_contracts")
    for data_path, schema_name, list_key in CONTRACTS:
        dpath = ROOT / data_path
        spath = ROOT / "schemas" / f"{schema_name}.schema.json"
        if not spath.exists():
            r.fail(f"schema missing: {spath.name}")
            continue
        if not dpath.exists():
            r.fail(f"data missing: {data_path}")
            continue
        schema = load_json(spath)
        if list_key is None:
            rows = load_jsonl(data_path)
        else:
            doc = load_yaml(data_path)
            rows = doc.get(list_key, []) if isinstance(doc, dict) else []
        errs = 0
        for i, row in enumerate(rows):
            for e in validate(row, schema):
                if errs < 5:  # cap noise
                    r.fail(f"{data_path}[{i}] {e}")
                errs += 1
        if errs:
            r.fail(f"{data_path}: {errs} record(s) failed {schema_name}")
        else:
            r.ok(f"{data_path}: {len(rows)} records valid against {schema_name}")
    return r.finish()


if __name__ == "__main__":
    main()
