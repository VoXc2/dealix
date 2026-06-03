#!/usr/bin/env python3
"""Initialize weekly founder decision YAML (one decision + deviation + stop list)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_comprehensive_plan import init_weekly_decision  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--week-id", default=None, help="e.g. 2026-W20")
    args = p.parse_args()
    path = init_weekly_decision(week_id=args.week_id)
    rel = path.relative_to(ROOT).as_posix()
    print(f"WEEKLY_DECISION_PATH={rel}")
    print("FOUNDER_WEEKLY_DECISION_INIT=OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
