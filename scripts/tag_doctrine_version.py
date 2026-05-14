#!/usr/bin/env python3
"""Tag a new doctrine version.

Appends an entry to:
  - open-doctrine/VERSIONS.md
  - open-doctrine/doctrine_versions.json

And (when --tag-git is set) creates a git tag named `doctrine/v<version>`.

Bumping rules — printed as a reminder:
  patch (vX.Y.Z+1): wording fixes that don't change a commitment
  minor (vX.Y+1.0): added clarifying commitment or new control
  major (vX+1.0.0): removed or modified an existing commitment

Usage:
    python scripts/tag_doctrine_version.py \\
        --version v1.0.1 \\
        --summary "Clarify Source Passport language."
    python scripts/tag_doctrine_version.py --version v2.0.0 --summary "..." --tag-git
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date as _date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MD_PATH = REPO_ROOT / "open-doctrine" / "VERSIONS.md"
JSON_PATH = REPO_ROOT / "open-doctrine" / "doctrine_versions.json"

VERSION_RX = re.compile(r"^v\d+\.\d+\.\d+$")


def _current_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=False, timeout=2,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        pass
    return "unknown"


def _load_json() -> dict:
    if not JSON_PATH.exists():
        return {"doctrine_id": "GOVERNED-AI-OPERATIONS-DOCTRINE", "owner": "Dealix", "versions": []}
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def _write_json(data: dict) -> None:
    JSON_PATH.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _append_md_row(version: str, sha: str, date_iso: str, summary: str, signed_by: str) -> None:
    # Append a row to the existing markdown table.
    new_row = f"| `{version}` | `{sha[:10]}` | {date_iso} | {summary} | {signed_by} |\n"
    text = MD_PATH.read_text(encoding="utf-8") if MD_PATH.exists() else ""
    # Place above the "Bumping rules" line if present, else just append.
    marker = "\nBumping rules:"
    if marker in text:
        prefix, suffix = text.split(marker, 1)
        # Make sure prefix ends with a single newline before the row.
        if not prefix.endswith("\n"):
            prefix += "\n"
        text = prefix + new_row + marker + suffix
    else:
        text = text.rstrip() + "\n" + new_row
    MD_PATH.write_text(text, encoding="utf-8")


def add_version(version: str, summary: str, signed_by: str) -> dict:
    if not VERSION_RX.match(version):
        raise SystemExit(f"version must match vX.Y.Z; got {version!r}")
    data = _load_json()
    used = {v["version"] for v in data["versions"]}
    if version in used:
        raise SystemExit(f"version {version} already exists (monotonicity rule)")
    today = _date.today().isoformat()
    entry = {
        "version": version,
        "commit_sha": _current_sha(),
        "date": today,
        "summary": summary.strip(),
        "signed_by": signed_by.strip() or "Founder",
    }
    data["versions"].append(entry)
    # Sort by version on disk for deterministic diffs.
    def _key(v):
        return tuple(int(x) for x in v["version"].lstrip("v").split("."))
    data["versions"].sort(key=_key)
    _write_json(data)
    _append_md_row(version, entry["commit_sha"], today, entry["summary"], entry["signed_by"])
    return entry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="tag a new doctrine version")
    parser.add_argument("--version", required=True, help="vX.Y.Z")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--signed-by", default="Founder")
    parser.add_argument("--tag-git", action="store_true", help="also create git tag doctrine/vX.Y.Z")
    args = parser.parse_args(argv)

    entry = add_version(args.version, args.summary, args.signed_by)
    print(f"appended version {entry['version']} (sha={entry['commit_sha'][:10]}, date={entry['date']})")

    if args.tag_git:
        tag = f"doctrine/{args.version}"
        out = subprocess.run(
            ["git", "tag", "-a", tag, "-m", f"doctrine {args.version} — {entry['summary']}"],
            cwd=REPO_ROOT, check=False,
        )
        if out.returncode == 0:
            print(f"created git tag {tag}")
        else:
            print(f"git tag failed (already exists?); skip", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
