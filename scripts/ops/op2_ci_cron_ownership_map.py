#!/usr/bin/env python3
"""OP2 CI-cron scheduler ownership map.

The canonical scheduler audit (``scripts/ops/audit_dealix_schedulers.py``,
OP1-owned) inventories systemd timers and Hermes cron. It does not cover the
GitHub Actions cron plane, where many Dealix daily/weekly loops actually run.

This OP2 tool adds the missing CI-cron inventory: it parses every workflow with
``schedule.cron``, detects duplicate slots across workflows (one responsibility
should have one scheduler), and emits a deterministic ownership map with a
suggested canonical owner and collision classification.

It is read-only: it never edits, dispatches, or disables a workflow.

Prints: DEALIX_OP2_CI_CRON_MAP=OK plus machine lines.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
OUT_PATH = REPO_ROOT / "data" / "commercial" / "op2_ci_cron_ownership_map_v1.json"

NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)
CRON_RE = re.compile(r"-\s*cron:\s*[\"']?([^\"'\n]+)")


def _workflow_title(path: Path, text: str) -> str:
    match = NAME_RE.search(text)
    return match.group(1).strip() if match else path.stem


def build_map() -> dict[str, Any]:
    workflows: list[dict[str, Any]] = []
    by_cron: dict[str, list[str]] = {}

    if WORKFLOWS_DIR.exists():
        for path in sorted(WORKFLOWS_DIR.glob("*.yml")):
            text = path.read_text(encoding="utf-8")
            if "schedule:" not in text:
                continue
            crons = [cron.strip().strip("\"'") for cron in CRON_RE.findall(text)]
            if not crons:
                continue
            entry = {
                "workflow": path.name,
                "title": _workflow_title(path, text),
                "crons": crons,
            }
            workflows.append(entry)
            for cron in crons:
                by_cron.setdefault(cron, []).append(path.name)

    duplicate_slots = {
        cron: sorted(files)
        for cron, files in sorted(by_cron.items())
        if len(files) > 1
    }

    for entry in workflows:
        collisions = sorted({cron for cron in entry["crons"] if cron in duplicate_slots})
        entry["collision_crons"] = collisions
        entry["classification"] = "COLLISION_REVIEW" if collisions else "UNIQUE_SLOT"
        # Suggested owner is the workflow itself; a human/PM resolves collisions.
        entry["suggested_canonical_owner"] = entry["workflow"]

    return {
        "schema": "dealix.op2-ci-cron-ownership-map.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "scope": "GITHUB_ACTIONS_CRON_PLANE",
        "complements": "scripts/ops/audit_dealix_schedulers.py (systemd + Hermes, OP1-owned)",
        "read_only": True,
        "workflow_count": len(workflows),
        "distinct_cron_slots": len(by_cron),
        "collision_slot_count": len(duplicate_slots),
        "duplicate_slots": duplicate_slots,
        "workflows": workflows,
    }


def render(result: dict[str, Any]) -> str:
    lines = [
        "DEALIX_OP2_CI_CRON_MAP=OK",
        f"WORKFLOWS_WITH_CRON={result['workflow_count']}",
        f"DISTINCT_SLOTS={result['distinct_cron_slots']}",
        f"COLLISION_SLOTS={result['collision_slot_count']}",
    ]
    for cron, files in result["duplicate_slots"].items():
        lines.append(f"COLLISION cron='{cron}' workflows={','.join(files)}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="OP2 CI-cron ownership map")
    parser.add_argument("--write", action="store_true", help=f"write {OUT_PATH}")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_map()
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render(result))
    if args.write:
        OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"WROTE {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
