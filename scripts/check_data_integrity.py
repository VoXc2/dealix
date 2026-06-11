"""Check integrity of business data.

Usage:
    python3 scripts/check_data_integrity.py
"""
from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "business" / "_data"


def main() -> int:
    if not DATA_DIR.exists():
        print(f"missing: {DATA_DIR}")
        return 1
    bad: list[str] = []
    for f in DATA_DIR.rglob("*.json"):
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            bad.append(f"{f.relative_to(REPO_ROOT)}: {e}")
    if bad:
        print("Bad JSON files:")
        for b in bad:
            print(f"  - {b}")
        return 1
    print(f"All JSON files in {DATA_DIR} are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
