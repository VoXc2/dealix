#!/usr/bin/env python3
"""Production layer map — live probes + optional local env (--from-railway-env)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.production_layers import (  # noqa: E402
    build_production_layers,
    format_layers_report,
    write_layers_cache,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()

RAILWAY_ENV = ROOT / ".env.railway.generated"
RAILWAY_FE_ENV = ROOT / ".env.railway.frontend.generated"


def _load_dotenv_file(path: Path) -> int:
    """Load KEY=VALUE lines into os.environ (no overwrite). Returns count loaded."""
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


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"))
    p.add_argument("--frontend-base", default=os.getenv("DEALIX_FRONTEND_BASE", "https://dealix.me"))
    p.add_argument(
        "--from-railway-env",
        action="store_true",
        help="Load .env.railway.generated (+ frontend) for env layer checks",
    )
    p.add_argument("--check-env", action="store_true", help="Score layers using process env")
    p.add_argument("--write-cache", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true", help="Exit 1 unless verdict PASS")
    args = p.parse_args()

    if args.from_railway_env:
        n = _load_dotenv_file(RAILWAY_ENV)
        n += _load_dotenv_file(RAILWAY_FE_ENV)
        if n:
            print(f"  loaded {n} env keys from railway generated files (not printed)")
        args.check_env = True

    blob = build_production_layers(
        api_base=args.api_base,
        frontend_base=args.frontend_base,
        check_env=args.check_env,
    )

    if args.write_cache:
        rel = write_layers_cache(blob)
        print(f"  cache: {rel}")

    if args.json:
        import json

        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print(format_layers_report(blob))

    print(f"PRODUCTION_LAYERS_VERDICT={blob['verdict']}")
    print(f"PRODUCTION_LAYERS_PCT={blob['overall_pct']}")

    if args.strict and blob["verdict"] != "PASS":
        return 1
    return 0 if blob["verdict"] in ("PASS", "WARN") else 1


if __name__ == "__main__":
    raise SystemExit(main())
