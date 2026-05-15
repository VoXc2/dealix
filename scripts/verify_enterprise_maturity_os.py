#!/usr/bin/env python3
"""Verify Dealix Enterprise Maturity Operating System readiness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from auto_client_acquisition.enterprise_maturity_os import (  # noqa: E402
    CAPABILITY_KEYS,
    domain_coverage_map,
    evaluate_all_domain_filesystem_status,
    evaluate_enterprise_maturity,
)

DEFAULT_MODEL_PATH = REPO / "docs" / "enterprise" / "ENTERPRISE_READINESS_MODEL.yaml"


def _load_capability_scores(path: Path) -> dict[str, float]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    capabilities = payload.get("capabilities") or {}
    scores: dict[str, float] = {}
    for key in CAPABILITY_KEYS:
        if key not in capabilities:
            raise ValueError(f"Missing capability score: {key}")
        scores[key] = float(capabilities[key])
    return scores


def _as_jsonable(statuses: Any, report: Any) -> dict[str, Any]:
    return {
        "overall_score": report.overall_score,
        "transformation_ready": report.transformation_ready,
        "domains": [
            {
                "domain": item.domain,
                "capability_score": item.capability_score,
                "artifact_coverage": item.artifact_coverage,
                "blended_score": item.blended_score,
            }
            for item in report.domain_scores
        ],
        "filesystem": [
            {
                "domain": status.domain,
                "coverage": status.coverage,
                "missing_paths": list(status.missing_paths),
                "missing_system_artifacts": list(status.missing_system_artifacts),
            }
            for status in statuses
        ],
        "platform_path_note": (
            "Canonical /platform/* was mapped to /dealix_platform/* "
            "to avoid stdlib 'platform' module shadowing."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--model",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Path to enterprise readiness YAML model.",
    )
    ap.add_argument("--json", action="store_true", help="Print full JSON output.")
    ap.add_argument(
        "--soft-fail",
        action="store_true",
        help="Always exit 0, even when transformation_ready=false.",
    )
    args = ap.parse_args()

    scores = _load_capability_scores(args.model)
    statuses = evaluate_all_domain_filesystem_status(REPO)
    coverage = domain_coverage_map(statuses)
    report = evaluate_enterprise_maturity(scores, coverage)

    if args.json:
        print(json.dumps(_as_jsonable(statuses, report), ensure_ascii=False, indent=2))
    else:
        print(f"ENTERPRISE_MATURITY_SCORE={report.overall_score}")
        print(f"ENTERPRISE_TRANSFORMATION_READY={'true' if report.transformation_ready else 'false'}")
        for item in report.domain_scores:
            print(
                "DOMAIN_SCORE:"
                f"{item.domain}:capability={item.capability_score}"
                f":artifacts={item.artifact_coverage}"
                f":blended={item.blended_score}"
            )
        for status in statuses:
            if status.missing_paths or status.missing_system_artifacts:
                print(
                    f"DOMAIN_GAPS:{status.domain}:"
                    f"missing_paths={len(status.missing_paths)}:"
                    f"missing_system_artifacts={len(status.missing_system_artifacts)}",
                    file=sys.stderr,
                )

    if args.soft_fail:
        return 0
    return 0 if report.transformation_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
