#!/usr/bin/env python3
"""Print or apply today's rotated agency P0 targets."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.commercial_ops.targeting_csv import TARGET_FIELDS, load_targets  # noqa: E402
from dealix.commercial_ops.targeting_rotation import (  # noqa: E402
    apply_rotation_touch_dates,
    select_daily_p0_targets,
)


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top-n", type=int, default=10)
    p.add_argument("--cooldown-days", type=int, default=3)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--apply", action="store_true", help="Write next_action_date on selected rows")
    args = p.parse_args()

    rows = load_targets(AGENCY_TARGETS_CSV)
    selected = select_daily_p0_targets(
        rows, top_n=args.top_n, cooldown_days=args.cooldown_days
    )

    print(f"ROTATION · selected={len(selected)} / pool={len(rows)}")
    for i, r in enumerate(selected, 1):
        print(
            f"  {i}. {r.get('company')} · {r.get('status')} · "
            f"pr={r.get('priority')} · {r.get('next_action', '')[:50]}"
        )

    if args.apply and not args.dry_run:
        updated = apply_rotation_touch_dates(rows, selected)
        path = AGENCY_TARGETS_CSV
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(TARGET_FIELDS))
            writer.writeheader()
            for row in updated:
                writer.writerow({k: row.get(k, "") for k in TARGET_FIELDS})
        print(f"WROTE · {path}")
    elif args.apply and args.dry_run:
        print("DRY-RUN · would write CSV")

    return 0


if __name__ == "__main__":
    sys.exit(main())
