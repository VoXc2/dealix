#!/usr/bin/env python3
"""Check Dealix OpenAPI contract stability.

If docs/architecture/openapi.json exists, this script exports the current schema
and compares it with the baseline. It reports removed paths and removed methods
as breaking changes. If no baseline exists, it still verifies that the schema can
be exported and explains how to create the baseline.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from export_openapi import export_openapi

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs" / "architecture" / "openapi.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        current_path = Path(tmp) / "openapi.json"
        export_openapi(current_path)
        current = load(current_path)

    if not BASELINE.exists():
        print("OpenAPI baseline not found: docs/architecture/openapi.json")
        print("Current schema exports successfully. Create a baseline with: make openapi-export")
        return 0

    baseline = load(BASELINE)
    baseline_paths = baseline.get("paths", {})
    current_paths = current.get("paths", {})

    errors: list[str] = []
    for path in sorted(set(baseline_paths) - set(current_paths)):
        errors.append(f"Removed API path: {path}")

    for path in sorted(set(baseline_paths) & set(current_paths)):
        old_methods = set(baseline_paths[path].keys())
        new_methods = set(current_paths[path].keys())
        for method in sorted(old_methods - new_methods):
            errors.append(f"Removed API method: {method.upper()} {path}")

    if errors:
        print("OpenAPI contract check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("OpenAPI contract OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
