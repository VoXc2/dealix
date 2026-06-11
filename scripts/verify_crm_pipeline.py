"""Verify CRM pipeline files exist.

Usage:
    python3 scripts/verify_crm_pipeline.py
"""
from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "business/crm/schema.md",
    "business/crm/prospects.seed.json",
    "business/crm/README.md",
    "apps/web/lib/company-os/pipeline.ts",
    "apps/web/lib/generated/founder-dashboard.ts",
    "apps/web/app/api/company-os/founder-dashboard/route.ts",
    "scripts/import_leads_csv.py",
    "scripts/score_leads.py",
    "scripts/generate_outreach_drafts.py",
    "scripts/approve_outreach_draft.py",
    "scripts/reject_outreach_draft.py",
    "scripts/generate_prospect_pack.py",
    "scripts/generate_followup_queue.py",
]


def main() -> int:
    missing = [r for r in REQUIRED if not (REPO_ROOT / r).exists()]
    if missing:
        print("MISSING:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("Dealix CRM pipeline verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
