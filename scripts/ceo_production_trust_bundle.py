#!/usr/bin/env python3
"""Production + trust close bundle for CEO Master Plan P0."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.railway_production import (  # noqa: E402
    DEFAULT_API_BASE,
    probe_trust_layer,
)

DNS_DOC = ROOT / "docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=DEFAULT_API_BASE)
    p.add_argument("--write-cache", action="store_true", help="Refresh production_layers_cache.json")
    args = p.parse_args()

    trust = probe_trust_layer(args.api_base.rstrip("/"))
    version_ok = (trust.get("probes") or {}).get("version", {}).get("ok")
    meta_ok = (trust.get("probes") or {}).get("api_v1_meta", {}).get("ok")
    healthz = (trust.get("probes") or {}).get("healthz", {})
    healthz_snippet = (healthz.get("snippet") or "").lower()
    healthz_rich = "version" in healthz_snippet

    print("== CEO Production Trust Bundle ==")
    print(f"  api: {args.api_base}")
    print(f"  /version ok: {version_ok}")
    print(f"  /api/v1/meta ok: {meta_ok}")
    print(f"  /healthz has version: {healthz_rich}")
    print(f"  dns_runbook: {DNS_DOC.relative_to(ROOT)}")
    print("  sentry: set SENTRY_DSN in Railway + .env (see .env.example)")

    if args.write_cache:
        cmd = [sys.executable, str(ROOT / "scripts/production_layers_verify.py"), "--write-cache"]
        subprocess.run(cmd, cwd=ROOT, check=False)

    ready = version_ok and meta_ok and healthz_rich
    print(f"\nCEO_PRODUCTION_TRUST_VERDICT={'PASS' if ready else 'OPEN'}")
    if not ready:
        print("FOUNDER_ACTION: DNS dealix.me → Railway + redeploy API (scripts/railway_redeploy_checklist.py)")

    if args.write_cache:
        cache_path = ROOT / "dealix/transformation/production_layers_cache.json"
        if cache_path.is_file():
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
            print(f"  layers_cache: {cache.get('verdict')} {cache.get('overall_pct')}%")

    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
