#!/usr/bin/env python3
"""Print consolidated commercial value-map status for founder review."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.commercial_ops.value_map_status import (  # noqa: E402
    build_commercial_value_map,
    build_value_map_status,
    write_value_map_artifacts,
)

SNAPSHOT_JSON = ROOT / "data" / "commercial_value_map_snapshot.json"


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true", help="Machine-readable output")
    p.add_argument("--full", action="store_true", help="Include value_plan snapshot")
    p.add_argument(
        "--write-json",
        action="store_true",
        help="Write data/commercial_value_map_snapshot.json",
    )
    p.add_argument("--top-n", type=int, default=5, help="Motion A targets when --full")
    p.add_argument(
        "--write-md",
        action="store_true",
        help="Write data/founder_briefs/commercial_value_map_YYYY-MM-DD.md",
    )
    args = p.parse_args()

    if args.write_md:
        paths = write_value_map_artifacts(motion_top_n=max(1, min(args.top_n, 20)))
        print(f"WROTE {paths['md']}")
        print(f"WROTE {paths['json']}")
        if not (args.full or args.write_json or args.json):
            print("COMMERCIAL_VALUE_MAP_WRITE=OK")
            return 0

    if args.full or args.write_json:
        blob = build_commercial_value_map(
            include_value_plan=True,
            motion_top_n=max(1, min(args.top_n, 20)),
        )
    else:
        blob = build_value_map_status()

    if args.write_json:
        SNAPSHOT_JSON.parent.mkdir(parents=True, exist_ok=True)
        SNAPSHOT_JSON.write_text(
            json.dumps(blob, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"WROTE {SNAPSHOT_JSON}")

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
        return 0

    if args.full:
        st = blob.get("status") or {}
        fp = st.get("first_paid") or {}
        print("== commercial_value_map (full) ==")
        print(f"  generated: {blob.get('generated_at')}")
        print(f"  pipeline: {fp.get('verdict')}")
        vp = blob.get("value_plan") or {}
        for w in vp.get("warnings_ar") or []:
            print(f"  WARN: {w}")
        print("COMMERCIAL_VALUE_MAP_FULL=OK")
        return 0

    fp = blob["first_paid"]
    print("== commercial_value_map_status ==")
    print(f"  generated: {blob['generated_at']}")
    print(f"  brief_latest: {blob.get('brief_latest_date') or '—'}")
    print(f"  agency_seed_rows: {blob['agency_seed_rows']} (strict>=80: {blob['agency_seed_strict_ok']})")
    print(f"  pipeline: {fp['verdict']}")
    print(f"  payment_received (real): {fp['payment_received_real']}")
    print(f"  proof_pack_delivered (real): {fp['proof_pack_delivered_real']}")
    print(f"  evidence_rows: {fp['total_events']}")
    print(f"  crm_kpi_pending: {fp['crm_kpi_pending']}")
    print(f"  ladder: {fp.get('revenue_ladder_ar', '—')}")
    print("  doc: docs/commercial/COMMERCIAL_VALUE_MAP_AR.md")
    for action in blob["founder_action"]:
        print(f"  FOUNDER_ACTION: {action}")
    print("COMMERCIAL_VALUE_MAP_STATUS=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
