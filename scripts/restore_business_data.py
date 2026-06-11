"""Restore business data from a backup zip (requires --confirm).

Usage:
    python3 scripts/restore_business_data.py --from reports/backups/dealix-business-data-YYYY-MM-DD.zip --confirm
"""
from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="src", required=True, help="Path to backup zip")
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()

    src = Path(args.src)
    if not src.exists():
        print(f"backup not found: {src}")
        return 1
    if not args.confirm:
        print("Refusing to restore without --confirm. Pass --confirm to proceed.")
        return 1

    with zipfile.ZipFile(src, "r") as zf:
        for member in zf.namelist():
            dest = REPO_ROOT / member
            dest.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as f, dest.open("wb") as out:
                shutil.copyfileobj(f, out)
    print(f"restored from {src}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
