#!/usr/bin/env python3
"""Validate the Business Need Intelligence engine: 25 needs, 20 sectors, 50 sprints."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    CheckResult, EXPECTED_NEEDS, EXPECTED_SECTORS, EXPECTED_SPRINTS,
    VALID_EVIDENCE_LEVELS, core_system_ids, load_yaml, main,
)


def check() -> CheckResult:
    r = CheckResult("need_intelligence")
    needs = load_yaml("data/business_need_intelligence/need_taxonomy_25.yaml")["needs"]
    sectors = load_yaml("data/business_need_intelligence/sector_need_matrix_20.yaml")["sectors"]
    signals = load_yaml("data/business_need_intelligence/signal_to_need_library.yaml")["signals"]
    sprints = load_yaml("data/business_need_intelligence/specialized_sprint_library_50.yaml")["sprints"]
    variants = load_yaml("data/business_need_intelligence/delivery_variants.yaml")["variants"]

    cores = set(core_system_ids())
    need_ids = {n["id"] for n in needs}
    variant_ids = {v["id"] for v in variants}

    r.require(len(needs) == EXPECTED_NEEDS, f"expected {EXPECTED_NEEDS} needs, got {len(needs)}")
    r.require(len(sectors) == EXPECTED_SECTORS, f"expected {EXPECTED_SECTORS} sectors, got {len(sectors)}")
    r.require(len(sprints) == EXPECTED_SPRINTS, f"expected {EXPECTED_SPRINTS} sprints, got {len(sprints)}")

    # every need mapped to a core system
    for n in needs:
        if n.get("core_system") not in cores:
            r.error(f"need {n.get('id')} not mapped to a core system")

    # every sector has top needs, all valid
    for s in sectors:
        tops = s.get("top_needs", [])
        if not tops:
            r.error(f"sector {s.get('id')} has no top_needs")
        for nid in tops:
            if nid not in need_ids:
                r.error(f"sector {s.get('id')} references unknown need {nid}")

    # every signal references a real need with a valid evidence level
    for sig in signals:
        if sig.get("need_id") not in need_ids:
            r.error(f"signal '{sig.get('signal_ar')}' references unknown need")
        if sig.get("evidence_level") not in VALID_EVIDENCE_LEVELS:
            r.error(f"signal '{sig.get('signal_ar')}' has bad evidence_level")

    # every sprint: need mapped, system core, delivery variant present
    for sp in sprints:
        if sp.get("need_id") not in need_ids:
            r.error(f"sprint {sp.get('id')} references unknown need")
        if sp.get("system_id") not in cores:
            r.error(f"sprint {sp.get('id')} system_id not a core system")
        if sp.get("delivery_variant") not in variant_ids:
            r.error(f"sprint {sp.get('id')} has no valid delivery_variant")

    r.note(f"{len(needs)} needs, {len(sectors)} sectors, {len(sprints)} sprints, "
           f"{len(signals)} signals, {len(variants)} delivery variants")
    return r


if __name__ == "__main__":
    main(check)
