#!/usr/bin/env python3
"""Compatibility view for Dealix growth work inside the canonical Company OS.

Growth is a workload lane, not a second operating system. This adapter ensures
that today's canonical Company OS cycle exists, then reports the existing
market/revenue/content actions. It never creates synthetic leads or sends.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "scripts" / "commercial" / "run_self_operating_company_os.py"
REPORT_ROOT = ROOT / "reports" / "self_operating_company_os"


def today() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def ensure_cycle(mode: str, limit: int) -> int:
    actions = REPORT_ROOT / "actions" / f"{today()}.json"
    if actions.is_file():
        return 0
    return subprocess.run(
        [sys.executable, str(CANONICAL), "--mode", mode, "--limit", str(limit)],
        cwd=ROOT,
        check=False,
    ).returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--autonomy-level", type=int, default=3)
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    if args.autonomy_level > 4:
        print("AUTONOMOUS_GROWTH=BLOCKED_MATERIAL_AUTONOMY")
        return 2
    if not CANONICAL.is_file():
        print("AUTONOMOUS_GROWTH=BLOCKED_CANONICAL_RUNNER_MISSING")
        return 2
    rc = ensure_cycle(args.mode, args.limit)
    if rc != 0:
        return rc
    path = REPORT_ROOT / "actions" / f"{today()}.json"
    try:
        actions = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("AUTONOMOUS_GROWTH=BLOCKED_CANONICAL_ACTIONS_UNREADABLE")
        return 2
    lanes = {"market_signal_intake", "relationship_and_revenue", "content_and_distribution"}
    selected = [item for item in actions if isinstance(item, dict) and item.get("playbook") in lanes]
    print(json.dumps({"delegated": True, "canonical_action_count": len(selected), "actions": selected}, ensure_ascii=False, indent=2))
    print("AUTONOMOUS_GROWTH=DELEGATED_TO_CANONICAL_COMPANY_OS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
