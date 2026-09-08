#!/usr/bin/env python3
"""Fail-closed source contract for the canonical Railway API runtime.

This verifier protects Dealix from two provider/source drift classes that have
already caused or could cause skipped/broken production releases:

1. a Railway UI/runtime start-command override such as ``./start.sh`` taking
   precedence over the Dockerfile's canonical ``CMD [\"/app/start.sh\"]``;
2. API Watch Paths losing canonical runtime trees (``/api/**``, ``/app/**``,
   ``/db/**``) so relevant changes do not trigger a deployment candidate.

It validates repository authority only. A PASS is not proof that Railway's live
provider configuration matches the source contract and is never Production
Green evidence by itself.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RAILWAY_JSON = ROOT / "railway.json"
SERVICE_MATRIX = ROOT / "dealix/config/railway_services.json"
DOCKERFILE = ROOT / "Dockerfile"

CANONICAL_RUNTIME_TREES = {"/api/**", "/app/**", "/db/**"}
FORBIDDEN_START_OVERRIDES = {"./start.sh", "start.sh"}


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} must contain an object")
    return payload


def _canonical_api(matrix: dict[str, Any]) -> dict[str, Any]:
    services = matrix.get("services")
    if not isinstance(services, list):
        raise AssertionError("railway service matrix services must be a list")
    candidates = [
        service
        for service in services
        if isinstance(service, dict)
        and service.get("role") == "canonical_api"
        and service.get("productionAuthority") is True
    ]
    if len(candidates) != 1:
        raise AssertionError(
            f"exactly one canonical production API is required, found {len(candidates)}"
        )
    return candidates[0]


def verify() -> dict[str, Any]:
    railway = _load_json(RAILWAY_JSON)
    matrix = _load_json(SERVICE_MATRIX)
    api = _canonical_api(matrix)

    build = railway.get("build")
    deploy = railway.get("deploy")
    if not isinstance(build, dict) or not isinstance(deploy, dict):
        raise AssertionError("railway.json requires build and deploy objects")

    actual_watch = set(build.get("watchPatterns") or [])
    expected_watch = set(api.get("expectedWatchPatterns") or [])

    missing_source = CANONICAL_RUNTIME_TREES - actual_watch
    missing_matrix = CANONICAL_RUNTIME_TREES - expected_watch
    if missing_source:
        raise AssertionError(
            f"railway.json missing canonical API watch paths: {sorted(missing_source)}"
        )
    if missing_matrix:
        raise AssertionError(
            "railway service authority missing canonical API watch paths: "
            f"{sorted(missing_matrix)}"
        )
    if actual_watch != expected_watch:
        raise AssertionError(
            "railway.json watchPatterns must equal canonical API expectedWatchPatterns; "
            f"source_only={sorted(actual_watch - expected_watch)} "
            f"matrix_only={sorted(expected_watch - actual_watch)}"
        )

    start_command = deploy.get("startCommand")
    if start_command in FORBIDDEN_START_OVERRIDES:
        raise AssertionError(
            f"forbidden Railway start override {start_command!r}; use null/empty and Dockerfile CMD"
        )
    if start_command not in (None, ""):
        raise AssertionError(
            "canonical API railway.json startCommand must be null/empty; "
            f"got {start_command!r}"
        )

    dockerfile = DOCKERFILE.read_text(encoding="utf-8")
    required_docker_markers = (
        "> /app/start.sh",
        'CMD ["/app/start.sh"]',
        'WORKDIR /app',
    )
    missing_markers = [marker for marker in required_docker_markers if marker not in dockerfile]
    if missing_markers:
        raise AssertionError(
            f"Dockerfile missing canonical API runtime markers: {missing_markers}"
        )

    return {
        "status": "PASS_SOURCE_CONTRACT_ONLY",
        "start_command": start_command,
        "watch_patterns": sorted(actual_watch),
        "canonical_runtime_trees": sorted(CANONICAL_RUNTIME_TREES),
        "provider_parity_proven": False,
        "production_green": False,
        "l5_executed": "NONE",
    }


def main() -> int:
    result = verify()
    print(json.dumps(result, sort_keys=True))
    print("RAILWAY_RUNTIME_DRIFT_GATE=PASS_SOURCE_CONTRACT_ONLY")
    print("PROVIDER_PARITY_PROVEN=false")
    print("PRODUCTION_GREEN=false")
    print("L5_EXECUTED=NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
