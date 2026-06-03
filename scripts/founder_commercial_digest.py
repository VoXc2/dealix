#!/usr/bin/env python3
"""Founder commercial digest — evidence, War Room, social draft, optional API sync."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.daily_pack import write_daily_pack_index  # noqa: E402
from dealix.commercial_ops.digest import (  # noqa: E402
    build_commercial_digest,
    render_digest_markdown,
    write_digest_file,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument("--out", default=None, help="Write markdown (default: data/founder_briefs/)")
    p.add_argument("--sync-evidence", action="store_true", help="POST CSV events to evidence API")
    p.add_argument(
        "--pull-evidence",
        action="store_true",
        help="Append new API evidence events into CSV before digest",
    )
    p.add_argument("--skip-no-build", action="store_true")
    p.add_argument("--no-build-days", type=int, default=14)
    p.add_argument("--no-pack-index", action="store_true", help="Skip DAILY_PACK_*.md + index.json")
    args = p.parse_args()

    digest = build_commercial_digest(
        sync_evidence=args.sync_evidence,
        pull_evidence=args.pull_evidence,
        no_build_days=args.no_build_days,
        skip_no_build=args.skip_no_build,
    )

    if args.format == "json":
        print(json.dumps(digest, ensure_ascii=False, indent=2))
    else:
        md = render_digest_markdown(digest)
        out_path: Path | None
        if args.out:
            out_path = Path(args.out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(md + "\n", encoding="utf-8")
            print(f"WROTE · {out_path}", file=sys.stderr)
        else:
            out_path = write_digest_file(digest)
            print(f"WROTE · {out_path}", file=sys.stderr)
        if not args.no_pack_index:
            pack = write_daily_pack_index(digest_path=out_path)
            print(f"WROTE · {pack}", file=sys.stderr)
            print(f"WROTE · {pack.parent / 'index.json'}", file=sys.stderr)
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
