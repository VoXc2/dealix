#!/usr/bin/env python3
"""Print / write founder SOAEN + doctrine block (governed commercial day)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


from dealix.commercial_ops.doctrine import (  # noqa: E402
    build_soaen_daily,
    format_doctrine_markdown,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument("--out", default=None, help="Write markdown to path")
    p.add_argument("--date", default=None)
    args = p.parse_args()

    block = build_soaen_daily(date_str=args.date)
    if args.format == "json":
        print(json.dumps(block, ensure_ascii=False, indent=2))
    else:
        md = format_doctrine_markdown(block)
        if args.out:
            path = Path(args.out)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(md + "\n", encoding="utf-8")
            print(f"WROTE · {path}", file=sys.stderr)
        print(md)
    print("FOUNDER_SOAEN_DAILY=OK", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
