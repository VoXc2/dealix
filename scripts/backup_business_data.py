"""Backup business data into a single zip.

Usage:
    python3 scripts/backup_business_data.py
"""
from __future__ import annotations

import datetime as dt
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = REPO_ROOT / "reports" / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    today = dt.date.today().isoformat()
    out = BACKUP_DIR / f"dealix-business-data-{today}.zip"

    paths = [
        "business/_data",
        "business/crm",
        "business/proposals/generated",
        "business/closing/exports",
        "business/conversion/exports",
        "business/delivery/exports",
        "business/lead-lists/exports",
        "business/launch/exports",
        "business/proof/exports",
        "business/reports/exports",
        "business/retention/exports",
        "business/sales-automation/exports",
        "business/sales-machine/exports",
    ]
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in paths:
            base = REPO_ROOT / p
            if not base.exists():
                continue
            for f in base.rglob("*"):
                if f.is_file():
                    zf.write(f, f.relative_to(REPO_ROOT))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
