"""Smoke test: checks that key local files exist and demo operator passes.

Usage:
    python3 scripts/local_smoke_test.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "apps/web/app/war-room/page.tsx",
    "apps/web/app/client-acquisition/page.tsx",
    "apps/web/app/delivery-os/page.tsx",
    "apps/web/app/kpi-finance/page.tsx",
    "apps/web/app/automated-sales/page.tsx",
    "apps/web/app/persuasion-room/page.tsx",
    "apps/web/app/brand/page.tsx",
    "apps/web/app/offers/page.tsx",
    "apps/web/app/pricing/page.tsx",
    "apps/web/app/cases/page.tsx",
    "apps/web/app/revenue-machine/page.tsx",
    "apps/web/app/sales-assets/page.tsx",
    "apps/web/app/lead-engine/page.tsx",
    "apps/web/app/command-center/page.tsx",
    "apps/web/app/pipeline/page.tsx",
    "apps/web/app/partner-room/page.tsx",
    "apps/web/app/daily-draft/page.tsx",
    "apps/web/app/api/company-os/ceo-brief/route.ts",
    "apps/web/app/api/company-os/founder-dashboard/route.ts",
    "apps/web/app/api/sales-machine/ultimate-pack/route.ts",
    "apps/web/app/api/sales-machine/daily-pack/route.ts",
]


def main() -> int:
    print("Dealix local smoke test")
    print("=" * 50)
    missing = [r for r in REQUIRED if not (REPO_ROOT / r).exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print(f"All {len(REQUIRED)} page/api files exist.")
    print("\nRunning daily operator (demo)...")
    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "dealix_daily_operator.py"), "--mode", "demo"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode == 0:
        print("Daily operator OK")
        return 0
    print("Daily operator FAIL")
    print(r.stdout[-1000:])
    print(r.stderr[-1000:])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
