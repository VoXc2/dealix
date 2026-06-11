"""Verify the Ultimate Sales OS pack files exist.

Usage:
    python3 scripts/verify_ultimate_sales_os.py
"""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "apps/web/lib/sales-machine/ultimate-sales-os.ts",
    "apps/web/app/api/sales-machine/ultimate-pack/route.ts",
    "apps/web/app/offers/page.tsx",
    "apps/web/app/pricing/page.tsx",
    "apps/web/app/brand/page.tsx",
    "apps/web/app/cases/page.tsx",
    "business/sales-machine/DEALIX_MASTER_SALES_FILE_AR.md",
    "business/sales-machine/DEALIX_MASTER_SALES_FILE_EN.md",
    "business/sales-machine/OBJECTION_HANDLING_LIBRARY.md",
    "business/pricing/OFFER_LADDER.md",
    "scripts/generate_ultimate_sales_os_pack.py",
]


def main() -> int:
    missing = [r for r in REQUIRED if not (REPO_ROOT / r).exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("Dealix Ultimate Sales OS verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
