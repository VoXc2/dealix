"""CSV connector — imports leads from a local CSV.

Usage:
    python3 connectors/csv_connector.py --file data/imports/sample_leads.csv --demo
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from base import BaseConnector, ConnectorManifest
from normalizer import normalize_lead
from source_audit import audit


class CSVConnector(BaseConnector):
    manifest = ConnectorManifest(
        name="CSV import (local)",
        source_type="csv_import",
        allowed_use="Bulk upload from founder-supplied public lists",
        restricted_use=["Private lists", "Lists without source"],
        risk_level="low",
        notes="Always requires --file and --demo flags in V1.",
    )

    def fetch_or_load(self) -> list[dict]:
        return self._rows

    def normalize(self, raw: list[dict]) -> list[dict]:
        return [normalize_lead(r, "csv_import", str(self._source_note)) for r in raw]

    def validate(self, record: dict) -> bool:
        return bool(record.get("id")) and bool(record.get("name"))

    def run(self, file: Path, demo: bool) -> list[dict]:
        if not file.exists():
            raise FileNotFoundError(file)
        self._source_note = file
        with file.open("r", encoding="utf-8", newline="") as f:
            self._rows = list(csv.DictReader(f))
        normalized = self.normalize(self._rows)
        if demo:
            for n in normalized:
                n["demo"] = True
        valid = [n for n in normalized if self.validate(n)]
        audit(self, len(valid), self.root)
        return valid


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    c = CSVConnector()
    rows = c.run(args.file, args.demo)
    print(json.dumps({"count": len(rows), "sample": rows[:1]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
