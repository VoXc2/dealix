"""V5 Run All — master script for the live revenue system.

Usage:
    python3 scripts/dealix_v5_run_all.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    ("Secrets check", "scripts/check_no_secrets.py", []),
    ("Master verification", "scripts/verify_dealix_ultimate_os.py", []),
    ("First 100 leads plan", "scripts/build_first_100_leads_plan.py", ["--mode", "demo"]),
    ("Daily operator (demo)", "scripts/dealix_daily_operator.py", ["--mode", "demo"]),
    ("Generate drafts", "scripts/generate_outreach_drafts.py", ["--top", "10", "--language", "both", "--channel", "whatsapp"]),
    ("Generate proposal (demo)", "scripts/generate_proposal.py", ["--account-id", "demo-acc-003", "--offer", "Command Center", "--lang", "both", "--timeline", "21 days"]),
    ("Generate quote", "scripts/generate_quote.py", ["--account-id", "demo-001", "--offer", "Revenue OS", "--setup-price", "18000", "--monthly-price", "5000"]),
    ("Launch brief", "scripts/generate_launch_brief.py", []),
    ("Conversion scorecard", "scripts/generate_conversion_scorecard.py", []),
    ("Proof report (demo)", "scripts/generate_proof_report.py", ["--account-id", "demo-001", "--lang", "both"]),
    ("Monthly review (demo)", "scripts/generate_monthly_client_review.py", ["--account-id", "demo-001", "--lang", "both"]),
    ("Backup business data", "scripts/backup_business_data.py", []),
    ("Check data integrity", "scripts/check_data_integrity.py", []),
    ("Ops health report", "scripts/generate_ops_health_report.py", []),
    ("Founder dashboard data", "scripts/generate_founder_dashboard_data.py", ["--mode", "demo"]),
    ("Production readiness", "scripts/production_readiness_check.py", []),
    ("Pre-push guard", "scripts/pre_push_guard.py", []),
    ("Local smoke test", "scripts/local_smoke_test.py", []),
]


def main() -> int:
    print("Dealix V5 Run All")
    print("=" * 50)
    passed = 0
    for label, rel, extra in STEPS:
        path = REPO_ROOT / rel
        if not path.exists():
            print(f"[{label}]  SKIP (file missing)")
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
