#!/usr/bin/env python3
"""CEO wrapper around the canonical Railway production-identity gate.

This bundle intentionally does not invent a second definition of Production Green.
Reachability alone is insufficient: fresh provider receipts must bind the canonical
web and API services to the same accepted release SHA.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENTITY_GATE = ROOT / "scripts/railway_production_identity_gate.py"


def _identity_gate_command(args: argparse.Namespace) -> list[str]:
    api_health_url = args.api_health_url or f"{args.api_base.rstrip('/')}/healthz"
    cmd = [
        sys.executable,
        str(IDENTITY_GATE),
        "--frontend-base",
        args.frontend_base,
        "--api-health-url",
        api_health_url,
    ]
    if args.web_provider_receipt is not None:
        cmd += ["--web-provider-receipt", str(args.web_provider_receipt)]
    if args.api_provider_receipt is not None:
        cmd += ["--api-provider-receipt", str(args.api_provider_receipt)]
    if args.accepted_sha:
        cmd += ["--accepted-sha", args.accepted_sha]
    return cmd


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default="https://api.dealix.me", help="Compatibility API base")
    p.add_argument("--frontend-base", default="https://dealix.me")
    p.add_argument("--api-health-url")
    p.add_argument("--web-provider-receipt", type=Path)
    p.add_argument("--api-provider-receipt", type=Path)
    p.add_argument("--accepted-sha")
    p.add_argument("--write-cache", action="store_true", help="Refresh production_layers_cache.json")
    args = p.parse_args()

    print("== CEO Production Trust Bundle ==")
    print("  authority: scripts/railway_production_identity_gate.py")
    print(f"  frontend: {args.frontend_base}")
    print(f"  api: {args.api_health_url or args.api_base.rstrip('/') + '/healthz'}")
    print("  rule: HTTP reachability alone never proves Production Green")

    proc = subprocess.run(
        _identity_gate_command(args),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if proc.stdout:
        print(proc.stdout.rstrip())

    ready = proc.returncode == 0 and "RAILWAY_PRODUCTION_IDENTITY_GATE_VERDICT=PASS" in proc.stdout

    if args.write_cache:
        cache_cmd = [sys.executable, str(ROOT / "scripts/production_layers_verify.py"), "--write-cache"]
        subprocess.run(cache_cmd, cwd=ROOT, check=False)

    print(f"CEO_PRODUCTION_TRUST_VERDICT={'PASS' if ready else 'HOLD'}")
    if not ready:
        print("NEXT_ACTION: capture fresh read-only Railway web/API provider receipts bound to the accepted SHA; do not weaken the gate or mutate DNS/provider state to manufacture green")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
