"""Verify Company OS files exist.

Usage:
    python3 scripts/verify_company_os.py
"""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "apps/web/lib/company-os/company-os.ts",
    "apps/web/app/war-room/page.tsx",
    "apps/web/app/client-acquisition/page.tsx",
    "apps/web/app/kpi-finance/page.tsx",
    "apps/web/app/command-center/page.tsx",
    "apps/web/app/api/company-os/ceo-brief/route.ts",
    "business/ceo/FOUNDER_WAR_ROOM.md",
    "business/reports/DAILY_CEO_BRIEF_TEMPLATE.md",
    "scripts/generate_daily_ceo_brief.py",
]


def main() -> int:
    missing = [r for r in REQUIRED if not (REPO_ROOT / r).exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("Dealix Company OS verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
