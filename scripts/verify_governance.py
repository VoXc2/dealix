#!/usr/bin/env python3
"""Entry point alias: run governance documentation verification."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "verify_governance_rules.py"


def main() -> int:
    return subprocess.call([sys.executable, str(SCRIPT)], cwd=SCRIPT.parent.parent)  # noqa: S603


if __name__ == "__main__":
    raise SystemExit(main())
