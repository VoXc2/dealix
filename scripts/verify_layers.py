#!/usr/bin/env python3
"""Enterprise Layer Validation — validates the 8 layers, dependency-gated.

A layer is READY only when its readiness score qualifies AND every lower
layer is READY (the strict layer-by-layer gate). Exits non-zero on any
regression so CI fails fast.

Usage:
    python scripts/verify_layers.py                # validate all 8 layers
    python scripts/verify_layers.py --layer governance
    python scripts/verify_layers.py --run-tests    # also run mapped pytest
    python scripts/verify_layers.py --json
    python scripts/verify_layers.py --report-only  # never exit non-zero
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from dealix.layer_validation.cross_layer import (  # noqa: E402
    apply_cross_layer_caps,
    cross_layer_passed,
    run_cross_layer_checks,
)
from dealix.layer_validation.loader import load_all  # noqa: E402
from dealix.layer_validation.report import render_json, render_report  # noqa: E402
from dealix.layer_validation.spec import layer_by_id  # noqa: E402
from dealix.layer_validation.validation_engine import (  # noqa: E402
    READY,
    all_ready,
    validate_all_layers,
)


def main() -> int:
    ap = argparse.ArgumentParser(description="Enterprise Layer Validation")
    ap.add_argument("--layer", help="validate a single layer id (gate it alone)")
    ap.add_argument("--run-tests", action="store_true", help="run mapped pytest files")
    ap.add_argument("--json", action="store_true", help="emit JSON report")
    ap.add_argument(
        "--report-only", action="store_true", help="print report, always exit 0"
    )
    args = ap.parse_args()

    if args.layer and layer_by_id(args.layer) is None:
        print(f"unknown_layer:{args.layer}", file=sys.stderr)
        return 2

    results = validate_all_layers(run_tests=args.run_tests)
    manifests = load_all()
    cross_checks = run_cross_layer_checks(manifests)
    apply_cross_layer_caps(results, cross_checks)

    if args.json:
        print(json.dumps(render_json(results, cross_checks), indent=2, ensure_ascii=False))
    else:
        print(render_report(results, cross_checks))

    if args.report_only:
        return 0

    if args.layer:
        return 0 if results[args.layer].status == READY else 1

    ok = all_ready(results) and cross_layer_passed(cross_checks)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
