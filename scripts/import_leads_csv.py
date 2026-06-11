"""Import leads from a CSV file into business/_data/leads.json.

Usage:
    python3 scripts/import_leads_csv.py --file data/imports/sample_leads.csv --demo
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LEADS_PATH = REPO_ROOT / "business" / "_data" / "leads.json"


REQUIRED_FIELDS = {"id", "name", "segment", "city", "sourceType", "sourceNote", "visibleSignal"}


def load_existing() -> list[dict]:
    if not LEADS_PATH.exists():
        return []
    try:
        data = json.loads(LEADS_PATH.read_text(encoding="utf-8"))
        return data.get("accounts", [])
    except json.JSONDecodeError:
        return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--demo", action="store_true", help="Mark every row as demo")
    parser.add_argument("--out", default=str(LEADS_PATH), help="Output JSON path")
    args = parser.parse_args()

    csv_path = Path(args.file)
    if not csv_path.exists():
        print(f"File not found: {csv_path}")
        return 1

    existing = load_existing()
    existing_ids = {a["id"] for a in existing}
    added: list[dict] = []
    skipped: list[str] = []

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            missing = REQUIRED_FIELDS - set(row.keys())
            if missing:
                skipped.append(f"row missing {missing}: {row}")
                continue
            if row["id"] in existing_ids:
                skipped.append(f"duplicate: {row['id']}")
                continue
            record = {
                "id": row["id"],
                "name": row["name"],
                "segment": row["segment"],
                "city": row.get("city", ""),
                "sourceType": row["sourceType"],
                "sourceNote": row["sourceNote"],
                "visibleSignal": row["visibleSignal"],
                "weaknessHypothesis": row.get("weaknessHypothesis", ""),
                "recommendedOffer": row.get("recommendedOffer", "diagnostic_sprint"),
                "score": int(row.get("score", 0) or 0),
                "stage": row.get("stage", "new"),
                "owner": row.get("owner", "Founder"),
                "reviewStatus": row.get("reviewStatus", "not_started"),
                "demo": args.demo or row.get("demo", "false").lower() == "true",
                "createdAt": row.get("createdAt", ""),
            }
            added.append(record)

    out = {"accounts": existing + added, "version": "1.0"}
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"added={len(added)} skipped={len(skipped)} -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
