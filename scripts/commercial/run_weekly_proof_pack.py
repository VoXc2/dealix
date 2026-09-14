#!/usr/bin/env python3
"""Compatibility adapter to the canonical Weekly Operating Proof Pack generator."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GENERATOR = ROOT / "scripts" / "generate_weekly_operating_proof_pack.py"


def _default_out(stamp: str) -> Path:
    """Weekly proof output must never dirty the canonical checkout.

    Honor DEALIX_RUNTIME_REPORTS_ROOT (e.g. /opt/dealix/control/reports) so
    scheduled runs write outside the git worktree and cannot poison Source
    Sync. The in-repo fallback stays gitignored (see .gitignore).
    """
    override = os.getenv("DEALIX_RUNTIME_REPORTS_ROOT", "").strip()
    if override:
        return Path(override) / "company_os" / "weekly" / f"OPERATING_PROOF_{stamp}.md"
    return ROOT / "reports" / "company_os" / "weekly" / f"OPERATING_PROOF_{stamp}.md"


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", default="dealix", help="Compatibility only")
    parser.add_argument("--mode", default="draft-only", choices=["draft-only"])
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    if not GENERATOR.is_file():
        print("WEEKLY_PROOF=BLOCKED_CANONICAL_GENERATOR_MISSING")
        return 2
    stamp = datetime.now(UTC).strftime("%Y-%m-%d")
    out = _default_out(stamp)
    command = [sys.executable, str(GENERATOR), "--repo-root", str(ROOT), "--out", str(out)]
    if args.strict:
        command.append("--strict")
    result = subprocess.run(command, cwd=ROOT, check=False)
    print(f"WEEKLY_PROOF_REPORT={_display_path(out)}")
    print("WEEKLY_PROOF=DELEGATED_TO_CANONICAL_OPERATING_PROOF_GENERATOR")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
