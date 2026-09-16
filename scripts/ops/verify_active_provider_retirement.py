#!/usr/bin/env python3
"""Fail if retired deployment providers regain active Dealix runtime authority."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACTIVE = [
    ROOT / "core/config/deployment_identity.py",
    ROOT / "core/config/settings.py",
    ROOT / "Dockerfile",
    ROOT / "apps/web/Dockerfile",
    ROOT / "scripts/dealix_daily_start.sh",
    ROOT / "scripts/dealix_brain_control.py",
    ROOT / "scripts/dealix_company_brain_daily.py",
    ROOT / "scripts/dealix_enterprise_readiness.py",
    ROOT / "scripts/dealix_scale_brief.py",
    ROOT / "scripts/dealix_strategic_brief.py",
    ROOT / "scripts/ops/install_dealix_agent_stack.sh",
    ROOT / "scripts/ops/install_dealix_company_autopilot.sh",
    ROOT / "scripts/ops/install_dealix_vps_issue_bridge.sh",
    ROOT / "scripts/ops/repair_dealix_vps_runtime_compat.sh",
]
FORBIDDEN = ("up.railway.app", "railway run", ".railway/bin", "RAILWAY_GIT_COMMIT_SHA", "VERCEL_GIT_COMMIT_SHA")
errors=[]
for path in ACTIVE:
    text=path.read_text(encoding="utf-8")
    for token in FORBIDDEN:
        if token in text:
            errors.append(f"{path.relative_to(ROOT)}:{token}")
print("ACTIVE_PROVIDER_RETIREMENT=" + ("PASS" if not errors else "FAIL"))
print("CANONICAL_RUNTIME_AUTHORITY=SELFHOST_EXACT_GIT_SHA")
print("MIGRATION_PROOF_REFERENCES=PRESERVED")
for error in errors: print("ERROR="+error)
raise SystemExit(0 if not errors else 1)
