#!/usr/bin/env python3
"""Verify every file required by the launch manifest exists and is non-empty."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import CheckResult, load_yaml, main, rel  # noqa: E402


def check() -> CheckResult:
    r = CheckResult("file_manifest")
    try:
        manifest = load_yaml("data/launch/file_manifest.yaml")
    except FileNotFoundError:
        r.error("data/launch/file_manifest.yaml is missing — run scripts/launch/build.py")
        return r

    packs = manifest.get("packs", {})
    total = 0
    missing = 0
    for pack, entries in packs.items():
        for entry in entries:
            total += 1
            path = entry["path"]
            min_bytes = entry.get("min_bytes", 1)
            p = rel(path)
            if not p.exists():
                r.error(f"[{pack}] missing: {path}")
                missing += 1
            elif p.stat().st_size < max(1, min_bytes):
                r.error(f"[{pack}] too small ({p.stat().st_size}b): {path}")
                missing += 1
    r.note(f"manifest lists {total} files across {len(packs)} packs; missing/empty: {missing}")
    return r


if __name__ == "__main__":
    main(check)
