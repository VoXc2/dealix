"""Pre-push guard.

Usage:
    python3 scripts/pre_push_guard.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

GUARDS = [
    ("Secrets", [sys.executable, str(REPO_ROOT / "scripts" / "check_no_secrets.py")]),
    ("Master verification", [sys.executable, str(REPO_ROOT / "scripts" / "verify_dealix_ultimate_os.py")]),
    ("Daily operator (demo)", [sys.executable, str(REPO_ROOT / "scripts" / "dealix_daily_operator.py"), "--mode", "demo"]),
    ("Production readiness", [sys.executable, str(REPO_ROOT / "scripts" / "production_readiness_check.py")]),
]


def main() -> int:
    print("Dealix pre-push guard")
    print("=" * 50)
    passed = 0
    for label, cmd in GUARDS:
        print(f"\n[{label}]")
        r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            passed += 1
            print("OK")
        else:
            print("FAIL")
            print(r.stdout[-1000:])
            print(r.stderr[-1000:])
    print("\n" + "=" * 50)
    print(f"{passed}/{len(GUARDS)} guards passed")
    return 0 if passed == len(GUARDS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
