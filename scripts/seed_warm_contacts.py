#!/usr/bin/env python3
"""Seed deterministic warm contacts for manual founder outreach.

This script prepares local CSV data only. It never sends any external message.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

CSV_HEADERS = [
    "contact_id",
    "audience_type",
    "name",
    "role",
    "company",
    "sector",
    "relationship",
    "city",
    "linkedin_url",
    "email",
    "notes",
]

SEED_CONTACTS: list[dict[str, str]] = [
    {
        "contact_id": "wc_001",
        "audience_type": "operator",
        "name": "Ahmad Al-Harbi",
        "role": "COO",
        "company": "Najd Facilities Group",
        "sector": "facilities_services",
        "relationship": "warm",
        "city": "Riyadh",
        "linkedin_url": "https://linkedin.com/in/wc-001",
        "email": "ahmad@example.sa",
        "notes": "Met at LEAP governance roundtable; asks about AI controls and operational ROI.",
    },
    {
        "contact_id": "wc_002",
        "audience_type": "founder",
        "name": "Mona Al-Qahtani",
        "role": "Founder",
        "company": "Safa Logistics Tech",
        "sector": "logistics",
        "relationship": "warm",
        "city": "Jeddah",
        "linkedin_url": "https://linkedin.com/in/wc-002",
        "email": "mona@example.sa",
        "notes": "Requested practical AI ops playbook for revenue and approvals.",
    },
    {
        "contact_id": "wc_003",
        "audience_type": "advisor",
        "name": "Faisal Al-Salem",
        "role": "Advisor",
        "company": "B2B Growth Majlis",
        "sector": "consulting",
        "relationship": "active",
        "city": "Riyadh",
        "linkedin_url": "https://linkedin.com/in/wc-003",
        "email": "faisal@example.sa",
        "notes": "Introduces SaaS operators asking for auditability before AI expansion.",
    },
    {
        "contact_id": "wc_004",
        "audience_type": "operator",
        "name": "Reem Al-Otaibi",
        "role": "GM",
        "company": "Horizon Clinics Network",
        "sector": "healthcare",
        "relationship": "warm",
        "city": "Dammam",
        "linkedin_url": "https://linkedin.com/in/wc-004",
        "email": "reem@example.sa",
        "notes": "Needs controlled rollout narrative for AI-enabled patient support workflows.",
    },
    {
        "contact_id": "wc_005",
        "audience_type": "investor",
        "name": "Khalid Al-Mutairi",
        "role": "Investment Manager",
        "company": "Wadi Ventures",
        "sector": "venture_capital",
        "relationship": "warm",
        "city": "Riyadh",
        "linkedin_url": "https://linkedin.com/in/wc-005",
        "email": "khalid@example.sa",
        "notes": "Tracks portfolio demand for AI governance and accountable revenue ops.",
    },
    {
        "contact_id": "wc_006",
        "audience_type": "operator",
        "name": "Noura Al-Dossary",
        "role": "VP Sales",
        "company": "Tawazon Manufacturing",
        "sector": "manufacturing",
        "relationship": "warm",
        "city": "Riyadh",
        "linkedin_url": "https://linkedin.com/in/wc-006",
        "email": "noura@example.sa",
        "notes": "Asks for lead qualification with governance boundaries.",
    },
    {
        "contact_id": "wc_007",
        "audience_type": "founder",
        "name": "Saad Al-Hassan",
        "role": "CEO",
        "company": "Madar SaaS",
        "sector": "saas",
        "relationship": "warm",
        "city": "Khobar",
        "linkedin_url": "https://linkedin.com/in/wc-007",
        "email": "saad@example.sa",
        "notes": "Looking for evidence trail model before scaling AI automations.",
    },
    {
        "contact_id": "wc_008",
        "audience_type": "advisor",
        "name": "Laila Al-Faraj",
        "role": "Strategy Advisor",
        "company": "Riyada Advisory",
        "sector": "professional_services",
        "relationship": "active",
        "city": "Riyadh",
        "linkedin_url": "https://linkedin.com/in/wc-008",
        "email": "laila@example.sa",
        "notes": "Supports founders evaluating safe AI-led GTM operations.",
    },
    {
        "contact_id": "wc_009",
        "audience_type": "operator",
        "name": "Yousef Al-Ghamdi",
        "role": "Head of Operations",
        "company": "Najm Commerce",
        "sector": "retail",
        "relationship": "warm",
        "city": "Jeddah",
        "linkedin_url": "https://linkedin.com/in/wc-009",
        "email": "yousef@example.sa",
        "notes": "Needs controlled AI adoption process with clear approval gates.",
    },
    {
        "contact_id": "wc_010",
        "audience_type": "investor",
        "name": "Huda Al-Rasheed",
        "role": "Principal",
        "company": "Sadu Capital",
        "sector": "private_equity",
        "relationship": "warm",
        "city": "Riyadh",
        "linkedin_url": "https://linkedin.com/in/wc-010",
        "email": "huda@example.sa",
        "notes": "Asks portfolio teams for measurable AI value with risk controls.",
    },
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed warm contacts CSV for manual outreach")
    parser.add_argument(
        "--out",
        default="data/warm_list.csv",
        help="Output CSV path relative to repo root",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists",
    )
    args = parser.parse_args()

    out_path = (REPO_ROOT / args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} already exists (use --force to overwrite)")
        return 0

    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(SEED_CONTACTS)

    print(f"OK: wrote {len(SEED_CONTACTS)} warm contacts -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
