#!/usr/bin/env python3
"""Validate Account Packs semantically: routing coherence + score re-derivation.

Schema shape is checked by check_schema_contracts.py; here we verify that the
intelligence is internally consistent and that no contact is invented.
"""
import _bootstrap  # noqa: F401
from dealix.lib import CheckResult, load_jsonl, load_yaml
from dealix import seeds
from dealix.scoring import verify_final


def main():
    r = CheckResult("account_pack_contract")
    packs = load_jsonl("data/account_intelligence/account_packs.jsonl")
    if not packs:
        r.fail("no account packs found")
        return r.finish()

    need_core = {n[0]: n[3] for n in seeds.NEEDS}
    sys_core = {s["id"]: s["core_system"] for s in seeds.iter_specialized_systems()}
    sprint_ids = {s["id"] for s in seeds.iter_sprints()}

    bad_route = bad_score = invented = bad_supp = 0
    for p in packs:
        need = p["primary_need"]
        if need not in need_core:
            r.fail(f"{p['company_name']}: unknown primary_need {need}"); bad_route += 1; continue
        if p["recommended_core_system"] != need_core[need]:
            bad_route += 1
            if bad_route <= 3:
                r.fail(f"{p['company_name']}: core {p['recommended_core_system']} != need's core {need_core[need]}")
        if sys_core.get(p["recommended_specialized_system"]) != p["recommended_core_system"]:
            bad_route += 1
            if bad_route <= 3:
                r.fail(f"{p['company_name']}: specialized system not under recommended core")
        if p["sector_specific_sprint"] not in sprint_ids:
            bad_route += 1
            if bad_route <= 3:
                r.fail(f"{p['company_name']}: sprint {p['sector_specific_sprint']} not in library")
        err = verify_final(p)
        if err:
            bad_score += 1
            if bad_score <= 3:
                r.fail(err)
        # contact ethics: demo channels must never contain a fabricated email
        if any("@" in ch for ch in p.get("public_contact_channels", [])):
            invented += 1
            if invented <= 3:
                r.fail(f"{p['company_name']}: public_contact_channels contains an email-like value")
        if p.get("suppressed") and "إيقاف" not in p.get("next_action", ""):
            bad_supp += 1
            if bad_supp <= 3:
                r.fail(f"{p['company_name']}: suppressed but next_action does not stop outreach")

    if not bad_route:
        r.ok(f"all {len(packs)} packs route sector->need->core->specialized->sprint consistently")
    if not bad_score:
        r.ok("all final_account_score values re-derive within tolerance")

    # cross-check against suppression list
    supp = {row["domain"].lower() for row in load_jsonl("data/suppression/do_not_contact.jsonl")}
    leaked = [p["company_name"] for p in packs if p.get("domain", "").lower() in supp and not p.get("suppressed")]
    if leaked:
        r.fail(f"suppressed domains not flagged: {leaked[:3]}")
    else:
        r.ok("suppression list correctly applied")

    return r.finish()


if __name__ == "__main__":
    main()
