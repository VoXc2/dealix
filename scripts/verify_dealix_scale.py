#!/usr/bin/env python3
"""Dealix Scale Readiness — proves the 10 scale systems + 10-point Final Scale Test.

Filesystem introspection only (no network, no DB). Prints per-system PASS flags,
the Final Scale Test score, and DEALIX_SCALE_VERDICT. Exit code 0 only on PASS.

See docs/scale/SCALE_READINESS.md for the human-readable gap register.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from auto_client_acquisition.scale_os.scale_readiness import (  # noqa: E402
    ScaleReadinessReport,
    compute_scale_readiness,
)


def _report_to_dict(report: ScaleReadinessReport) -> dict:
    return {
        "verdict": report.verdict,
        "systems_passed": report.systems_passed,
        "systems_partial": report.systems_partial,
        "systems_failed": report.systems_failed,
        "final_scale_score": report.final_scale_score,
        "final_scale_total": len(report.final_scale),
        "systems": [
            {
                "id": s.system_id,
                "name": s.name,
                "name_ar": s.name_ar,
                "status": s.status,
                "missing_packages": list(s.missing_packages),
                "missing_probes": list(s.missing_probes),
                "missing_router": s.missing_router,
                "missing_tests": list(s.missing_tests),
            }
            for s in report.systems
        ],
        "final_scale": [
            {
                "id": check.item_id,
                "name": check.name,
                "name_ar": check.name_ar,
                "probe": check.probe,
                "passed": passed,
            }
            for check, passed in report.final_scale
        ],
    }


def _print_human(report: ScaleReadinessReport) -> None:
    for result in report.systems:
        flag = "true" if result.status == "pass" else "false"
        print(f"SCALE_SYSTEM_{result.system_id}_PASS={flag}  # {result.status} — {result.name}")
        for pkg in result.missing_packages:
            print(f"  MISSING_PACKAGE={pkg}")
        if result.missing_router:
            print("  MISSING_ROUTER=true")
        for probe in result.missing_probes:
            print(f"  MISSING_CAPABILITY={probe}")
        for test in result.missing_tests:
            print(f"  MISSING_TEST={test}")

    print("")
    for check, passed in report.final_scale:
        flag = "true" if passed else "false"
        print(f"FINAL_SCALE_{check.item_id}_PASS={flag}  # {check.name}")

    print("")
    print(f"SCALE_SYSTEMS_PASSED={report.systems_passed}/{len(report.systems)}")
    print(f"SCALE_SYSTEMS_PARTIAL={report.systems_partial}/{len(report.systems)}")
    print(f"SCALE_SYSTEMS_FAILED={report.systems_failed}/{len(report.systems)}")
    print(f"FINAL_SCALE_TEST={report.final_scale_score}/{len(report.final_scale)}")
    print(f"DEALIX_SCALE_VERDICT={report.verdict}")
    if report.verdict != "PASS":
        print(
            "See docs/scale/SCALE_READINESS.md for the gap register.",
            file=sys.stderr,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix scale readiness harness")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of flags")
    args = parser.parse_args()

    report = compute_scale_readiness(REPO)

    if args.json:
        print(json.dumps(_report_to_dict(report), ensure_ascii=False, indent=2))
    else:
        _print_human(report)

    return 0 if report.verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
