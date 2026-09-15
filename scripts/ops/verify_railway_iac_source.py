#!/usr/bin/env python3
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IAC = ROOT / ".railway" / "railway.ts"
README = ROOT / ".railway" / "README.md"
CUTOFF = date(2026, 12, 1)


def require(text: str, needle: str) -> None:
    if needle not in text:
        raise SystemExit(f"RAILWAY_IAC_VERIFY=HOLD missing={needle}")


def main() -> int:
    text = IAC.read_text(encoding="utf-8")
    for needle in (
        'project("Dealix"', 'service("dealix"', 'service("web"',
        'postgres("Postgres"', 'rootDirectory: "."',
        'rootDirectory: "apps/web"', 'checkSuites: true',
        'healthcheck: "/healthz"', 'dockerfilePath: "Dockerfile"',
        '/scripts/railway_predeploy.sh', '/api/**', '/app/**', '/db/**',
        '/dealix/**', '/alembic/**', '/alembic.ini',
    ):
        require(text, needle)
    for needle in (
        '/config/**', '/templates/**', '/prompts/**',
        'domains: ["api.dealix.me"]',
        'domains: ["dealix.me", "www.dealix.me"]', 'preserve()',
    ):
        require(text, needle)
    if re.search(r"(?:sk-|ghp_|Bearer )[A-Za-z0-9._-]{8,}", text):
        raise SystemExit("RAILWAY_IAC_VERIFY=HOLD raw_secret_literal")

    readme = README.read_text(encoding="utf-8")
    require(readme, "2026-12-01")
    require(readme, "Never run `railway config apply`")
    remaining = (CUTOFF - date.today()).days
    if remaining < 0:
        raise SystemExit("RAILWAY_IAC_VERIFY=HOLD legacy_cutoff_elapsed")

    print("RAILWAY_IAC_SOURCE_VERIFY=PASS")
    print(f"LEGACY_CUTOFF_DAYS_REMAINING={remaining}")
    print("PROVIDER_APPLY_AUTHORITY=FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
