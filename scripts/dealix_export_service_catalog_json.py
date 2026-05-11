#!/usr/bin/env python3
"""Wave 15 §B2 — Export Service Catalog truth registry to static JSON.

Source of truth: auto_client_acquisition/service_catalog/registry.py.
Output: landing/assets/data/services-catalog.json (committed to git).

This enables:
- /services.html dynamic-load-and-validate (frontend can fetch + compare
  to hard-coded HTML to detect drift)
- Mobile clients / external integrations to read the catalog without
  invoking the API
- Single-command verification that the on-disk JSON matches the
  in-code registry (run this script in CI; diff against committed file)

Hard rules:
- Article 4: NEVER includes `live_send` or `live_charge` in
  action_modes_used (validated by ServiceOffering schema in registry)
- Article 8: every numeric carries `is_estimate=True`
- Article 11: ONLY data export — no business logic. Single source of
  truth remains the registry.

Usage:
    python3 scripts/dealix_export_service_catalog_json.py            # write
    python3 scripts/dealix_export_service_catalog_json.py --check    # verify
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

# Adjust path so we can import from repo root when run as script.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.service_catalog.registry import list_offerings  # noqa: E402

_OUT_PATH = REPO_ROOT / "landing" / "assets" / "data" / "services-catalog.json"


def build_catalog_dict() -> dict:
    """Compose the canonical JSON payload."""
    offerings = [o.model_dump(mode="json") for o in list_offerings()]
    return {
        "schema_version": "1.0",
        "source": "auto_client_acquisition/service_catalog/registry.py",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "constitution": {
            "article_4_hard_gates": [
                "no_live_send", "no_live_charge", "no_cold_whatsapp",
                "no_linkedin_auto", "no_scraping", "no_fake_proof",
                "no_fake_revenue", "no_blast",
            ],
            "article_8_no_fake_claims": True,
            "article_11_single_source_of_truth": True,
        },
        "count": len(offerings),
        "offerings": offerings,
    }


def write_json(payload: dict) -> None:
    _OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _OUT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def check_json(payload: dict) -> bool:
    """Return True iff on-disk JSON matches the in-code registry."""
    if not _OUT_PATH.exists():
        return False
    on_disk = json.loads(_OUT_PATH.read_text(encoding="utf-8"))
    # Compare structural fields only (ignore generated_at timestamp drift)
    keys_compare = ("schema_version", "source", "constitution", "count", "offerings")
    return all(on_disk.get(k) == payload.get(k) for k in keys_compare)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="Exit 0 if on-disk JSON matches registry, else 1.",
    )
    args = parser.parse_args()

    payload = build_catalog_dict()

    if args.check:
        if check_json(payload):
            print(f"OK · {_OUT_PATH.relative_to(REPO_ROOT)} matches registry ({payload['count']} offerings)")
            return 0
        print(
            f"FAIL · {_OUT_PATH.relative_to(REPO_ROOT)} is out of sync.\n"
            f"  Run: python3 scripts/dealix_export_service_catalog_json.py",
            file=sys.stderr,
        )
        return 1

    write_json(payload)
    print(f"WROTE · {_OUT_PATH.relative_to(REPO_ROOT)} · {payload['count']} offerings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
