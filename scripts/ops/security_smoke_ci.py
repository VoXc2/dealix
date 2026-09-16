#!/usr/bin/env python3
"""CI-safe security smoke gate for Dealix.

This check keeps hard failures for risky committed runtime files while avoiding
false positives from documented/test-only synthetic credentials.
"""

from __future__ import annotations

import re
import sys
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.repo_scan import git_path_state, is_pruned_dir
from scripts.lib.repo_scan import iter_candidate_files as _iter_files

SKIP_DIR_NAMES = {
    ".eggs",
    ".git",
    ".github",
    ".mypy_cache",
    ".next",
    ".nox",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "dist-packages",
    "htmlcov",
    "node_modules",
    "site-packages",
    "venv",
}

SKIP_PATH_PREFIXES = ("reports/runtime",)

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

SECRET_PATTERNS = [
    re.compile(r"sk_live_[A-Za-z0-9_\-]{12,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]

SAFE_CONTEXT_PATHS = (
    "docs/",
    "tests/",
)

SAFE_PLACEHOLDER_WORDS = (
    "example",
    "fixture",
    "fake",
    "dummy",
    "placeholder",
    "redacted",
    "replace",
    "change_me",
    "test",
    "synthetic",
    "sample",
    "xxxxx",
    "xxxx",
    "<fill",
    "<replace",
    "<your",
)

SAFE_TEMPLATE_PATHS = {
    "scripts/generate_production_env.sh",
}


def relpath(path: Path, root: Path = ROOT) -> str:
    return path.relative_to(root).as_posix()


def is_skipped_dir(directory: Path, rel: str) -> bool:
    """Return True when a directory must be pruned from this gate's scan."""
    return is_pruned_dir(directory, rel, SKIP_DIR_NAMES, SKIP_PATH_PREFIXES)


def iter_candidate_files(root: Path = ROOT) -> Iterator[Path]:
    """Walk the repo, pruning excluded directories instead of descending them."""
    return _iter_files(root, SKIP_DIR_NAMES, SKIP_PATH_PREFIXES)


def is_text_candidate(path: Path) -> bool:
    name = path.name
    if name.startswith(".env"):
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def is_allowed_env_example(path: Path) -> bool:
    name = path.name
    return name.startswith(".env") and name.endswith((".example", ".template", ".sample"))


def line_is_placeholder(line: str) -> bool:
    lowered = line.lower()
    return any(word in lowered for word in SAFE_PLACEHOLDER_WORDS)


def path_is_safe_context(path: Path, root: Path = ROOT) -> bool:
    rel = relpath(path, root)
    return rel.startswith(SAFE_CONTEXT_PATHS) or rel in SAFE_TEMPLATE_PATHS


def scan(root: Path = ROOT) -> tuple[list[str], list[str]]:
    """Scan ``root`` and return ``(failures, warnings)``."""
    failures: list[str] = []
    warnings: list[str] = []

    for path in iter_candidate_files(root):
        if not path.is_file():
            continue

        rel = relpath(path, root)

        if path.name.startswith(".env") and not is_allowed_env_example(path):
            state = git_path_state(root, path)
            if state == "ignored_untracked":
                warnings.append(f"Ignored local env residue excluded from source scan: {rel}")
            else:
                failures.append(f"Do not commit local env file: {rel}")
            # Do not read local runtime env contents; this gate validates repository source.
            continue

        if not is_text_candidate(path):
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for idx, line in enumerate(text.splitlines(), start=1):
            for pattern in SECRET_PATTERNS:
                if not pattern.search(line):
                    continue
                if path_is_safe_context(path, root) or line_is_placeholder(line):
                    warnings.append(f"Synthetic credential example ignored: {rel}:{idx}")
                    continue
                failures.append(f"Potential live secret in {rel}:{idx}: matches {pattern.pattern}")

    return failures, warnings


def main() -> int:
    failures, warnings = scan(ROOT)

    if failures:
        print("CI_SECURITY_SMOKE=FAIL")
        for item in failures:
            print(f"FAIL: {item}")
        for item in warnings:
            print(f"WARN: {item}")
        return 1

    print("CI_SECURITY_SMOKE=PASS")
    if warnings:
        print(f"Ignored synthetic/test examples: {len(warnings)}")
        for item in warnings[:20]:
            print(f"WARN: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
