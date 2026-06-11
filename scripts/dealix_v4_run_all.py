"""V4 Run All — master script.

Usage:
    bash scripts/dealix_v4_run_all.sh
    python scripts/dealix_v4_run_all.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    ("Secrets check", "scripts/check_no_secrets.py"),
    ("Master verification", "scripts/verify_dealix_ultimate_os.py"),
    ("Build first 100 leads plan", "scripts/build_first_100_leads_plan.py"),
    ("Daily operator (demo)", "scripts/dealix_daily_operator.py"),
    ("Launch brief", "scripts/generate_launch_brief.py"),
    ("Conversion scorecard", "scripts/generate_conversion_scorecard.py"),
    ("Proof report (demo)", "scripts/generate_proof_report.py"),
    ("Production readiness", "scripts/production_readiness_check.py"),
    ("Pre-push guard", "scripts/pre_push_guard.py"),
]


def main() -> int:
    print("Dealix V4 Run All")
    print("=" * 50)
    passed = 0
    for label, rel in STEPS:
        path = REPO_ROOT / rel
        if not path.exists():
            print(f"[{label}]  SKIP (not implemented in V4, see V5)")
            continue
        cmd = [sys.executable, str(path)]
        if "daily_operator" in rel:
            cmd += ["--mode", "demo"]
        elif "proof_report" in rel:
            cmd += ["--account-id", "demo-001", "--lang", "both"]
        elif "build_first_100" in rel:
            cmd += ["--mode", "demo"]
        elif "conversion_scorecard" in rel:
            pass
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
