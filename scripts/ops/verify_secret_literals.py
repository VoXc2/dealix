#!/usr/bin/env python3
"""Scan tracked text files for credential-shaped literals without printing values.

This verifier is intentionally conservative and non-disclosing:
- only Git-tracked files are scanned;
- secret values are never emitted;
- findings report path + line + detector only;
- detector source code such as ``sk-proj-[A-Za-z...]`` does not match because
  it is not a credential-shaped literal.

Exit codes:
  0 = no credential-shaped literals found
  1 = one or more possible credential-shaped literals found
  2 = scanner/runtime error
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

DETECTORS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_project_key", re.compile(r"sk-proj-[A-Za-z0-9_-]{20,}")),
    ("openai_legacy_key", re.compile(r"sk-[A-Za-z0-9]{40,}")),
    ("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{40,}")),
    ("github_token", re.compile(r"gh[opusr]_[A-Za-z0-9]{30,}")),
    ("slack_token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}")),
    ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
)

SKIP_SUFFIXES = {
    ".7z", ".avi", ".bin", ".bmp", ".class", ".db", ".dll", ".docx",
    ".dylib", ".gif", ".gz", ".ico", ".jar", ".jpeg", ".jpg", ".lock",
    ".mov", ".mp3", ".mp4", ".pdf", ".png", ".pptx", ".pyc", ".so",
    ".sqlite", ".sqlite3", ".tar", ".tgz", ".webp", ".woff", ".woff2",
    ".xlsx", ".zip",
}


def tracked_files(repo: Path) -> list[Path]:
    proc = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [repo / item.decode("utf-8") for item in proc.stdout.split(b"\0") if item]


def scan_file(path: Path) -> list[tuple[int, str]]:
    if path.suffix.lower() in SKIP_SUFFIXES or not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    findings: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for detector, pattern in DETECTORS:
            if pattern.search(line):
                findings.append((lineno, detector))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[2]))
    args = parser.parse_args()
    repo = Path(args.repo).resolve()

    try:
        findings: list[tuple[str, int, str]] = []
        for path in tracked_files(repo):
            for lineno, detector in scan_file(path):
                findings.append((path.relative_to(repo).as_posix(), lineno, detector))
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"SECRET_LITERAL_SCAN=ERROR error_type={type(exc).__name__}")
        print("SECRET_VALUES_PRINTED=false")
        return 2

    print(f"SECRET_LITERAL_FILES={len({item[0] for item in findings})}")
    print(f"SECRET_LITERAL_FINDINGS={len(findings)}")
    print("SECRET_VALUES_PRINTED=false")
    for path, lineno, detector in findings:
        print(f"SECRET_LITERAL_FILE={path} line={lineno} detector={detector}")

    if findings:
        print("SECRET_LITERAL_SCAN=HOLD")
        return 1
    print("SECRET_LITERAL_SCAN=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
