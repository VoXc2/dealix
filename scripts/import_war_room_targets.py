#!/usr/bin/env python3
"""Import agency targeting CSV into War Room (local autopilot store)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.targeting_csv import load_targets
from dealix.commercial_ops.war_room_import import import_default_csv, import_target_rows
from dealix.revenue_ops_autopilot.orchestrator import RevenueAutopilotOrchestrator


def main() -> int:
    parser = argparse.ArgumentParser(description="Import War Room targets from agency_accounts_seed.csv")
    parser.add_argument("--dry-run", action="store_true", help="Count rows only; do not write store")
    parser.add_argument("--apply", action="store_true", help="Apply import to local autopilot store")
    parser.add_argument("--csv", type=Path, default=None, help="Override CSV path")
    parser.add_argument(
        "--via-api",
        action="store_true",
        help="POST to ops-autopilot/import-targets when DEALIX_ADMIN_API_KEY set",
    )
    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Specify --dry-run or --apply")
        return 2

    rows = load_targets(args.csv) if args.csv else load_targets()
    print(f"WAR_ROOM_IMPORT: rows_in_csv={len(rows)}")

    if args.dry_run:
        companies = [r.get("company", "").strip() for r in rows if r.get("company", "").strip()]
        print(f"WAR_ROOM_IMPORT: unique_companies={len(set(c.lower() for c in companies))}")
        print(json.dumps({"dry_run": True, "rows": len(rows)}, ensure_ascii=False))
        return 0

    if args.via_api:
        from dealix.commercial_ops.api_client import import_war_room_targets_api

        result = import_war_room_targets_api(use_default_csv=not args.csv)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print(f"WAR_ROOM_IMPORT: OK via API imported={result.get('imported', 0)}")
            return 0
        print("WAR_ROOM_IMPORT: API skipped — falling back to local store", file=sys.stderr)

    orch = RevenueAutopilotOrchestrator()
    if args.csv:
        result = import_target_rows(rows, orch)
    else:
        result = import_default_csv(orch)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"WAR_ROOM_IMPORT: OK imported={result.get('imported', 0)} skipped={result.get('skipped_duplicates', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
