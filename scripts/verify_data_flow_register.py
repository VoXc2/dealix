#!/usr/bin/env python3
"""Verify data flow register seed against JSON schema — PDPA readiness gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    try:
        import jsonschema
    except ImportError:
        print("SKIP jsonschema not installed")
        return 0

    schema_path = ROOT / "schemas" / "data_flow_entry.schema.json"
    seed_path = ROOT / "data" / "privacy" / "data_flow_register_seed.json"

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    seed = json.loads(seed_path.read_text(encoding="utf-8"))

    errors = []
    if not isinstance(seed, list):
        errors.append("seed must be a JSON array")
    else:
        for i, entry in enumerate(seed):
            try:
                jsonschema.validate(entry, schema)
            except jsonschema.ValidationError as e:
                errors.append(f"{entry.get('flow_id', i)}: {e.message}")

    if errors:
        for e in errors:
            print(f"FAIL {e}")
        return 1

    print(f"PASS data_flow_register ({len(seed)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
