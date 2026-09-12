#!/usr/bin/env python3
"""Verify the OP2 CI-cron ownership map is complete and collision-aware.

Prints: DEALIX_OP2_CI_CRON_MAP_VERDICT=PASS|FAIL
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PATH = REPO_ROOT / "data" / "commercial" / "op2_ci_cron_ownership_map_v1.json"
VERDICT_PASS = "DEALIX_OP2_CI_CRON_MAP_VERDICT=PASS"
VERDICT_FAIL = "DEALIX_OP2_CI_CRON_MAP_VERDICT=FAIL"


def main() -> int:
    errors: list[str] = []
    if not PATH.exists():
        print(VERDICT_FAIL)
        print(f"  - missing {PATH}")
        return 1
    try:
        payload = json.loads(PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(VERDICT_FAIL)
        print(f"  - invalid json: {exc}")
        return 1

    if payload.get("schema") != "dealix.op2-ci-cron-ownership-map.v1":
        errors.append("unexpected schema")
    if payload.get("read_only") is not True:
        errors.append("map must be read-only")
    workflows = payload.get("workflows") or []
    if not workflows:
        errors.append("no workflows parsed")
    if payload.get("workflow_count") != len(workflows):
        errors.append("workflow_count mismatch")

    seen = {entry.get("workflow") for entry in workflows}
    for entry in workflows:
        if not entry.get("crons"):
            errors.append(f"{entry.get('workflow')}: missing crons")
        if entry.get("classification") not in {"UNIQUE_SLOT", "COLLISION_REVIEW"}:
            errors.append(f"{entry.get('workflow')}: invalid classification")
        collisions = entry.get("collision_crons") or []
        if collisions and entry.get("classification") != "COLLISION_REVIEW":
            errors.append(f"{entry.get('workflow')}: has collisions but not flagged")

    for cron, files in (payload.get("duplicate_slots") or {}).items():
        if len(files) < 2:
            errors.append(f"duplicate slot {cron} must list >=2 workflows")
        if not set(files) <= seen:
            errors.append(f"duplicate slot {cron} references unknown workflow")

    print(VERDICT_PASS if not errors else VERDICT_FAIL)
    for err in errors:
        print(f"  - {err}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
