#!/usr/bin/env python3
"""Validate the nightly Account Pack output contract (27 fields + scoring)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    ACCOUNT_PACK_FIELDS, CheckResult, VALID_CONTACT_CONFIDENCE,
    core_system_ids, load_jsonl, load_yaml, main,
)


def check() -> CheckResult:
    r = CheckResult("account_pack_contract")
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    if not packs:
        r.error("no account packs found")
        return r

    cores = set(core_system_ids())
    need_ids = {n["id"] for n in load_yaml(
        "data/business_need_intelligence/need_taxonomy_25.yaml")["needs"]}
    sprint_ids = {s["id"] for s in load_yaml(
        "data/business_need_intelligence/specialized_sprint_library_50.yaml")["sprints"]}
    sys_ids = {s["id"] for s in load_yaml(
        "data/business_os_catalog/systems.yaml")["systems"]}

    score_fields = ["cash_priority_score", "need_fit_score", "account_score", "final_account_score"]
    invented = 0
    for i, p in enumerate(packs):
        for f in ACCOUNT_PACK_FIELDS:
            if f not in p:
                r.error(f"pack[{i}] missing field '{f}'")
        for f in score_fields:
            v = p.get(f)
            if not isinstance(v, (int, float)) or not (0 <= v <= 100):
                r.error(f"pack[{i}] {f}={v} out of range 0..100")
        if p.get("primary_need") not in need_ids:
            r.error(f"pack[{i}] primary_need not in taxonomy")
        if p.get("recommended_core_system") not in cores:
            r.error(f"pack[{i}] recommended_core_system invalid")
        if p.get("recommended_specialized_system") not in sys_ids:
            r.error(f"pack[{i}] recommended_specialized_system not in catalog")
        if p.get("sector_specific_sprint") not in sprint_ids:
            r.error(f"pack[{i}] sector_specific_sprint not in sprint library")
        if p.get("contact_confidence") not in VALID_CONTACT_CONFIDENCE:
            r.error(f"pack[{i}] contact_confidence invalid")
        # no invented contacts: sample records must not assert a verified contact
        if p.get("record_type") == "sample" and p.get("contact_confidence") not in ("missing", "unknown"):
            invented += 1
        if p.get("record_type") not in ("sample", "live"):
            r.error(f"pack[{i}] record_type must be sample|live")
        if not p.get("source"):
            r.error(f"pack[{i}] missing source (provenance)")
        # recomputed final score must match the documented weighting
        expected = round(0.40 * p.get("account_score", 0) + 0.35 * p.get("need_fit_score", 0)
                         + 0.25 * p.get("cash_priority_score", 0))
        if p.get("final_account_score") != expected:
            r.error(f"pack[{i}] final_account_score {p.get('final_account_score')} != formula {expected}")

    r.require(invented == 0, f"{invented} sample packs assert a contact without a verified source")
    r.note(f"validated {len(packs)} account packs against the 27-field contract")
    return r


if __name__ == "__main__":
    main(check)
