#!/usr/bin/env python3
"""Validate every JSON schema is well-formed and that data instances conform."""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    CheckResult, load_json, load_jsonl, load_yaml, main, rel, validate_instance,
)


def _yaml_list(path, key):
    return load_yaml(path)[key]


# schema name -> callable returning a list of instances to validate
INSTANCE_SOURCES = {
    "account_intelligence_pack": lambda: load_jsonl("data/account_intelligence/account_packs.jsonl"),
    "business_system": lambda: _yaml_list("data/business_os_catalog/systems.yaml", "systems"),
    "sector_system_map": lambda: _yaml_list("data/business_os_catalog/sector_to_system.yaml", "map"),
    "need_taxonomy": lambda: _yaml_list("data/business_need_intelligence/need_taxonomy_25.yaml", "needs"),
    "signal_to_need": lambda: _yaml_list("data/business_need_intelligence/signal_to_need_library.yaml", "signals"),
    "delivery_variant": lambda: _yaml_list("data/business_need_intelligence/delivery_variants.yaml", "variants"),
    "email_draft": lambda: load_jsonl("data/outreach/email_drafts.jsonl"),
    "client_need_card": lambda: load_jsonl("data/acquisition/client_need_cards.jsonl"),
    "company_intelligence_pack": lambda: load_jsonl("data/acquisition/company_intelligence_packs.jsonl"),
    "contact_target": lambda: load_jsonl("data/acquisition/contact_targets.jsonl"),
    "call_brief": lambda: load_jsonl("data/acquisition/call_briefs.jsonl"),
    "follow_up_sequence": lambda: load_jsonl("data/acquisition/follow_up_sequences.jsonl"),
    "objection_response": lambda: load_jsonl("data/acquisition/objection_responses.jsonl"),
    "contact_discovery": lambda: load_jsonl("data/contacts/contact_discovery.jsonl"),
    "contact_channel": lambda: load_jsonl("data/contacts/contact_channels.jsonl"),
    "mini_proposal": lambda: load_jsonl("data/proposals/mini_proposals.jsonl"),
    "delivery_pipeline": lambda: load_jsonl("data/delivery/pipelines.jsonl"),
    "delivery_task": lambda: load_jsonl("data/delivery/tasks.jsonl"),
    "weekly_value_report": lambda: load_jsonl("data/delivery/weekly_value_reports.jsonl"),
    "delivery_acceptance_gate": lambda: load_jsonl("data/delivery/acceptance_gates.jsonl"),
    "cash_priority_score": lambda: load_jsonl("data/finance/cash_priority_scores.jsonl"),
}


def check() -> CheckResult:
    r = CheckResult("schema_contracts")
    schema_files = sorted(glob.glob(str(rel("schemas/*.schema.json"))))
    if not schema_files:
        r.error("no schemas found under schemas/")
        return r

    validated_instances = 0
    for path in schema_files:
        name = os.path.basename(path).replace(".schema.json", "")
        try:
            schema = load_json(os.path.relpath(path, rel(".")))
        except json.JSONDecodeError as exc:
            r.error(f"{name}: invalid JSON ({exc})")
            continue
        for key in ("$schema", "title", "type"):
            if key not in schema:
                r.error(f"{name}: schema missing '{key}'")
        if schema.get("type") == "object" and "properties" not in schema:
            r.warn(f"{name}: object schema without properties")

        source = INSTANCE_SOURCES.get(name)
        if source is None:
            continue
        try:
            instances = source()
        except FileNotFoundError as exc:
            r.error(f"{name}: data source missing ({exc})")
            continue
        for i, inst in enumerate(instances):
            errs = validate_instance(inst, schema, f"{name}[{i}]")
            for e in errs[:3]:
                r.error(e)
            validated_instances += 1

    r.note(f"validated {len(schema_files)} schemas and {validated_instances} data instances")
    return r


if __name__ == "__main__":
    main(check)
