"""V10 Run All.

Usage:
    python3 scripts/dealix_v10_run_all.py
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
    ("Daily operator (demo)", "scripts/dealix_daily_operator.py", ["--mode", "demo"]),
    ("AI evals (demo)", "scripts/run_ai_evals.py", ["--mode", "demo"]),
    ("Content calendar (30 days)", "scripts/generate_content_calendar.py", ["--days", "30"]),
    ("Campaign: revenue-os", "scripts/generate_campaign_pack.py", ["--campaign", "revenue-os", "--lang", "both"]),
    ("Demo pack", "scripts/generate_demo_pack.py", ["--lang", "both"]),
    ("Release notes", "scripts/generate_release_notes.py", []),
    ("Health snapshot", "scripts/generate_health_snapshot.py", []),
    ("Production readiness", "scripts/production_readiness_check.py", []),
    ("Pre-push guard", "scripts/pre_push_guard.py", []),
]


def main() -> int:
    print("Dealix V10 Run All")
    print("=" * 50)
    passed = 0
    for label, rel, extra in STEPS:
        path = REPO_ROOT / rel
        if not path.exists():
            print(f"[{label}]  SKIP")
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
    return 0 if passed == len(STEPS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
