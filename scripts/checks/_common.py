#!/usr/bin/env python3
"""
Shared helpers for Dealix scale-readiness check scripts.

Stdlib only. Provides repo-root resolution, JSON loading, file existence
checks, and a small Reporter that prints PASS/WARN/FAIL lines and returns
an overall success boolean (used to drive process exit codes / CI gating).
"""

import json
from pathlib import Path


def repo_root() -> Path:
    """Return the repository root (two levels up from scripts/checks/)."""
    return Path(__file__).resolve().parent.parent.parent


def load_json(rel_path: str):
    """Load a JSON file relative to the repo root. Returns None if missing/invalid."""
    path = repo_root() / rel_path
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def file_exists(rel_path: str) -> bool:
    """True if a path (relative to repo root) exists."""
    return (repo_root() / rel_path).exists()


class Reporter:
    """Collects check outcomes and renders a consistent CLI report."""

    def __init__(self, title: str):
        self.title = title
        self.passes: list[str] = []
        self.warnings: list[str] = []
        self.failures: list[str] = []

    def ok(self, msg: str) -> None:
        self.passes.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    def check(self, condition: bool, ok_msg: str, fail_msg: str,
              warn_only: bool = False) -> bool:
        """Record a PASS if condition is truthy, else FAIL (or WARN)."""
        if condition:
            self.ok(ok_msg)
        elif warn_only:
            self.warn(fail_msg)
        else:
            self.fail(fail_msg)
        return bool(condition)

    def require_files(self, rel_paths: list[str], label: str = "doc") -> None:
        """FAIL for each missing required file."""
        for rel in rel_paths:
            self.check(
                file_exists(rel),
                f"{label} present: {rel}",
                f"{label} MISSING: {rel}",
            )

    def render(self) -> bool:
        """Print the report and return True when there are no failures."""
        bar = "=" * 78
        print(bar)
        print(f"  {self.title}")
        print(bar)
        print()
        for msg in self.passes:
            print(f"  [PASS] {msg}")
        for msg in self.warnings:
            print(f"  [WARN] {msg}")
        for msg in self.failures:
            print(f"  [FAIL] {msg}")
        print()
        print(f"  Summary: {len(self.passes)} passed, "
              f"{len(self.warnings)} warnings, {len(self.failures)} failed")
        if self.failures:
            status = "FAIL"
        elif self.warnings:
            status = "PASS (with warnings)"
        else:
            status = "PASS"
        print(f"  Status: {status}")
        print(bar)
        return len(self.failures) == 0
