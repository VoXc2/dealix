#!/usr/bin/env python3
"""Generate commercial weekly scorecard from evidence CSV (no invented CRM)."""

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
from dealix.commercial_ops.weekly_scorecard_commercial import (  # noqa: E402
    build_weekly_scorecard,
    render_weekly_scorecard_markdown,
)

BRIEFS = ROOT / "data/founder_briefs"


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    p.add_argument("--stdout-only", action="store_true")
    args = p.parse_args()

    blob = build_weekly_scorecard()
    md = render_weekly_scorecard_markdown(blob)

    if not args.stdout_only:
        BRIEFS.mkdir(parents=True, exist_ok=True)
        day = blob.get("week_end") or datetime.now(UTC).strftime("%Y-%m-%d")
        out = BRIEFS / f"weekly_scorecard_{day}.md"
        out.write_text(md, encoding="utf-8")
        blob["written_path"] = str(out.relative_to(ROOT)).replace("\\", "/")

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print(md)
        if blob.get("written_path"):
            print(f"\nWEEKLY_SCORECARD: OK → {blob['written_path']}")

    print("WEEKLY_SCORECARD_VERDICT=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
