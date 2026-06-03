#!/usr/bin/env python3
"""Validate the internal Business OS catalog (40 systems + maps)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (  # noqa: E402
    BUSINESS_SYSTEM_FIELDS, CheckResult, EXPECTED_BUSINESS_SYSTEMS,
    core_system_ids, load_yaml, main,
)


def check() -> CheckResult:
    r = CheckResult("business_os_catalog")
    systems = load_yaml("data/business_os_catalog/systems.yaml")["systems"]
    cores = set(core_system_ids())
    sprint_ids = {s["id"] for s in load_yaml(
        "data/business_need_intelligence/specialized_sprint_library_50.yaml")["sprints"]}
    sys_ids = {s["id"] for s in systems}

    r.require(len(systems) >= EXPECTED_BUSINESS_SYSTEMS,
              f"expected >= {EXPECTED_BUSINESS_SYSTEMS} systems, got {len(systems)}")

    for s in systems:
        sid = s.get("id", "<no-id>")
        for field in BUSINESS_SYSTEM_FIELDS:
            if not s.get(field) and s.get(field) != 0:
                r.error(f"{sid}: missing/empty field '{field}'")
        if s.get("core_system_mapping") not in cores:
            r.error(f"{sid}: core_system_mapping '{s.get('core_system_mapping')}' not a core system")
        if s.get("entry_sprint") not in sprint_ids:
            r.error(f"{sid}: entry_sprint '{s.get('entry_sprint')}' not in sprint library")
        if not isinstance(s.get("starter_price"), (int, float)) or s.get("starter_price", 0) <= 0:
            r.error(f"{sid}: starter_price must be a positive number")
        if s.get("upsell_path") and s["upsell_path"] not in sys_ids and not isinstance(s["upsell_path"], str):
            r.error(f"{sid}: invalid upsell_path")

    # Map files must reference real system ids.
    pricing = load_yaml("data/business_os_catalog/system_pricing.yaml")["pricing"]
    complexity = load_yaml("data/business_os_catalog/delivery_complexity.yaml")["complexity"]
    sector_map = load_yaml("data/business_os_catalog/sector_to_system.yaml")["map"]
    core_map = load_yaml("data/business_os_catalog/core_to_specialized_system.yaml")["map"]

    r.require(len(pricing) == len(systems), "system_pricing must cover every system")
    r.require(len(complexity) == len(systems), "delivery_complexity must cover every system")
    for row in pricing:
        if row["system_id"] not in sys_ids:
            r.error(f"pricing references unknown system {row['system_id']}")
    for row in complexity:
        if row.get("level") not in ("low", "medium", "high"):
            r.error(f"complexity bad level for {row.get('system_id')}")
    for m in sector_map:
        for sid in m.get("systems", []):
            if sid not in sys_ids:
                r.error(f"sector_to_system references unknown system {sid}")
    mapped = {sid for m in core_map for sid in m.get("specialized_systems", [])}
    r.require(set(c["core_system"] for c in core_map) == cores,
              "core_to_specialized must cover all 5 core systems")
    r.require(mapped == sys_ids, "core_to_specialized must map every system exactly once")

    r.note(f"validated {len(systems)} business systems and 4 map files")
    return r


if __name__ == "__main__":
    main(check)
