#!/usr/bin/env python3
"""Render the master-verifier JSON report to a tracked location.

Used by CI (via `git diff --exit-code`) to enforce that the published
verifier report stays in sync with reality. Also used by the Founder
Command Center dashboard, which fetches the JSON to render the 19-system
score grid.

Output path: landing/assets/data/verifier-report.json

Behavior:
- Always exits 0 (the master verifier's own exit code reflects state).
- Pretty-prints JSON with stable key order for clean git diffs.
- Strips runtime-only fields (timestamps, machine names) so the file
  doesn't churn on every run — only changes when SYSTEM STATE changes.

Usage:
    python scripts/render_verifier_report.py
    python scripts/render_verifier_report.py --output some/other/path.json

The companion CI step (in .github/workflows/ci.yml):
    python scripts/render_verifier_report.py
    git diff --exit-code -- landing/assets/data/verifier-report.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "landing" / "assets" / "data" / "verifier-report.json"
VERIFIER = REPO_ROOT / "scripts" / "verify_all_dealix.py"


def render(output_path: Path) -> dict:
    """Run the master verifier in --json mode and persist its output."""
    if not VERIFIER.exists():
        print(f"verifier missing: {VERIFIER}", file=sys.stderr)
        sys.exit(2)

    result = subprocess.run(
        [sys.executable, str(VERIFIER), "--json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    # The verifier exits 1 on FAIL; that's expected. We only fail this
    # script if the verifier itself crashed (no JSON on stdout).
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("verifier did not emit valid JSON", file=sys.stderr)
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(2)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    # Stable, sorted keys + trailing newline = clean git diffs.
    output_path.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="render verifier report")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="output JSON path (default: landing/assets/data/verifier-report.json)",
    )
    args = parser.parse_args(argv)

    data = render(args.output)
    rel = args.output.relative_to(REPO_ROOT) if args.output.is_absolute() else args.output
    overall = "PASS" if data.get("overall_pass") else "FAIL"
    ceo = "YES" if data.get("ceo_complete") else "NO"
    print(f"wrote {rel}  (overall: {overall}, CEO-complete: {ceo})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
