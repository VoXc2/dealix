"""V6 Run All — verifies production data + auth + reliability foundations.

Usage:
    python3 scripts/dealix_v6_run_all.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    ("Secrets check", "scripts/check_no_secrets.py", []),
    ("Env check (demo)", "scripts/check_required_env.py", ["--mode", "demo"]),
    ("Master verification", "scripts/verify_dealix_ultimate_os.py", []),
    ("Backup business data", "scripts/backup_business_data.py", []),
    ("Check data integrity", "scripts/check_data_integrity.py", []),
    ("Env report", "scripts/generate_env_report.py", []),
    ("Ops health report", "scripts/generate_ops_health_report.py", []),
    ("Daily operator (demo)", "scripts/dealix_daily_operator.py", ["--mode", "demo"]),
    ("Production readiness", "scripts/production_readiness_check.py", []),
]


def main() -> int:
    print("Dealix V6 Run All")
    print("=" * 50)
    passed = 0
    for label, rel, extra in STEPS:
        path = REPO_ROOT / rel
        if not path.exists():
            print(f"[{label}]  SKIP (missing)")
            continue
        cmd = [sys.executable, str(path)] + extra
        print(f"\n[{label}]")
        r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            passed += 1
            print("OK")
        else:
            print("FAIL")
            print(r.stdout[-500:])
            print(r.stderr[-500:])
    print("\n" + "=" * 50)
    print(f"{passed} steps OK")
    return 0 if passed > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
