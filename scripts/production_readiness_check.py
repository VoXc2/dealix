"""Production readiness check.

Usage:
    python3 scripts/production_readiness_check.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    ("No secrets", [sys.executable, str(REPO_ROOT / "scripts" / "check_no_secrets.py")]),
    ("Master verification", [sys.executable, str(REPO_ROOT / "scripts" / "verify_dealix_ultimate_os.py")]),
    ("Daily operator (demo)", [sys.executable, str(REPO_ROOT / "scripts" / "dealix_daily_operator.py"), "--mode", "demo"]),
    ("Founder dashboard data", [sys.executable, str(REPO_ROOT / "scripts" / "generate_founder_dashboard_data.py"), "--mode", "demo"]),
    ("Test: no auto-send", [sys.executable, "-c", "from tests.test_no_auto_send import test_no_auto_send; test_no_auto_send(); print('OK')"]),
]


def main() -> int:
    print("Dealix production readiness check")
    print("=" * 50)
    passed = 0
    for label, cmd in CHECKS:
        print(f"\n[{label}]")
        r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            passed += 1
            print(r.stdout.strip())
        else:
            print("FAIL")
            print(r.stdout.strip())
            print(r.stderr.strip())
    print("\n" + "=" * 50)
    print(f"{passed}/{len(CHECKS)} checks passed")
    return 0 if passed == len(CHECKS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
