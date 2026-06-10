#!/usr/bin/env python3
"""Validate Dealix environment templates.

This script intentionally has no third-party dependencies so it can run early in CI.
It checks for duplicate keys, malformed assignments, unsafe public-admin exposure hints,
and required production variables in backend and frontend env templates.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_TEMPLATE = ROOT / ".env.example"
WEB_ENV_TEMPLATE = ROOT / "apps" / "web" / ".env.example"

ASSIGNMENT = re.compile(r"^([A-Z][A-Z0-9_]*)=(.*)$")

REQUIRED_KEYS = {
    "ENVIRONMENT",
    "LOG_LEVEL",
    "APP_SECRET_KEY",
    "DATABASE_URL",
    "APP_URL",
    "ADMIN_API_KEYS",
    "CORS_ORIGINS",
}

REQUIRED_WEB_KEYS = {
    "NEXT_PUBLIC_SITE_URL",
    "NEXT_PUBLIC_API_URL",
    "NEXT_PUBLIC_USE_DEALIX_OPS_PROXY",
}

PUBLIC_ADMIN_KEYS = {
    "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY",
}


def parse_env(path: Path) -> tuple[dict[str, list[tuple[int, str]]], list[str]]:
    keys: dict[str, list[tuple[int, str]]] = defaultdict(list)
    errors: list[str] = []

    if not path.exists():
        return keys, [f"Missing env template: {path}"]

    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = ASSIGNMENT.match(line)
        if not match:
            errors.append(f"{path}:{line_no}: malformed env assignment: {raw_line!r}")
            continue
        key, value = match.groups()
        keys[key].append((line_no, value))

    return keys, errors


def check_template(path: Path, required: set[str], label: str) -> list[str]:
    keys, errors = parse_env(path)

    duplicates = {key: rows for key, rows in keys.items() if len(rows) > 1}
    for key, rows in duplicates.items():
        locations = ", ".join(f"line {line_no}" for line_no, _ in rows)
        errors.append(f"Duplicate env key {key} in {label} at {locations}")

    missing = sorted(required.difference(keys))
    for key in missing:
        errors.append(f"Missing required env key in {label}: {key}")

    for key in PUBLIC_ADMIN_KEYS.intersection(keys):
        values = [value for _, value in keys[key]]
        if any("ADMIN" in value.upper() or "REPLACE_same_as_ADMIN" in value for value in values):
            errors.append(
                f"{key} appears to expose an admin credential to the browser. "
                "Prefer NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1 with a server-side key."
            )

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(check_template(ENV_TEMPLATE, REQUIRED_KEYS, ".env.example"))
    errors.extend(check_template(WEB_ENV_TEMPLATE, REQUIRED_WEB_KEYS, "apps/web/.env.example"))

    if errors:
        print("Environment contract check failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Environment contract OK: backend and frontend templates checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
