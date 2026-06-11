"""Verify Delivery OS files exist.

Usage:
    python3 scripts/verify_delivery_os.py
"""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "apps/web/app/delivery-os/page.tsx",
    "business/delivery/CLIENT_DELIVERY_SOP.md",
    "business/delivery/CLIENT_ONBOARDING_CHECKLIST.md",
    "business/delivery/PROOF_REPORT_TEMPLATE.md",
    "business/delivery/WEEKLY_COMMAND_REPORT_TEMPLATE.md",
    "business/delivery/CHANGE_REQUEST_POLICY.md",
    "business/delivery/DELIVERY_AUTOMATION_BLUEPRINT.md",
    "scripts/generate_delivery_plan.py",
    "scripts/generate_weekly_command_report.py",
    "scripts/generate_client_brief.py",
    "scripts/generate_workflow_review_agenda.py",
]


def main() -> int:
    missing = [r for r in REQUIRED if not (REPO_ROOT / r).exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("Dealix Delivery OS verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
