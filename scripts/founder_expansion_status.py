#!/usr/bin/env python3
"""Print commercial expansion snapshot (targeting, social, ABM)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.expansion_status import build_expansion_status  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    p.add_argument("--top-n", type=int, default=10)
    args = p.parse_args()

    blob = build_expansion_status(abm_top_n=max(1, min(args.top_n, 20)))
    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
        return 0

    t = blob.get("targeting") or {}
    s = blob.get("social") or {}
    print("== founder_expansion_status ==")
    print(f"  targeting pool: {t.get('pool_rows', 0)} rows")
    print(f"  wave2 ready (>=150): {t.get('wave2_ready')}")
    print(f"  wave3 prep (>=200): {t.get('wave3_prep_ready')}")
    print(f"  wave4 prep (>=250): {t.get('wave4_prep_ready')}")
    print(f"  queue 28w ready: {s.get('queue_ready_28w')}")
    print(f"  social: {s.get('posts', 0)} posts / {s.get('cycle_weeks', 0)}w")
    print(f"  queue 24w ready: {s.get('queue_ready_24w')}")
    for line in blob.get("next_actions_ar") or []:
        print(f"  -> {line}")
    print("FOUNDER_EXPANSION_STATUS=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
