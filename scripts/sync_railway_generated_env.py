#!/usr/bin/env python3
"""Sync generated Railway env files (no secret values printed)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_ENV = ROOT / ".env.railway.generated"
FE_ENV = ROOT / ".env.railway.frontend.generated"


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


def _write(path: Path, data: dict[str, str]) -> None:
    lines: list[str] = []
    if path.is_file():
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                lines.append(raw.rstrip())
                continue
            key = line.partition("=")[0].strip()
            if key in data:
                lines.append(f"{key}={data[key]}")
                del data[key]
            else:
                lines.append(raw.rstrip())
    else:
        lines = [f"# {path.name}"]
    for key, val in data.items():
        lines.append(f"{key}={val}")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    api = _parse(API_ENV)
    fe = _parse(FE_ENV)
    if not api and not fe:
        print("RAILWAY_ENV_SYNC=SKIP (no .env.railway.*.generated)")
        return 0

    admin = (
        fe.get("DEALIX_ADMIN_API_KEY")
        or fe.get("NEXT_PUBLIC_DEALIX_ADMIN_API_KEY")
        or api.get("DEALIX_ADMIN_API_KEY")
        or api.get("ADMIN_API_KEYS", "").split(",")[0].strip()
    )
    changes: list[str] = []
    if admin:
        if not fe.get("NEXT_PUBLIC_DEALIX_ADMIN_API_KEY"):
            fe["NEXT_PUBLIC_DEALIX_ADMIN_API_KEY"] = admin
            changes.append("FE:NEXT_PUBLIC_DEALIX_ADMIN_API_KEY")
        if not fe.get("DEALIX_ADMIN_API_KEY"):
            fe["DEALIX_ADMIN_API_KEY"] = admin
            changes.append("FE:DEALIX_ADMIN_API_KEY")
        if not api.get("DEALIX_ADMIN_API_KEY"):
            api["DEALIX_ADMIN_API_KEY"] = admin
            changes.append("API:DEALIX_ADMIN_API_KEY")
        if not api.get("DEALIX_API_KEY"):
            api["DEALIX_API_KEY"] = admin
            changes.append("API:DEALIX_API_KEY")

    for key, val in (
        ("NEXT_PUBLIC_API_URL", "https://api.dealix.me"),
        ("NEXT_PUBLIC_SITE_URL", "https://dealix.me"),
        ("NEXT_PUBLIC_USE_DEALIX_OPS_PROXY", "1"),
    ):
        if not fe.get(key):
            fe[key] = val
            changes.append(f"FE:{key}")

    if not changes:
        print("RAILWAY_ENV_SYNC=OK (already aligned)")
        return 0

    print("RAILWAY_ENV_SYNC=UPDATED")
    for c in changes:
        print(f"  {c}")
    if args.dry_run:
        print("  (dry-run — no files written)")
        return 0

    if fe:
        _write(FE_ENV, fe)
    if api:
        _write(API_ENV, api)
    print(f"  wrote: {API_ENV.name}, {FE_ENV.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
