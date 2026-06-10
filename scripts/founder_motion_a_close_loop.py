#!/usr/bin/env python3
"""Wave 0 revenue — Motion A close checklist."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_comprehensive_plan import analyze_phase_0_1_gate  # noqa: E402


def main() -> int:
    gate = analyze_phase_0_1_gate()
    print(f"FOUNDER_MOTION_A_VERDICT={gate.get('verdict')}")
    for b in gate.get("blockers_ar") or []:
        print(f"  blocker: {b}")
    return 0 if gate.get("verdict") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
