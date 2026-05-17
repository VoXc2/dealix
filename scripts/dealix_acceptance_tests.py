#!/usr/bin/env python3
"""Dealix Red-Team Acceptance Suite — weekly cron guardrail check.

Runs the Revenue Assurance acceptance suite (test the system against
failure, not success). Exits non-zero if any guardrail has regressed —
suitable as a cron alarm.

Usage:
  python3 scripts/dealix_acceptance_tests.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    from auto_client_acquisition.revenue_assurance_os.acceptance_tests import (
        run_acceptance_suite,
    )

    results = run_acceptance_suite()
    passed = sum(1 for r in results if r.passed)
    print("=== Dealix Red-Team Acceptance Suite ===")
    for r in results:
        mark = "PASS" if r.passed else "FAIL"
        print(f"  [{mark}] {r.case_id}: {r.description}")
        if not r.passed:
            print(f"         expected={r.expected!r} actual={r.actual!r}")
    print(f"\n{passed}/{len(results)} cases passed.")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
