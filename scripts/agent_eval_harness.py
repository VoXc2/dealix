#!/usr/bin/env python3
"""Run offline agent governance eval harness."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.agent_eval_harness import run_agent_eval_harness  # noqa: E402


def main() -> int:
    blob = run_agent_eval_harness()
    print(f"AGENT_EVAL_VERDICT={blob['verdict']}")
    return 0 if blob["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
