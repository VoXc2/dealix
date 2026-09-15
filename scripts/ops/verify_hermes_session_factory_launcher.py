#!/usr/bin/env python3
"""Verify a rendered Hermes Session Factory launcher without executing it."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
STALE_RUNTIME_PREFIX = "/opt/dealix/control/runtime/session-factory-"
REQUIRED = (
    'git -C "$REPO" rev-parse HEAD',
    "HOLD_SOURCE_IDENTITY",
    "HOLD_DIRTY_SOURCE",
    '"$REPO/scripts/ops/session_factory_watchdog.py"',
    '"$REPO/scripts/ops/session_factory.py" recover',
    '"$REPO/scripts/ops/session_factory.py" tick',
    '"$REPO/scripts/ops/session_factory.py" status',
)


def verify_text(text: str, accepted_sha: str, repo: Path) -> list[str]:
    errors: list[str] = []
    if not FULL_SHA.fullmatch(accepted_sha):
        errors.append("accepted SHA is not exact-40 lowercase hex")
    if f"EXPECTED_SHA={accepted_sha}" not in text:
        errors.append("accepted SHA is not embedded")
    if f"REPO={repo}" not in text and f"REPO='{repo}'" not in text:
        errors.append("canonical repository path is not embedded")
    if STALE_RUNTIME_PREFIX in text:
        errors.append("stale frozen Session Factory runtime path remains")
    for marker in REQUIRED:
        if marker not in text:
            errors.append(f"missing required marker: {marker}")
    if re.search(r"(?im)^\s*(MODEL|PROVIDER|MODEL_ID)\s*=", text):
        errors.append("launcher must not mint model/provider authority")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--accepted-sha", required=True)
    parser.add_argument("--repo", type=Path, default=Path("/opt/dealix/workspace/dealix"))
    args = parser.parse_args()
    text = args.path.read_text(encoding="utf-8")
    errors = verify_text(text, args.accepted_sha, args.repo)
    if errors:
        for error in errors:
            print(f"HERMES_SESSION_FACTORY_LAUNCHER_ERROR={error}")
        return 1
    print("HERMES_SESSION_FACTORY_LAUNCHER_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
