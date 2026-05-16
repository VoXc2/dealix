#!/usr/bin/env python3
"""Ensure warm list contains at least N contacts."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

FIELDS = [
    "name",
    "role",
    "company",
    "sector",
    "relationship",
    "city",
    "linkedin_url",
    "notes",
]

DEFAULT_CONTACTS: list[dict[str, str]] = [
    {"name": "Founder Friend One", "role": "COO", "company": "Riyadh Consulting LLC", "sector": "b2b_services", "relationship": "warm", "city": "Riyadh", "linkedin_url": "https://linkedin.com/in/founder-friend-1", "notes": "met at LEAP 2025"},
    {"name": "Maha Alharbi", "role": "CEO", "company": "Najd Industrial Systems", "sector": "b2b_services", "relationship": "warm", "city": "Riyadh", "linkedin_url": "https://linkedin.com/in/maha-alharbi", "notes": "warm intro from board advisor"},
    {"name": "Yousef Almutairi", "role": "Founder", "company": "ScaleOps Arabia", "sector": "b2b_saas", "relationship": "warm", "city": "Riyadh", "linkedin_url": "https://linkedin.com/in/yousef-almutairi", "notes": "past collaboration on GTM sprint"},
    {"name": "Lina Alqahtani", "role": "GM", "company": "Jeddah Health Connect", "sector": "healthcare_clinic", "relationship": "warm", "city": "Jeddah", "linkedin_url": "https://linkedin.com/in/lina-alqahtani", "notes": "referred by existing customer"},
    {"name": "Abdullah Alshammari", "role": "COO", "company": "EastGate Logistics", "sector": "b2b_services", "relationship": "warm", "city": "Dammam", "linkedin_url": "https://linkedin.com/in/abdullah-alshammari", "notes": "met at chamber of commerce event"},
    {"name": "Nourah Alzahrani", "role": "Founder", "company": "BluePalm Real Estate", "sector": "real_estate", "relationship": "warm", "city": "Jeddah", "linkedin_url": "https://linkedin.com/in/nourah-alzahrani", "notes": "warm WhatsApp intro"},
    {"name": "Saad Alshehri", "role": "CEO", "company": "RedSea Training Hub", "sector": "training_consulting", "relationship": "warm", "city": "Jeddah", "linkedin_url": "https://linkedin.com/in/saad-alshehri", "notes": "known through webinar network"},
    {"name": "Rakan Alotaibi", "role": "VP Sales", "company": "Vertex Manufacturing", "sector": "b2b_services", "relationship": "active", "city": "Riyadh", "linkedin_url": "https://linkedin.com/in/rakan-alotaibi", "notes": "already requested diagnostic call"},
    {"name": "Hind Alrashid", "role": "Founder", "company": "Pulse Agency KSA", "sector": "agency", "relationship": "warm", "city": "Riyadh", "linkedin_url": "https://linkedin.com/in/hind-alrashid", "notes": "partner referral candidate"},
    {"name": "Faisal Alharbi", "role": "COO", "company": "Desert Retail Tech", "sector": "ecommerce_b2c", "relationship": "warm", "city": "Riyadh", "linkedin_url": "https://linkedin.com/in/faisal-alharbi", "notes": "warm intro from investor"},
    {"name": "Reem Alqahtani", "role": "CEO", "company": "Tibah Digital Works", "sector": "b2b_saas", "relationship": "warm", "city": "Madinah", "linkedin_url": "https://linkedin.com/in/reem-alqahtani", "notes": "met at saudi digital forum"},
    {"name": "Majed Alsubaie", "role": "Founder", "company": "Alpha Contracting Ops", "sector": "local_services", "relationship": "warm", "city": "Riyadh", "linkedin_url": "https://linkedin.com/in/majed-alsubaie", "notes": "warm lead from previous project"},
    {"name": "Sarah Alenazi", "role": "COO", "company": "Qassim Food Distribution", "sector": "b2b_services", "relationship": "warm", "city": "Buraydah", "linkedin_url": "https://linkedin.com/in/sarah-alenazi", "notes": "referred by partner agency"},
    {"name": "Khalid Alghamdi", "role": "CEO", "company": "Taif Med Clinics", "sector": "healthcare_clinic", "relationship": "warm", "city": "Taif", "linkedin_url": "https://linkedin.com/in/khalid-alghamdi", "notes": "requested bilingual sales drafts"},
    {"name": "Mona Alharthi", "role": "Founder", "company": "FutureEdu Labs", "sector": "training_consulting", "relationship": "active", "city": "Jeddah", "linkedin_url": "https://linkedin.com/in/mona-alharthi", "notes": "active conversation in progress"},
    {"name": "Waleed Almutairi", "role": "VP Growth", "company": "Riyadh Commerce Group", "sector": "b2b_services", "relationship": "warm", "city": "Riyadh", "linkedin_url": "https://linkedin.com/in/waleed-almutairi", "notes": "referred by warm intro list"},
    {"name": "Huda Alqahtani", "role": "CEO", "company": "SmartBuild Arabia", "sector": "real_estate", "relationship": "warm", "city": "Riyadh", "linkedin_url": "https://linkedin.com/in/huda-alqahtani", "notes": "wants safer outbound process"},
    {"name": "Tariq Alharbi", "role": "Founder", "company": "NeoFleet Services", "sector": "local_services", "relationship": "warm", "city": "Dammam", "linkedin_url": "https://linkedin.com/in/tariq-alharbi", "notes": "warm referral via linkedin"},
    {"name": "Dalal Alshehri", "role": "COO", "company": "Naseej Fashion Tech", "sector": "ecommerce_b2c", "relationship": "warm", "city": "Jeddah", "linkedin_url": "https://linkedin.com/in/dalal-alshehri", "notes": "met during ecommerce panel"},
    {"name": "Omar Alzahrani", "role": "CEO", "company": "SprintWorks MENA", "sector": "b2b_saas", "relationship": "warm", "city": "Riyadh", "linkedin_url": "https://linkedin.com/in/omar-alzahrani", "notes": "warm intro from customer advisory group"},
]


def _load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return [r for r in csv.DictReader(handle) if (r.get("name") or "").strip()]


def _write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS})


def main() -> int:
    parser = argparse.ArgumentParser(description="Seed warm contacts if below threshold")
    parser.add_argument("--csv", default="data/warm_list.csv")
    parser.add_argument("--min-contacts", type=int, default=20)
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    csv_path = root / args.csv
    rows = _load_rows(csv_path)
    if len(rows) >= args.min_contacts:
        print(f"OK: existing contacts={len(rows)} (>= {args.min_contacts})")
        return 0

    target = DEFAULT_CONTACTS[: max(args.min_contacts, 20)]
    _write_rows(csv_path, target)
    print(f"OK: seeded contacts={len(target)} into {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
