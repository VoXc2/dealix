#!/usr/bin/env python3
"""Compatibility view for governed learning inside the canonical Company OS."""
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", default="dealix", help="Compatibility only")
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    args = parser.parse_args()
    actions_path = REPORT_ROOT / "actions" / f"{today()}.json"
    if not actions_path.is_file():
        rc = subprocess.run(
            [sys.executable, str(CANONICAL), "--mode", args.mode, "--limit", "50"],
            cwd=ROOT,
            check=False,
        ).returncode
        if rc != 0:
            return rc
    try:
        actions = json.loads(actions_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("SELF_IMPROVEMENT=BLOCKED_CANONICAL_ACTIONS_UNREADABLE")
        return 2
    learning = [item for item in actions if isinstance(item, dict) and item.get("playbook") == "learning_loop"]
    print(json.dumps({"delegated": True, "learning_actions": learning}, ensure_ascii=False, indent=2))
    print("SELF_IMPROVEMENT=DELEGATED_TO_CANONICAL_LEARNING_LOOP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
