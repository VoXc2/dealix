#!/usr/bin/env python3
"""Scan docs/ top-level directories: markdown counts + README first heading.

Writes committed snapshot JSON for the holding documentation hub.

Run: py -3 scripts/generate_docs_hub_snapshot.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs"
OUT = REPO / "docs" / "strategic" / "_generated" / "docs_top_level_snapshot.json"

# Large binary or generated trees — skip from top-level scan only.
SKIP_NAMES = frozenset({"assets"})


def _readme_title(readme: Path) -> str | None:
    if not readme.is_file():
        return None
    try:
        text = readme.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return re.sub(r"^#+\s*", "", line).strip() or None
    return None


def main() -> int:
    if not DOCS.is_dir():
        print("docs/ not found", file=sys.stderr)
        return 1

    entries: list[dict[str, object]] = []
    for p in sorted(DOCS.iterdir(), key=lambda x: x.name.lower()):
        if not p.is_dir() or p.name.startswith("."):
            continue
        if p.name in SKIP_NAMES:
            continue
        md_files = list(p.rglob("*.md"))
        readme = p / "README.md"
        entries.append(
            {
                "name": p.name,
                "markdown_file_count": len(md_files),
                "readme_path": str(readme.relative_to(REPO)).replace("\\", "/"),
                "readme_title": _readme_title(readme),
            },
        )

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo_root": ".",
        "docs_top_level_dir_count": len(entries),
        "skipped_top_level": sorted(SKIP_NAMES),
        "entries": entries,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(REPO)} ({len(entries)} dirs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
