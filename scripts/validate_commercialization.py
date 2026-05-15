#!/usr/bin/env python3
"""Validate customer-facing commercialization assets."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    errors: list[str] = []
    required_paths = [
        Path("intake/intake_schema.json"),
        Path("templates/proposal_bundle_ar.md"),
        Path("templates/offer_ar.md"),
        Path("templates/sow_ar.md"),
        Path("gtm/ICPs.json"),
        Path("gtm/positioning.md"),
    ]
    for path in required_paths:
        if not path.exists():
            errors.append(f"missing file: {path}")

    intake_schema = Path("intake/intake_schema.json")
    if intake_schema.exists():
        data = json.loads(intake_schema.read_text(encoding="utf-8"))
        required_keys = {"required_fields", "optional_fields"}
        missing = required_keys - set(data.keys())
        if missing:
            errors.append(f"intake_schema missing keys: {', '.join(sorted(missing))}")

    if errors:
        print("COMMERCIALIZATION_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("COMMERCIALIZATION_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
