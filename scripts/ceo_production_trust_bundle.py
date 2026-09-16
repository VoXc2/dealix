#!/usr/bin/env python3
"""CEO wrapper around canonical self-host public exact-SHA release identity.

Reachability alone is insufficient: public Web/API must expose the accepted full SHA.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDENTITY_GATE = ROOT / "scripts/ops/verify_selfhost_public_release_identity.py"


def _identity_gate_command(args: argparse.Namespace) -> list[str]:
    return [sys.executable, str(IDENTITY_GATE), "--frontend-base", args.frontend_base, "--api-base", args.api_base, "--accepted-sha", args.accepted_sha]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default="https://api.dealix.me", help="Compatibility API base")
    p.add_argument("--frontend-base", default="https://dealix.me")
    p.add_argument("--api-health-url", help="Deprecated compatibility argument; ignored")
    p.add_argument("--web-provider-receipt", type=Path, help="Deprecated; self-host authority does not use provider receipts")
    p.add_argument("--api-provider-receipt", type=Path, help="Deprecated; self-host authority does not use provider receipts")
    p.add_argument("--accepted-sha", required=True)
    p.add_argument("--write-cache", action="store_true", help="Refresh production_layers_cache.json")
    args = p.parse_args()

    print("== CEO Production Trust Bundle ==")
    print("  authority: scripts/ops/verify_selfhost_public_release_identity.py")
    print(f"  frontend: {args.frontend_base}")
    print(f"  api: {args.api_base.rstrip('/')}/version")
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

    ready = proc.returncode == 0 and "SELFHOST_PUBLIC_RELEASE_IDENTITY=PASS" in proc.stdout

    if args.write_cache:
        cache_cmd = [sys.executable, str(ROOT / "scripts/production_layers_verify.py"), "--write-cache"]
        subprocess.run(cache_cmd, cwd=ROOT, check=False)

    print(f"CEO_PRODUCTION_TRUST_VERDICT={'PASS' if ready else 'HOLD'}")
    if not ready:
        print("NEXT_ACTION: align public Web/API to the accepted self-host SHA and re-run strict read-only identity verification; do not weaken the gate")
    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
