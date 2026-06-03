#!/usr/bin/env python3
"""Verify founder master plan waves 0–3 (repo implementation + founder ops gates)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.wave_master_plan import build_wave_master_plan_snapshot  # noqa: E402


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    blob = build_wave_master_plan_snapshot()
    print(json.dumps(blob, ensure_ascii=False, indent=2))
    print(f"\nWAVE_MASTER_PLAN_VERDICT={blob['overall_verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
