#!/usr/bin/env python3
"""Export the governed public Dealix service-catalog projection.

The internal registry contains the full capability/experiment portfolio. The
public static catalog intentionally exposes only the current governed launch
path:

Free Mini Diagnostic -> qualified discovery -> customer-specific quote ->
Customer-specific Revenue Command Pilot -> governed delivery/proof; duration stays customer-specific.

This exporter validates the two public compatibility IDs against the internal
registry, but never copies internal/future fixed prices into the public file.
That separation preserves the current quote-only commercial authority.

Usage:
    python3 scripts/dealix_export_service_catalog_json.py
    python3 scripts/dealix_export_service_catalog_json.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.service_catalog.registry import get_offering

_OUT_PATH = REPO_ROOT / "landing" / "assets" / "data" / "services-catalog.json"


def _required_offering(offering_id: str):
    offering = get_offering(offering_id)
    if offering is None:
        raise RuntimeError(f"required public compatibility offering missing: {offering_id}")
    return offering


def build_catalog_dict() -> dict:
    """Build the deterministic public projection without leaking internal prices."""
    diagnostic = _required_offering("free_mini_diagnostic")
    pilot = _required_offering("revenue_command_pilot_30d")

    if diagnostic.price_sar != 0 or diagnostic.commercial_status != "free_entry":
        raise RuntimeError("free_mini_diagnostic commercial authority drift")
    if pilot.price_sar != 0 or pilot.commercial_status != "quote_only":
        raise RuntimeError("revenue_command_pilot_30d must remain quote-only")

    return {
        "schema_version": "2.0-public",
        "public_commercial_truth": "one_governed_path",
        "generated_for": "public_static_surface",
        "offerings": [
            {
                "id": diagnostic.id,
                "name_en": "Free Mini Diagnostic",
                "name_ar": diagnostic.name_ar,
                "pricing": "free",
                "commercial_status": "public_entry",
                "next_step": "qualified_discovery",
            },
            {
                "id": pilot.id,
                "name_en": "Revenue Command Pilot",
                "name_ar": "تجربة مركز قيادة الإيرادات",
                "duration": "customer_specific_after_qualified_discovery",
                "legacy_id_semantics": "identifier_only_no_fixed_duration_authority",
                "pricing": "customer_specific_quote_after_qualified_discovery",
                "commercial_status": "quote_only",
                "public_checkout": False,
                "customer_result_guarantee": False,
                "next_step": "governed_delivery_and_proof",
            },
        ],
        "claim_policy": {
            "synthetic_or_demo_is_customer_proof": False,
            "revenue_requires_payment_evidence": True,
            "testimonial_requires_publication_approval": True,
            "unsupported_certification_or_residency_claims": False,
        },
    }


def write_json(payload: dict) -> None:
    _OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _OUT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def check_json(payload: dict) -> bool:
    """Return True iff the committed public projection matches current authority."""
    if not _OUT_PATH.exists():
        return False
    try:
        on_disk = json.loads(_OUT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return on_disk == payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 0 if the committed public projection matches current authority.",
    )
    args = parser.parse_args()

    try:
        payload = build_catalog_dict()
    except Exception as exc:
        print(f"FAIL · public catalog authority validation failed: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if check_json(payload):
            print(
                "OK · "
                f"{_OUT_PATH.relative_to(REPO_ROOT)} matches governed public projection "
                f"({len(payload['offerings'])} offerings)"
            )
            return 0
        print(
            f"FAIL · {_OUT_PATH.relative_to(REPO_ROOT)} is out of sync with governed public authority.\n"
            "  Run: python3 scripts/dealix_export_service_catalog_json.py",
            file=sys.stderr,
        )
        return 1

    write_json(payload)
    print(
        f"WROTE · {_OUT_PATH.relative_to(REPO_ROOT)} · "
        f"{len(payload['offerings'])} governed public offerings"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
