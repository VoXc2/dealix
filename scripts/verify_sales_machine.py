"""Verify Stage 2 — Automated Sales Machine files exist.

Usage:
    python3 scripts/verify_sales_machine.py
"""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "apps/web/lib/sales-automation/lead-sources.ts",
    "apps/web/app/automated-sales/page.tsx",
    "apps/web/app/persuasion-room/page.tsx",
    "apps/web/app/api/sales-machine/daily-pack/route.ts",
    "apps/web/public/dealix-logo.svg",
    "business/sales-automation/AUTOMATED_LEAD_ENGINE.md",
    "business/sales-automation/BILINGUAL_OUTREACH_LIBRARY.md",
    "business/brand/LOGO_BRIEF.md",
    "scripts/generate_sales_machine_pack.py",
]


def main() -> int:
    missing = [r for r in REQUIRED if not (REPO_ROOT / r).exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("Dealix Automated Sales Machine verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
