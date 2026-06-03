#!/usr/bin/env python3
"""Dealix Revenue Factory — command-line entrypoint.

Usage:
    python dealix.py seed
    python dealix.py factory-run --dry-run
    python dealix.py account-packs --limit 400 --dry-run
    python dealix.py quality-check
    python dealix.py security-check
    python dealix.py delivery-status
    python dealix.py founder-command --dry-run
    python dealix.py launch-score

The real logic lives in the `dealix` package under scripts/. We put scripts/
on sys.path so `import dealix.<module>` resolves to scripts/dealix/.
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

from dealix.cli import main  # noqa: E402  (path set above)

if __name__ == "__main__":
    sys.exit(main())
