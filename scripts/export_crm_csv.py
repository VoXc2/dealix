"""Export CRM to CSV.

Usage:
    python3 scripts/export_crm_csv.py
"""
from __future__ import annotations

import csv
import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"
OUT_DIR = REPO_ROOT / "business" / "crm" / "exports"
OUT_DIR.mkdir(parents=True, exist_ok=True)


FIELDS = [
    "account_id",
    "account_name",
    "sector",
    "city",
    "website",
    "score",
    "priority",
    "recommended_offer",
    "stage",
    "next_action",
    "follow_up_date",
    "review_status",
    "source",
    "source_url_or_note",
]


def main() -> int:
    if not LEADS_PATH.exists():
        print(f"missing: {LEADS_PATH}")
        return 1
    data = json.loads(LEADS_PATH.read_text(encoding="utf-8"))
    accounts = data.get("accounts", [])

    today = dt.date.today().isoformat()
    out = OUT_DIR / f"dealix-crm-export-{today}.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for a in accounts:
            row = {
                "account_id": a.get("id", ""),
                "account_name": a.get("name", ""),
                "sector": a.get("segment", ""),
                "city": a.get("city", ""),
                "website": a.get("website", ""),
                "score": a.get("score", 0),
                "priority": "high" if a.get("score", 0) >= 70 else "medium" if a.get("score", 0) >= 50 else "low",
                "recommended_offer": a.get("recommendedOffer", ""),
                "stage": a.get("stage", ""),
                "next_action": a.get("nextAction", ""),
                "follow_up_date": a.get("nextActionDate", ""),
                "review_status": a.get("reviewStatus", ""),
                "source": a.get("sourceType", ""),
                "source_url_or_note": a.get("sourceNote", ""),
            }
            w.writerow(row)
    print(f"wrote {out} ({len(accounts)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
