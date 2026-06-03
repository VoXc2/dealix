#!/usr/bin/env python3
"""Bundle weekly KPI + Truth Matrix + evidence scorecard (no invented CRM)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_weekly_metrics import (  # noqa: E402
    build_founder_weekly_metrics,
    write_weekly_metrics_artifact,
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write", action="store_true", help="Write data/founder_weekly/metrics_{week}.yaml")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    blob = build_founder_weekly_metrics()
    if args.write:
        path = write_weekly_metrics_artifact(blob)
        print(f"wrote: {path}")

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print(f"iso_week: {blob['iso_week']}")
        print(f"kpi pending: {len(blob['kpi_commercial'].get('pending', []))}")
        print(f"truth red: {len(blob['truth_matrix'].get('red', []))}")
        for b in blob.get("blockers_ar", []):
            print(f"  blocker: {b}")

    print(f"FOUNDER_WEEKLY_METRICS_VERDICT={blob['verdict']}")
    return 0 if blob["verdict"] == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
