#!/usr/bin/env python3
"""Human-friendly summary of the Capital Asset Library.

Reads data/capital_asset_index.json and prints:
  - total count
  - count by CapitalAssetType
  - the 10 most recent entries (title + asset_type + git_author)

Usage:
    python scripts/capital_asset_summary.py
    python scripts/capital_asset_summary.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "data" / "capital_asset_index.json"


def _load() -> dict:
    if not INDEX_PATH.exists():
        return {"entries": []}
    try:
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"entries": []}


def summarize(data: dict) -> dict:
    entries = list(data.get("entries") or [])
    by_type: Counter[str] = Counter()
    for e in entries:
        atype = str(e.get("asset_type") or "")
        if atype:
            by_type[atype] += 1
    recent = []
    for e in entries[-10:]:
        recent.append({
            "title": str(e.get("title") or "")[:80],
            "asset_type": str(e.get("asset_type") or ""),
            "created_at": str(e.get("created_at") or ""),
            "git_author": str(e.get("git_author") or ""),
        })
    return {
        "total": len(entries),
        "by_type": dict(by_type),
        "recent": recent,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="capital asset summary")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)
    s = summarize(_load())
    if args.json:
        print(json.dumps(s, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    print(f"Capital Asset Library — {s['total']} entries")
    if s["by_type"]:
        print("By type:")
        for t in sorted(s["by_type"]):
            print(f"  {t:25s} {s['by_type'][t]}")
    if s["recent"]:
        print("Recent:")
        for r in s["recent"]:
            print(f"  [{r['asset_type']}] {r['title']}  ({r['created_at'][:10]} by {r['git_author']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
