#!/usr/bin/env python3
"""Enterprise layer readiness verification runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from auto_client_acquisition.enterprise_layer_validation import (  # noqa: E402
    load_manifest,
    validate_manifest,
)


def _build_payload(report) -> dict:
    return {
        "verdict": report.verdict,
        "total_layers": report.total_layers,
        "ready_layers": report.ready_layers,
        "cross_layer_score": report.cross_layer_score,
        "cross_layer_status": report.cross_layer_status,
        "layers": [
            {
                "id": layer.layer_id,
                "status": layer.status,
                "score": layer.score,
                "owner": layer.owner,
                "missing_docs": list(layer.missing_docs),
                "missing_required_paths": list(layer.missing_required_paths),
                "missing_test_paths": list(layer.missing_test_paths),
            }
            for layer in report.layers
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        default="readiness/layer_validation.yaml",
        help="Path to layer validation YAML manifest",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON output only",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero unless verdict is PASS",
    )
    args = parser.parse_args()

    manifest_path = REPO / args.manifest
    manifest = load_manifest(manifest_path)
    report = validate_manifest(manifest, REPO)
    payload = _build_payload(report)

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"DEALIX_ENTERPRISE_LAYER_VERDICT={report.verdict}")
        print(f"ENTERPRISE_LAYER_TOTAL={report.total_layers}")
        print(f"ENTERPRISE_LAYER_READY={report.ready_layers}")
        print(f"CROSS_LAYER_SCORE={report.cross_layer_score}")
        print(f"CROSS_LAYER_STATUS={report.cross_layer_status}")
        for layer in report.layers:
            key = layer.layer_id.upper()
            print(f"LAYER_{key}_STATUS={layer.status}")
            print(f"LAYER_{key}_SCORE={layer.score}")
        failed_cross = [
            check.check_id for check in report.cross_layer_checks if not check.passed
        ]
        if failed_cross:
            print(f"CROSS_LAYER_BLOCKERS={','.join(failed_cross)}")

    if args.strict:
        return 0 if report.verdict == "PASS" else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
