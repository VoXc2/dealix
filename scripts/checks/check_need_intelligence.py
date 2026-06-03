#!/usr/bin/env python3
"""Validate Business Need Intelligence: 25 needs, 20 sectors, 50 sprints, routing."""
import _bootstrap  # noqa: F401
from dealix.lib import CheckResult, load_yaml
from dealix import seeds


def main():
    r = CheckResult("need_intelligence")
    needs = load_yaml("data/business_need_intelligence/need_taxonomy_25.yaml")["needs"]
    sectors = load_yaml("data/business_need_intelligence/sector_need_matrix_20.yaml")["sectors"]
    sprints = load_yaml("data/business_need_intelligence/specialized_sprint_library_50.yaml")["sprints"]
    routes = load_yaml("data/business_need_intelligence/need_to_system_router.yaml")["routes"]

    need_ids = {n["id"] for n in needs}
    need_core = {n["id"]: n["core_system"] for n in needs}

    r.ok("25 needs") if len(needs) == 25 else r.fail(f"expected 25 needs, found {len(needs)}")
    r.ok("20 sector maps") if len(sectors) == 20 else r.fail(f"expected 20 sectors, found {len(sectors)}")
    r.ok("50 specialized sprints") if len(sprints) == 50 else r.fail(f"expected 50 sprints, found {len(sprints)}")

    for n in needs:
        if n["core_system"] not in seeds.CORE_SYSTEM_IDS:
            r.fail(f"need {n['id']}: invalid core_system {n['core_system']}")

    for sec in sectors:
        for nid in sec["needs"]:
            if nid not in need_ids:
                r.fail(f"sector {sec['sector']}: references unknown need {nid}")

    for sp in sprints:
        if sp["need_id"] not in need_ids:
            r.fail(f"sprint {sp['id']}: unknown need {sp['need_id']}")
        elif sp["core_system"] != need_core[sp["need_id"]]:
            r.fail(f"sprint {sp['id']}: core {sp['core_system']} != need's core {need_core[sp['need_id']]}")
        if len(sp.get("required_inputs", [])) < 2:
            r.fail(f"sprint {sp['id']}: needs >= 2 required_inputs")
        if len(sp.get("acceptance_criteria", [])) < 2:
            r.fail(f"sprint {sp['id']}: needs >= 2 acceptance_criteria")
        if len(sp.get("deliverables", [])) < 3:
            r.fail(f"sprint {sp['id']}: needs >= 3 deliverables")
    if not r.errors:
        r.ok("every sprint has valid need, matching core, inputs, criteria, deliverables")

    routed = {rt["need_id"] for rt in routes}
    if routed >= need_ids:
        r.ok("every need is routed to a core + specialized systems")
    else:
        r.fail(f"needs missing from router: {sorted(need_ids - routed)}")
    for rt in routes:
        if rt["core_system"] != need_core.get(rt["need_id"]):
            r.fail(f"route {rt['need_id']}: core mismatch")
        if not rt["specialized_systems"]:
            r.fail(f"route {rt['need_id']}: no specialized systems")

    return r.finish()


if __name__ == "__main__":
    main()
