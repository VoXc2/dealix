#!/usr/bin/env python3
"""Lightweight repository security smoke checks.

This is not a replacement for dedicated secret scanners, SAST, or dependency
scanners. It gives CI a fast built-in guard for common repository mistakes:
committed `.env` files, obvious live-token markers, and browser-exposed admin
credential placeholders.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "htmlcov",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
}

TEXT_SUFFIXES = {
    ".env",
    ".example",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

LIVE_TOKEN_PATTERNS = [
    re.compile(r"sk_live_[A-Za-z0-9_\-]{12,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9\-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]

ALLOWED_PLACEHOLDER_MARKERS = (
    "REPLACE",
    "CHANGE_ME",
    "example",
    "test-",
    "placeholder",
)


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.name == ".env.example" or path.suffix in TEXT_SUFFIXES:
            files.append(path)
    return files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def main() -> int:
    errors: list[str] = []

    forbidden_env_files = [
        path
        for path in ROOT.glob(".env*")
        if path.name not in {".env.example"} and path.is_file()
    ]
    for path in forbidden_env_files:
        errors.append(f"Do not commit local env file: {path.relative_to(ROOT)}")

    for path in iter_text_files():
        text = read_text(path)
        if not text:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(marker in line for marker in ALLOWED_PLACEHOLDER_MARKERS):
                continue
            for pattern in LIVE_TOKEN_PATTERNS:
                if pattern.search(line):
                    errors.append(
                        f"Potential live secret in {path.relative_to(ROOT)}:{line_no}: "
                        f"matches {pattern.pattern}"
                    )

    if errors:
        print("Repository security smoke check failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Repository security smoke OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
