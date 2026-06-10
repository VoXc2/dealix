#!/usr/bin/env python3
"""Validate .env.railway.*.generated — no secrets printed, only missing placeholders."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = re.compile(
    r"CHANGE_ME|REPLACE_|REPLACE$|<paste|<your_|sk_live_CHANGE|phc_CHANGE",
    re.I,
)

REQUIRED_API = (
    "DATABASE_URL",
    "APP_SECRET_KEY",
    "ENVIRONMENT",
    "CORS_ORIGINS",
    "ADMIN_API_KEYS",
    "MOYASAR_SECRET_KEY",
    "MOYASAR_WEBHOOK_SECRET",
    "POSTHOG_API_KEY",
    "CALENDLY_URL",
)
REQUIRED_FE = (
    "NEXT_PUBLIC_API_URL",
    "NEXT_PUBLIC_SITE_URL",
    "NEXT_PUBLIC_USE_DEALIX_OPS_PROXY",
    "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY",
    "DEALIX_ADMIN_API_KEY",
)


def _load_dotenv(path: Path) -> int:
    if not path.is_file():
        return 0
    loaded = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        if not key or key in os.environ:
            continue
        os.environ[key] = val.strip().strip('"').strip("'")
        loaded += 1
    return loaded


def _parse(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        out[key.strip()] = val.strip()
    return out


def _env_snapshot(keys: tuple[str, ...]) -> dict[str, str]:
    return {k: (os.getenv(k) or "").strip() for k in keys}


def _check_env(keys: tuple[str, ...], *, label: str) -> list[str]:
    issues: list[str] = []
    for key in keys:
        val = (os.getenv(key) or "").strip()
        if not val:
            issues.append(f"{label}: missing {key}")
        elif PLACEHOLDER.search(val):
            issues.append(f"{label}: placeholder {key}")
    cal = os.getenv("CALENDLY_WEBHOOK_SECRET") or os.getenv("CALENDLY_WEBHOOK_SIGNING_KEY", "")
    if "CALENDLY" in label or keys == REQUIRED_API:
        if not cal:
            issues.append(f"{label}: missing CALENDLY_WEBHOOK_SECRET or SIGNING_KEY")
        elif PLACEHOLDER.search(cal):
            issues.append(f"{label}: placeholder Calendly webhook")
    return issues


def _check_file(path: Path, required: tuple[str, ...]) -> list[str]:
    issues: list[str] = []
    env = _parse(path)
    if not env:
        return [f"missing file: {path.name}"]
    for key in required:
        val = env.get(key, "")
        if not val:
            issues.append(f"{path.name}: missing {key}")
        elif PLACEHOLDER.search(val):
            issues.append(f"{path.name}: placeholder {key}")
    if path.name.startswith(".env.railway.generated"):
        cal = env.get("CALENDLY_WEBHOOK_SECRET") or env.get("CALENDLY_WEBHOOK_SIGNING_KEY", "")
        if not cal:
            issues.append(f"{path.name}: missing CALENDLY_WEBHOOK_SECRET or SIGNING_KEY")
        elif PLACEHOLDER.search(cal):
            issues.append(f"{path.name}: placeholder Calendly webhook")
    return issues


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--from-railway-env",
        action="store_true",
        help="Load generated env into process before validating (uses exported + file values)",
    )
    args = p.parse_args()

    api = ROOT / ".env.railway.generated"
    fe = ROOT / ".env.railway.frontend.generated"

    if args.from_railway_env:
        n = _load_dotenv(api) + _load_dotenv(fe)
        if n:
            print(f"  loaded {n} keys from railway generated files (not printed)")
        issues = _check_env(REQUIRED_API, label="api")
        issues.extend(_check_env(REQUIRED_FE, label="frontend"))
    else:
        issues = _check_file(api, REQUIRED_API)
        issues.extend(_check_file(fe, REQUIRED_FE))

    print("== validate_railway_generated_env ==")
    if issues:
        for i in issues:
            print(f"  FAIL: {i}")
        print("RAILWAY_GENERATED_ENV=INCOMPLETE")
        return 1
    print("  ok: API + Frontend generated env complete (no placeholders)")
    print("RAILWAY_GENERATED_ENV=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
