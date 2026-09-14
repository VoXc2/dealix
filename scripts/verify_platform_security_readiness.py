#!/usr/bin/env python3
"""Deterministic platform-security readiness verifier (Omega V3).

Reports READY/HOLD per capability from
config/security/platform_security_readiness_v1.json plus environment
evidence. Config presence is never treated as operational proof.
No network access. Prints a receipt; exits 0 on READY or HOLD,
exits 2 only on hard violations (secret material, forbidden automerge)
or a non-closed receipt.

Usage:
    python3 scripts/verify_platform_security_readiness.py [--write-receipt PATH]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.platform_security.readiness import evaluate, receipt_is_closed


def _base_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Platform-security readiness verifier")
    parser.add_argument("--write-receipt", default="", help="Write receipt JSON to PATH")
    args = parser.parse_args()

    receipt = evaluate(base_commit=_base_commit())
    closed = receipt_is_closed(receipt)

    print(f"PLATFORM_SECURITY_STATUS={receipt['overall']}")
    for cap_id, cap in receipt["capabilities"].items():
        reasons = ",".join(cap["reasons"]) if cap["reasons"] else "ok"
        print(f"PLATFORM_SECURITY_{cap_id.upper()}={cap['status']} reasons={reasons}")
    print(f"PLATFORM_SECURITY_VIOLATIONS={','.join(receipt['violations']) or 'none'}")
    print(f"PLATFORM_SECURITY_RECEIPT_CLOSED={str(closed).lower()}")

    if args.write_receipt:
        Path(args.write_receipt).write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        print(f"PLATFORM_SECURITY_RECEIPT_PATH={args.write_receipt}")

    if not closed or receipt["violations"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
