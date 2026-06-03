#!/usr/bin/env python3
"""Merge founder closure env from local .env into Railway generated files (no values printed)."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PLACEHOLDER = re.compile(
    r"CHANGE_ME|REPLACE_|REPLACE$|<paste|<your_|sk_live_CHANGE|phc_CHANGE",
    re.I,
)

ENV_KEYS = (
    "SENTRY_DSN",
    "MOYASAR_SECRET_KEY",
    "MOYASAR_WEBHOOK_SECRET",
    "POSTHOG_API_KEY",
    "POSTHOG_HOST",
    "CALENDLY_URL",
    "CALENDLY_WEBHOOK_SECRET",
    "CALENDLY_WEBHOOK_SIGNING_KEY",
    "HUBSPOT_ACCESS_TOKEN",
    "GMAIL_CLIENT_ID",
    "GMAIL_CLIENT_SECRET",
    "DATABASE_URL",
    "APP_SECRET_KEY",
    "ENVIRONMENT",
    "CORS_ORIGINS",
    "ADMIN_API_KEYS",
    "DEALIX_ADMIN_API_KEY",
    "DEALIX_API_KEY",
)

FE_KEYS = (
    "NEXT_PUBLIC_API_URL",
    "NEXT_PUBLIC_SITE_URL",
    "NEXT_PUBLIC_USE_DEALIX_OPS_PROXY",
    "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY",
    "DEALIX_ADMIN_API_KEY",
)

SOURCE_FILES = (
    ROOT / ".env.founder.closure.local",
    ROOT / ".env",
    ROOT / ".env.local",
)

TARGET_API = ROOT / ".env.railway.generated"
TARGET_FE = ROOT / ".env.railway.frontend.generated"


def _parse(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        out[key.strip()] = val.strip().strip('"').strip("'")
    return out


def _write_merged(path: Path, updates: dict[str, str]) -> list[str]:
    changed: list[str] = []
    existing = _parse(path)
    lines: list[str] = []
    if path.is_file():
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                lines.append(raw.rstrip())
                continue
            key = line.partition("=")[0].strip()
            if key in updates:
                lines.append(f"{key}={updates[key]}")
                if existing.get(key) != updates[key]:
                    changed.append(key)
                del updates[key]
            else:
                lines.append(raw.rstrip())
    else:
        lines = [f"# {path.name}"]
    for key, val in updates.items():
        lines.append(f"{key}={val}")
        changed.append(key)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return changed


def _collect_sources() -> dict[str, str]:
    merged: dict[str, str] = {}
    for src in SOURCE_FILES:
        for key, val in _parse(src).items():
            if not val or PLACEHOLDER.search(val):
                continue
            merged.setdefault(key, val)
    return merged


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    sources = _collect_sources()
    if not sources:
        print("FOUNDER_CLOSURE_ENV=SKIP (no local env sources)")
        return 0

    api_updates = {k: sources[k] for k in ENV_KEYS if k in sources}
    fe_updates = {k: sources[k] for k in FE_KEYS if k in sources}

    admin = (
        sources.get("DEALIX_ADMIN_API_KEY")
        or sources.get("ADMIN_API_KEYS", "").split(",")[0].strip()
        or sources.get("DEALIX_API_KEY")
    )
    if admin:
        api_updates.setdefault("ADMIN_API_KEYS", admin)
        api_updates.setdefault("DEALIX_ADMIN_API_KEY", admin)
        api_updates.setdefault("DEALIX_API_KEY", admin)
        fe_updates.setdefault("NEXT_PUBLIC_DEALIX_ADMIN_API_KEY", admin)
        fe_updates.setdefault("DEALIX_ADMIN_API_KEY", admin)

    api_updates.setdefault("NEXT_PUBLIC_API_URL", "https://api.dealix.me")
    fe_updates.setdefault("NEXT_PUBLIC_API_URL", "https://api.dealix.me")
    fe_updates.setdefault("NEXT_PUBLIC_SITE_URL", "https://dealix.me")
    fe_updates.setdefault("NEXT_PUBLIC_USE_DEALIX_OPS_PROXY", "1")

    cal = sources.get("CALENDLY_WEBHOOK_SECRET") or sources.get("CALENDLY_WEBHOOK_SIGNING_KEY")
    if cal:
        api_updates.setdefault("CALENDLY_WEBHOOK_SECRET", cal)

    print("== apply_founder_closure_env ==")
    if args.dry_run:
        print(f"  would merge {len(api_updates)} api keys, {len(fe_updates)} fe keys (not printed)")
        return 0

    api_changed = _write_merged(TARGET_API, api_updates) if api_updates else []
    fe_changed = _write_merged(TARGET_FE, fe_updates) if fe_updates else []

    sync = subprocess.run(
        [sys.executable, str(ROOT / "scripts/sync_railway_generated_env.py")],
        cwd=ROOT,
        check=False,
    )
    validate = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_railway_generated_env.py"),
            "--from-railway-env",
        ],
        cwd=ROOT,
        check=False,
    )

    if api_changed:
        print(f"  api updated: {', '.join(sorted(set(api_changed)))}")
    if fe_changed:
        print(f"  fe updated: {', '.join(sorted(set(fe_changed)))}")

    if validate.returncode == 0:
        print("FOUNDER_CLOSURE_ENV=OK")
        return 0 if sync.returncode == 0 else sync.returncode

    print("FOUNDER_CLOSURE_ENV=INCOMPLETE (run validate_railway_generated_env for details)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
