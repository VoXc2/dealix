#!/usr/bin/env python3
"""
Dealix Check: Delivery Capacity Planning

Never sell more than you can deliver. If utilization exceeds the scale-block
threshold (80%), do not raise sending — focus on delivery or delegate.
Above the hard threshold (100%) the pipeline is over-committed (FAIL).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Reporter, load_json  # noqa: E402

REQUIRED_SYSTEM_FIELDS = [
    "estimated_delivery_hours", "complexity", "required_inputs_difficulty",
    "revision_risk", "founder_involvement", "can_delegate", "gross_margin_pct",
]


def run() -> bool:
    r = Reporter("DEALIX CHECK — DELIVERY CAPACITY PLANNING")

    c = load_json("company_os/delivery/capacity.json")
    if c is None:
        r.fail("capacity.json missing or invalid")
        return r.render()

    total = c.get("total_capacity_hours_per_week", 0)
    committed = c.get("committed_hours_per_week", 0)
    scale_block = c.get("scale_block_threshold_pct", 80)
    hard_block = c.get("hard_block_threshold_pct", 100)

    r.check(total > 0, f"weekly capacity declared: {total}h",
            "total_capacity_hours_per_week must be > 0")

    util = (committed / total * 100) if total else 0
    print_util = round(util, 1)

    if util > hard_block:
        r.fail(f"utilization {print_util}% over hard block {hard_block}% — over-committed")
    elif util > scale_block:
        r.warn(f"utilization {print_util}% over scale-block {scale_block}% — DO NOT raise sending")
    else:
        r.ok(f"utilization {print_util}% under scale-block {scale_block}% — capacity to scale")

    systems = c.get("systems", [])
    r.check(len(systems) >= 1, f"{len(systems)} delivery systems modeled",
            "no delivery systems modeled")

    for s in systems:
        name = s.get("name", "<unknown>")
        missing = [f for f in REQUIRED_SYSTEM_FIELDS if f not in s]
        r.check(not missing,
                f"{name}: capacity model complete",
                f"{name}: missing capacity fields {missing}")

    # Surface the fastest-to-deliver systems (lowest hours) as guidance.
    ranked = sorted(
        [s for s in systems if isinstance(s.get("estimated_delivery_hours"), (int, float))],
        key=lambda s: s["estimated_delivery_hours"],
    )
    if ranked:
        fastest = ", ".join(s["name"] for s in ranked[:3])
        r.ok(f"fastest to deliver: {fastest}")

    r.require_files(["docs/scale/DELIVERY_CAPACITY_PLANNING_AR.md",
                     "reports/scale/DELIVERY_CAPACITY_REVIEW.md"],
                    label="capacity doc")
    return r.render()


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
