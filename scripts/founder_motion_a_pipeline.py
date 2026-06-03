#!/usr/bin/env python3
"""Print Motion A daily pipeline + write data/founder_briefs/motion_a_YYYY-MM-DD.md."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.motion_a_pipeline import (  # noqa: E402
    build_motion_a_pipeline_plan,
    render_motion_a_markdown,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

BRIEFS = ROOT / "data/founder_briefs"


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--top-n", type=int, default=10)
    p.add_argument("--json", action="store_true")
    p.add_argument("--no-write", action="store_true", help="Print only; skip brief file")
    args = p.parse_args()

    plan = build_motion_a_pipeline_plan(top_n=max(1, min(args.top_n, 20)))
    md = render_motion_a_markdown(plan)

    if not args.no_write:
        BRIEFS.mkdir(parents=True, exist_ok=True)
        day = datetime.now(UTC).strftime("%Y-%m-%d")
        out = BRIEFS / f"motion_a_{day}.md"
        out.write_text(md, encoding="utf-8")
        plan["written_path"] = str(out.relative_to(ROOT)).replace("\\", "/")

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(md)
        if plan.get("written_path"):
            print(f"\nMOTION_A_PIPELINE: OK → {plan['written_path']}")

    print(f"MOTION_A_PIPELINE_VERDICT={plan['first_paid'].get('verdict', 'UNKNOWN')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
