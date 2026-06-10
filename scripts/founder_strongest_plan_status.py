#!/usr/bin/env python3
"""Print FOUNDER_STRONGEST_PLAN_VERDICT=PASS|FAIL for checklist wiring."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from dealix.commercial_ops.founder_strongest_plan import strongest_plan_status  # noqa: E402


def main() -> int:
    st = strongest_plan_status()
    verdict = "PASS" if st.get("ok") else "FAIL"
    print(f"FOUNDER_STRONGEST_PLAN_VERDICT={verdict}")
    print(f"task_count={st.get('task_count')}")
    print(f"min_task_count={st.get('min_task_count')}")
    print(f"min_task_count={st.get('min_task_count')}")
    if st.get("missing_paths"):
        print("missing_paths=" + ",".join(st["missing_paths"]))
    if "--json" in sys.argv:
        print(json.dumps(st, ensure_ascii=False, indent=2))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
