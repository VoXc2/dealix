#!/usr/bin/env python3
"""Write value_plan JSON + markdown to data/founder_briefs/."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.commercial_ops.value_plan import (  # noqa: E402
    build_value_plan_snapshot,
    render_value_plan_markdown,
)

BRIEFS = ROOT / "data/founder_briefs"


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top-n", type=int, default=5)
    args = p.parse_args()

    snap = build_value_plan_snapshot(motion_top_n=max(1, min(args.top_n, 20)))
    day = snap.get("date") or datetime.now(UTC).strftime("%Y-%m-%d")
    BRIEFS.mkdir(parents=True, exist_ok=True)
    jpath = BRIEFS / f"value_plan_{day}.json"
    mpath = BRIEFS / f"value_plan_{day}.md"
    jpath.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mpath.write_text(render_value_plan_markdown(snap) + "\n", encoding="utf-8")
    print(f"VALUE_PLAN_SNAPSHOT: OK json={jpath.relative_to(ROOT)} md={mpath.relative_to(ROOT)}")
    print(f"FIRST_PAID_VERDICT={snap.get('north_star', {}).get('first_paid_verdict')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
