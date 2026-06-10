#!/usr/bin/env python3
"""Fail if Alembic reports more than one migration head.

Used in CI to enforce docs/ops/ALEMBIC_MIGRATION_POLICY.md (single head before upgrade head).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    proc = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", "alembic.ini", "heads"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout or "alembic heads failed\n")
        return proc.returncode or 1

    out = (proc.stdout or "").strip()
    if not out:
        sys.stderr.write("alembic heads produced empty stdout\n")
        return 1

    # Typical lines: "009 (head)" or "revid (head) (mergepoint)"
    head_lines = [ln.strip() for ln in out.splitlines() if "(head)" in ln]
    if not head_lines:
        # Fallback: non-empty lines without obvious logging prefix
        head_lines = [ln.strip() for ln in out.splitlines() if ln.strip() and not ln.startswith("INFO")]

    n = len(head_lines)
    if n != 1:
        sys.stderr.write(
            f"Expected exactly 1 Alembic head, found {n}.\n"
            f"Output:\n{out}\n"
            "Create a merge revision or fix down_revision links. See docs/ops/ALEMBIC_MIGRATION_POLICY.md\n"
        )
        return 1

    rev = re.sub(r"\s*\(head\).*$", "", head_lines[0]).strip()
    print(f"OK: single Alembic head ({rev})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
