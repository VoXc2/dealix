#!/usr/bin/env python3
"""Validate the Business OS Catalog: 40 internal systems, 8 per core, mapped."""
import _bootstrap  # noqa: F401
from dealix.lib import CheckResult, load_yaml
from dealix import seeds

PRICE = seeds.COMPLEXITY_PRICE_SAR


def main():
    r = CheckResult("business_os_catalog")
    systems = load_yaml("data/business_os_catalog/systems.yaml")["systems"]

    if len(systems) == 40:
        r.ok("exactly 40 internal systems")
    else:
        r.fail(f"expected 40 systems, found {len(systems)}")

    per_core = {c: 0 for c in seeds.CORE_SYSTEM_IDS}
    ids = set()
    for s in systems:
        if s["core_system"] not in seeds.CORE_SYSTEM_IDS:
            r.fail(f"{s['id']}: unknown core_system {s['core_system']}")
        else:
            per_core[s["core_system"]] += 1
        if s["id"] in ids:
            r.fail(f"duplicate system id: {s['id']}")
        ids.add(s["id"])
        if PRICE.get(s["complexity"]) != s["starter_price_sar"]:
            r.fail(f"{s['id']}: price {s['starter_price_sar']} != {PRICE.get(s['complexity'])} for {s['complexity']}")

    for core, n in per_core.items():
        if n == 8:
            r.ok(f"{core}: 8 specialized systems")
        else:
            r.fail(f"{core}: expected 8 specialized systems, found {n}")

    # mapping coverage
    core_map = load_yaml("data/business_os_catalog/core_to_specialized_system.yaml")["map"]
    mapped = {sid for row in core_map for sid in row["specialized_systems"]}
    missing = ids - mapped
    if missing:
        r.fail(f"systems missing from core->specialized map: {sorted(missing)}")
    else:
        r.ok("every specialized system is mapped to exactly one core")

    # each system internal_only (never public)
    if all(s.get("internal_only") for s in systems):
        r.ok("all 40 systems flagged internal_only (not publicly listed)")
    else:
        r.fail("some systems are not flagged internal_only")

    return r.finish()


if __name__ == "__main__":
    main()
