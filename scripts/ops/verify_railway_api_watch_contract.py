#!/usr/bin/env python3
"""Verify Dealix API Railway watch paths against the canonical source contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAILWAY_JSON = ROOT / "railway.json"
SERVICE_MATRIX = ROOT / "dealix" / "config" / "railway_services.json"


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"{path.name} root must be an object")
    return payload


def main() -> int:
    railway = _load(RAILWAY_JSON)
    matrix = _load(SERVICE_MATRIX)

    candidates = [
        item
        for item in matrix.get("services", [])
        if isinstance(item, dict)
        and item.get("role") == "canonical_api"
        and item.get("productionAuthority") is True
    ]
    if len(candidates) != 1:
        print("RAILWAY_API_WATCH_CONTRACT=FAIL reason=canonical_api_authority_count")
        return 1

    expected = candidates[0].get("expectedWatchPatterns")
    actual = (railway.get("build") or {}).get("watchPatterns")
    if not isinstance(expected, list) or not expected:
        print("RAILWAY_API_WATCH_CONTRACT=FAIL reason=expected_watch_patterns_missing")
        return 1
    if actual != expected:
        print("RAILWAY_API_WATCH_CONTRACT=FAIL reason=railway_json_watch_pattern_drift")
        print(f"EXPECTED_PATTERN_COUNT={len(expected)}")
        print(f"ACTUAL_PATTERN_COUNT={len(actual) if isinstance(actual, list) else 0}")
        return 1

    minimum = {
        "/*.py",
        "/**/*.py",
        "/Dockerfile",
        "/railway.json",
        "/pyproject.toml",
        "/requirements*.txt",
        "/scripts/railway_predeploy.sh",
    }
    missing = sorted(minimum.difference(actual))
    if missing:
        print("RAILWAY_API_WATCH_CONTRACT=FAIL reason=minimum_runtime_patterns_missing")
        print(f"MISSING_PATTERN_COUNT={len(missing)}")
        return 1

    print(f"RAILWAY_API_WATCH_PATTERN_COUNT={len(actual)}")
    print("RAILWAY_API_PYTHON_RUNTIME_CHANGES_TRIGGER_DEPLOY=true")
    print("RAILWAY_API_WATCH_CONTRACT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
