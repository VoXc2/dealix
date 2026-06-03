#!/usr/bin/env python3
"""Verify full autonomous commercial ops stack (governed — no external send)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()

FAILURES: list[str] = []


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL: {msg}")


REQUIRED = [
    "dealix/commercial_ops/full_ops_autopilot.py",
    "dealix/commercial_ops/complete_autonomous_day.py",
    "dealix/commercial_ops/founder_cockpit.py",
    "dealix/commercial_ops/unified_founder_day.py",
    "scripts/run_dealix_complete_autonomous_day.py",
    "scripts/run_full_commercial_ops_autopilot.py",
    "scripts/run_dealix_full_autonomous_ops.py",
    "scripts/founder_one_command.sh",
    "scripts/founder_one_command.ps1",
    "frontend/src/components/gtm/OpsFullAutonomousOpsCard.tsx",
    "frontend/src/components/gtm/OpsFounderCommandCenter.tsx",
    "docs/commercial/FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md",
    ".github/workflows/governed-full-ops-daily.yml",
    ".github/workflows/founder_evening_evidence.yml",
]


def check_files() -> None:
    for rel in REQUIRED:
        if (ROOT / rel).is_file():
            ok(rel)
        else:
            fail(f"missing {rel}")


def check_snapshot() -> None:
    from dealix.commercial_ops.full_ops_autopilot import (
        RESEARCH_ALIGNMENT_AR,
        build_full_autonomous_ops_snapshot,
    )

    if len(RESEARCH_ALIGNMENT_AR.get("external_consensus") or []) < 3:
        fail("research_alignment external_consensus too short")
    else:
        ok("research_alignment consensus")

    snap = build_full_autonomous_ops_snapshot(
        top_n=3,
        include_nested=False,
        include_value_plan=False,
    )
    if snap.get("schema_version") != "1.1":
        fail(f"schema_version={snap.get('schema_version')}")
    else:
        ok("full_autonomous_ops snapshot 1.1")

    ar = snap.get("automation_readiness") or {}
    if ar.get("verdict") not in {"AUTONOMOUS_READY", "NEEDS_FOUNDER", "BLOCKED"}:
        fail(f"automation_readiness verdict={ar.get('verdict')}")
    else:
        ok(f"automation_readiness={ar.get('verdict')}")


def check_cockpit() -> None:
    from dealix.commercial_ops.founder_cockpit import build_founder_cockpit

    cockpit = build_founder_cockpit(top_n=3, strongest_ops_mode="morning")
    if not cockpit.get("cockpit_verdict"):
        fail("cockpit missing verdict")
    else:
        ok(f"cockpit_verdict={cockpit.get('cockpit_verdict')}")
    if not cockpit.get("hitl_spectrum_2026_ar"):
        fail("cockpit missing HITL spectrum")
    else:
        ok("hitl_spectrum_2026")


def check_plan_dry() -> None:
    from dealix.commercial_ops.complete_autonomous_day import build_complete_autonomous_plan

    plan = build_complete_autonomous_plan()
    if not plan.get("phases"):
        fail("complete_autonomous_plan empty phases")
    else:
        ok(f"complete_autonomous_plan phases={len(plan['phases'])}")


def check_api_routes() -> None:
    try:
        from fastapi.testclient import TestClient

        from api.main import app

        client = TestClient(app)
        headers = {"X-Admin-API-Key": "dev"}
        import os

        os.environ["DEALIX_ADMIN_API_KEY"] = "dev"
        os.environ["ADMIN_API_KEYS"] = "dev"

        r = client.get(
            "/api/v1/ops-autopilot/founder/full-autonomous-ops",
            params={"top_n": 3, "include_nested": False, "include_value_plan": False},
            headers=headers,
        )
        if r.status_code == 200 and r.json().get("schema_version"):
            ok("GET founder/full-autonomous-ops")
        else:
            fail(f"full-autonomous-ops status={r.status_code}")

        r2 = client.get(
            "/api/v1/ops-autopilot/founder/complete-autonomous-day",
            headers=headers,
        )
        if r2.status_code == 200 and r2.json().get("phases"):
            ok("GET founder/complete-autonomous-day")
        else:
            fail(f"complete-autonomous-day plan status={r2.status_code}")

        r3 = client.get(
            "/api/v1/ops-autopilot/founder/cockpit",
            params={"top_n": 3, "mode": "morning"},
            headers=headers,
        )
        if r3.status_code == 200 and r3.json().get("cockpit_verdict"):
            ok("GET founder/cockpit")
        else:
            fail(f"cockpit status={r3.status_code}")
    except Exception as exc:
        fail(f"API smoke: {exc}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--skip-api", action="store_true")
    args = p.parse_args()

    print("== verify_full_autonomous_ops_stack ==")
    check_files()
    check_snapshot()
    check_cockpit()
    check_plan_dry()
    if not args.skip_api:
        check_api_routes()

    if FAILURES:
        print("\nDEALIX_FULL_AUTONOMOUS_OPS_STACK=FAIL")
        for f in FAILURES:
            print(f"  - {f}")
        return 1

    print("\nDEALIX_FULL_AUTONOMOUS_OPS_STACK=PASS")
    print("Run: bash scripts/founder_one_command.sh")
    print("Doc: docs/commercial/FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
