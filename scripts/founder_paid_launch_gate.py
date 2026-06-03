#!/usr/bin/env python3
"""Paid launch gate after soft PASS — integrations checklist (FOUNDER_ACTION)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

PAID_DOC = ROOT / "docs/commercial/PAID_LAUNCH_AFTER_SOFT_PASS_AR.md"


def main() -> int:
    ensure_stdout_utf8()
    print("== founder_paid_launch_gate ==")
    print("\n== Prerequisite: soft launch PASS ==")
    print("  py -3 scripts/verify_commercial_launch_ready.py")
    print(f"  doc: {PAID_DOC.relative_to(ROOT)}")

    paid = analyze_first_paid_diagnostic()
    print("\n== First paid Diagnostic (evidence truth) ==")
    print(f"  verdict: {paid['verdict']}")
    print(f"  payment_received (real): {paid['payment_received_real']}")
    print(f"  proof_pack_delivered (real): {paid['proof_pack_delivered_real']}")
    if not paid["first_close_ready"]:
        print(
            "  FOUNDER_ACTION: أغلق Diagnostic واحد (payment + proof + CRM KPI) قبل Paid Launch الكامل"
        )

    print("\n== Integration readiness ==")
    script = ROOT / "scripts/verify_paid_launch_readiness.py"
    r = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    print(f"\nPAID_LAUNCH_GATE_EXIT={r.returncode}")
    print("See docs/LAUNCH_GATES.md · docs/commercial/PAID_LAUNCH_TRACKER_AR.md")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
