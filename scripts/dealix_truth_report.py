#!/usr/bin/env python3
"""Dealix Truth Report — weekly cron generator.

Writes docs/DEALIX_FULL_OPS_TRUTH_REPORT.md (+ JSON sidecar). Built from
verifiable local facts (git SHA, hard-gate test files, value ledger).
Operator facts (production SHA, verifier status) come from env vars:
  DEALIX_PROD_GIT_SHA, DEALIX_VERIFIER_STATUS, DEALIX_HEALTH_STATUS

NO_LIVE_SEND: never auto-sends; the founder reviews and shares manually.

Usage:
  python3 scripts/dealix_truth_report.py
  python3 scripts/dealix_truth_report.py --counts-json data/funnel.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix weekly Truth Report generator")
    parser.add_argument(
        "--counts-json",
        type=str,
        default="",
        help="Optional JSON file of funnel stage counts (drives next-action).",
    )
    args = parser.parse_args()

    from auto_client_acquisition.revenue_assurance_os.renderers import render_truth_report
    from auto_client_acquisition.revenue_assurance_os.truth_report import build_truth_report

    funnel_counts = None
    if args.counts_json:
        funnel_counts = json.loads(Path(args.counts_json).read_text(encoding="utf-8"))

    report = build_truth_report(funnel_counts=funnel_counts)
    md = render_truth_report(report)

    md_path = _REPO_ROOT / "docs" / "DEALIX_FULL_OPS_TRUTH_REPORT.md"
    md_path.write_text(md, encoding="utf-8")

    json_dir = _REPO_ROOT / "data" / "revenue_assurance" / "truth_report"
    json_dir.mkdir(parents=True, exist_ok=True)
    json_path = json_dir / "latest.json"
    json_path.write_text(
        json.dumps(report.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"=== Dealix Truth Report — {report.generated_at} ===")
    print(f"  local SHA : {report.local_git_sha}")
    print(f"  prod SHA  : {report.prod_git_sha} ({report.git_sha_match})")
    print(f"  paid intent: {report.paid_intent}")
    print(f"  ✓ {md_path.relative_to(_REPO_ROOT)}")
    print(f"  ✓ {json_path.relative_to(_REPO_ROOT)}")
    print("NO_LIVE_SEND: founder reviews and shares manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
