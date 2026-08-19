#!/usr/bin/env python3
"""Run the existing Dealix production smoke test with safe API-key fallback.

The scheduled smoke workflow can carry a dedicated smoke key plus one or more
production-key aliases. A stale dedicated key must not mask a still-valid
fallback. This wrapper probes one read-only protected endpoint with each
configured candidate, never prints key values, then runs the canonical smoke
suite exactly once with the first candidate that gets past platform API-key
authentication.

Authenticated response-derived details are intentionally not written to CI
stdout or artifacts. The workflow uses the process exit code as its trust gate.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.dealix_smoke_test import (
    CHECKS,
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT,
    APIKeyCandidate,
    _do_request,
    _split_api_key_bundle,
    run,
)

_SINGLE_KEY_ENVS = (
    "DEALIX_SMOKE_API_KEY",
    "DEALIX_PRODUCTION_API_KEY",
    "DEALIX_READ_API_KEY",
    "DEALIX_API_KEY",
    "API_KEY",
)
_BUNDLE_KEY_ENVS = ("API_KEYS", "DEALIX_API_KEYS")


@dataclass(frozen=True)
class AuthSelection:
    candidate: APIKeyCandidate
    configured_count: int
    tried_count: int
    all_rejected: bool


def configured_api_key_candidates() -> list[APIKeyCandidate]:
    """Return configured API-key candidates in precedence order, deduplicated.

    Only environment variable names are retained as metadata. Secret values are
    used in memory solely to authenticate the read-only probe and smoke calls.
    """
    candidates: list[APIKeyCandidate] = []
    seen_values: set[str] = set()

    def add(value: str, source: str) -> None:
        normalized = value.strip()
        if not normalized or normalized in seen_values:
            return
        seen_values.add(normalized)
        candidates.append(APIKeyCandidate(value=normalized, source=source))

    for env_name in _SINGLE_KEY_ENVS:
        add(os.getenv(env_name, ""), env_name)

    for env_name in _BUNDLE_KEY_ENVS:
        for value in _split_api_key_bundle(os.getenv(env_name, "")):
            add(value, env_name)

    return candidates


def _auth_probe_check():
    """Use the first protected read-only smoke check as an auth probe."""
    for check in CHECKS:
        if check.method == "GET" and check.path.startswith("/api/"):
            return check
    raise RuntimeError("smoke suite has no protected GET endpoint for auth probing")


def select_api_key_candidate(
    base_url: str,
    timeout: float,
    candidates: list[APIKeyCandidate],
) -> AuthSelection:
    """Select the first candidate not rejected by platform API-key middleware.

    The middleware returns HTTP 401 for an invalid or missing X-API-Key. Any
    non-401 response means the candidate passed that platform gate; a later
    route-level 4xx/5xx remains a genuine smoke failure and is not hidden by
    trying another credential.
    """
    if not candidates:
        return AuthSelection(
            candidate=APIKeyCandidate(value="", source=""),
            configured_count=0,
            tried_count=0,
            all_rejected=False,
        )

    probe = _auth_probe_check()
    for index, candidate in enumerate(candidates, start=1):
        result = _do_request(
            base_url,
            probe,
            timeout,
            api_key=candidate.value,
        )
        if result.status != 401:
            return AuthSelection(
                candidate=candidate,
                configured_count=len(candidates),
                tried_count=index,
                all_rejected=False,
            )

    return AuthSelection(
        candidate=candidates[0],
        configured_count=len(candidates),
        tried_count=len(candidates),
        all_rejected=True,
    )


def _emit_non_secret_execution_marker(
    base_url: str,
    *,
    as_json: bool,
    canonical_smoke_executed: bool,
) -> None:
    """Emit only non-secret control-flow metadata after execution is known."""
    marker = {
        "schema_version": 1,
        "base_url": base_url,
        "canonical_smoke_executed": canonical_smoke_executed,
        "authenticated_details_logged": False,
        "result_source": "process_exit_code",
    }
    if as_json:
        print(json.dumps(marker, indent=2, ensure_ascii=False))
    else:
        print("Dealix production smoke")
        print(f"base_url: {base_url}")
        print(f"canonical_smoke_executed: {str(canonical_smoke_executed).lower()}")
        print("authenticated_details_logged: false")
        print("result_source: process_exit_code")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    candidates = configured_api_key_candidates()
    selection = select_api_key_candidate(args.base_url, args.timeout, candidates)
    if selection.all_rejected:
        _emit_non_secret_execution_marker(
            args.base_url,
            as_json=args.json,
            canonical_smoke_executed=False,
        )
        return 3

    internal_report = run(
        args.base_url,
        timeout=args.timeout,
        api_key=selection.candidate.value,
        api_key_source=selection.candidate.source,
    )
    _emit_non_secret_execution_marker(
        args.base_url,
        as_json=args.json,
        canonical_smoke_executed=True,
    )

    network_failures = sum(
        1 for row in internal_report["results"] if row["status"] is None
    )
    if network_failures == internal_report["total"]:
        return 2
    return 0 if internal_report["failed_required"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
