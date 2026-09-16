#!/usr/bin/env python3
"""Lightweight repository security smoke checks.

This is not a replacement for dedicated secret scanners, SAST, or dependency
scanners. It gives CI a fast built-in guard for common repository mistakes:
committed local `.env` files, obvious live-token markers, and browser-exposed
admin credential placeholders.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.repo_scan import git_path_state, iter_candidate_files

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

IGNORED_PATH_PREFIXES = ("reports/runtime",)

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
    "dummy",
    "fake",
    "synthetic",
    "sample",
    "xxxxx",
    "xxxx",
    "<fill",
    "<replace",
    "<your",
)

SAFE_FIXTURE_PREFIXES = (
    "tests/",
    "docs/",
)

ALLOWED_ENV_EXAMPLE_SUFFIXES = (
    ".example",
    ".sample",
    ".template",
)


def rel(path: Path, root: Path = ROOT) -> str:
    return path.relative_to(root).as_posix()


def iter_text_files(root: Path = ROOT) -> list[Path]:
    files: list[Path] = []
    for path in iter_candidate_files(root, IGNORED_DIRS, IGNORED_PATH_PREFIXES):
        try:
            if not path.is_file():
                continue
        except OSError:
            continue
        if path.name.startswith(".env") or path.suffix in TEXT_SUFFIXES:
            files.append(path)
    return files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError, PermissionError):
        return ""


def is_allowed_env_template(path: Path) -> bool:
    name = path.name
    return name.startswith(".env") and name.endswith(ALLOWED_ENV_EXAMPLE_SUFFIXES)


def is_placeholder_line(line: str) -> bool:
    lowered = line.lower()
    return any(marker.lower() in lowered for marker in ALLOWED_PLACEHOLDER_MARKERS)


def is_safe_fixture_path(path: Path, root: Path = ROOT) -> bool:
    path_rel = rel(path, root)
    return path_rel.startswith(SAFE_FIXTURE_PREFIXES)


def scan(root: Path = ROOT) -> tuple[list[str], list[str]]:
    """Return repository-source failures and non-blocking hygiene warnings."""
    errors: list[str] = []
    warnings: list[str] = []

    for path in iter_text_files(root):
        if path.name.startswith(".env") and not is_allowed_env_template(path):
            state = git_path_state(root, path)
            if state == "ignored_untracked":
                warnings.append(
                    f"Ignored local env residue excluded from source scan: {rel(path, root)}"
                )
            else:
                errors.append(f"Do not commit local env file: {rel(path, root)}")
            # Never inspect local runtime env contents in a repository smoke gate.
            continue

        text = read_text(path)
        if not text:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if is_placeholder_line(line):
                continue
            for pattern in LIVE_TOKEN_PATTERNS:
                if not pattern.search(line):
                    continue
                location = f"{rel(path, root)}:{line_no}"
                if is_safe_fixture_path(path, root):
                    warnings.append(f"Synthetic fixture token ignored in {location}")
                    continue
                errors.append(
                    f"Potential live secret in {location}: matches {pattern.pattern}"
                )

    return errors, warnings


def main() -> int:
    errors, warnings = scan(ROOT)

    if errors:
        print("Repository security smoke check failed:\n", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        if warnings:
            print("\nWarnings:\n", file=sys.stderr)
            for warning in warnings[:50]:
                print(f"- {warning}", file=sys.stderr)
        return 1

    print("Repository security smoke OK")
    if warnings:
        print(f"Ignored synthetic fixture tokens: {len(warnings)}")
        for warning in warnings[:20]:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
