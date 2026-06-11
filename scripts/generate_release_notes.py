"""Generate release notes from CHANGELOG.md.

Usage:
    python3 scripts/generate_release_notes.py
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CHANGELOG = REPO_ROOT / "CHANGELOG.md"
OUT_DIR = REPO_ROOT / "reports" / "releases"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    today = dt.date.today().isoformat()
    if not CHANGELOG.exists():
        print(f"missing: {CHANGELOG}")
        return 1
    body = CHANGELOG.read_text(encoding="utf-8")
    out = OUT_DIR / f"release-notes-{today}.md"
    header = f"# Release Notes — {today}\n\n"
    out.write_text(header + body, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
