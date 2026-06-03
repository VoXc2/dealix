#!/usr/bin/env python3
"""
High-signal secret scan (low false-positive).

Fails CI if a committed file looks like a real secret:
  * a committed ``.env`` (not ``.env.example``),
  * a private key block (-----BEGIN ... PRIVATE KEY-----),
  * a `.pem` / `id_rsa` key file.

Example/test tokens (under tests/, data/evals/, docs/, reports/) are NOT real
secrets and are intentionally excluded. GitHub native secret-scanning /
push-protection is the second layer.

Usage:  python3 scripts/scan_secrets.py
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")
# Paths that legitimately contain example tokens / regexes.
EXCLUDE_PREFIXES = ("tests/", "data/evals/", "docs/", "reports/", "core/safety/whatsapp.py",
                    "scripts/scan_secrets.py", ".env.example")


def tracked_files() -> list[str]:
    try:
        out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
        return [l for l in out.splitlines() if l.strip()]
    except Exception:
        return []


def main() -> int:
    problems: list[str] = []
    for rel in tracked_files():
        base = os.path.basename(rel)
        if base == ".env" or rel.endswith(".pem") or base in ("id_rsa", "id_dsa"):
            problems.append(f"committed key/secret file: {rel}")
            continue
        if rel.startswith(EXCLUDE_PREFIXES):
            continue
        path = os.path.join(ROOT, rel)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except (IsADirectoryError, FileNotFoundError):
            continue
        if PRIVATE_KEY.search(content):
            problems.append(f"private key block in: {rel}")

    if problems:
        print("SECRET SCAN VIOLATIONS:")
        for p in problems:
            print("  - " + p)
        return 1
    print("OK: no committed secrets detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
