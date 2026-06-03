"""Generate the Business OS Catalog data (40 internal systems) from seeds."""
from __future__ import annotations

import sys

from . import seeds
from .lib import dump_yaml


def build():
    systems = list(seeds.iter_specialized_systems())

    # systems.yaml
    dump_yaml("data/business_os_catalog/systems.yaml", {"systems": systems})

    # core_to_specialized_system.yaml
    core_map = {core: [] for core in seeds.CORE_SYSTEM_IDS}
    for sysrec in systems:
        core_map[sysrec["core_system"]].append(sysrec["id"])
    dump_yaml(
        "data/business_os_catalog/core_to_specialized_system.yaml",
        {
            "map": [
                {"core_system": core, "specialized_systems": specs}
                for core, specs in core_map.items()
            ]
        },
    )

    # sector_to_system.yaml (sector -> core systems via its needs)
    smap = seeds.sector_need_map()
    sector_rows = []
    for sid, sector_ar in seeds.SECTORS:
        cores = []
        for need_id in smap[sid]:
            core = seeds.need_by_id(need_id)["core_system"]
            if core not in cores:
                cores.append(core)
        sector_rows.append({"sector": sid, "sector_name_ar": sector_ar, "core_systems": cores})
    dump_yaml("data/business_os_catalog/sector_to_system.yaml", {"sectors": sector_rows})

    # system_pricing.yaml
    dump_yaml(
        "data/business_os_catalog/system_pricing.yaml",
        {
            "currency": "SAR",
            "by_complexity": seeds.COMPLEXITY_PRICE_SAR,
            "systems": [
                {"id": s["id"], "starter_price_sar": s["starter_price_sar"]} for s in systems
            ],
        },
    )

    # delivery_complexity.yaml
    dump_yaml(
        "data/business_os_catalog/delivery_complexity.yaml",
        {
            "systems": [
                {
                    "id": s["id"],
                    "complexity": s["complexity"],
                    "duration_days": seeds.COMPLEXITY_DURATION_DAYS[s["complexity"]],
                }
                for s in systems
            ]
        },
    )
    return len(systems)


def main():
    n = build()
    print(f"Business OS Catalog generated: {n} internal systems across {len(seeds.CORE_SYSTEM_IDS)} core systems.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
