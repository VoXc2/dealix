"""Verify Stage 1 — Client Acquisition & Delivery OS files exist.

Usage:
    python3 scripts/verify_client_acquisition_delivery_os.py
"""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "apps/web/lib/company-os/company-os.ts",
    "apps/web/app/war-room/page.tsx",
    "apps/web/app/client-acquisition/page.tsx",
    "apps/web/app/delivery-os/page.tsx",
    "apps/web/app/kpi-finance/page.tsx",
    "apps/web/app/api/company-os/ceo-brief/route.ts",
    "business/acquisition/CLIENT_ACQUISITION_SYSTEM.md",
    "business/delivery/DELIVERY_AUTOMATION_BLUEPRINT.md",
    "business/finance/KPI_FINANCE_CONTROL.md",
    "business/ceo/FOUNDER_WAR_ROOM.md",
    "business/reports/DAILY_CEO_BRIEF_TEMPLATE.md",
    "scripts/generate_daily_ceo_brief.py",
]


def main() -> int:
    missing: list[str] = []
    for rel in REQUIRED_PATHS:
        p = REPO_ROOT / rel
        if not p.exists():
            missing.append(rel)
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("Dealix Client Acquisition & Delivery OS verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
