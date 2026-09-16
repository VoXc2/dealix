"""Shared repository-walk scope for Dealix scanners.

Both security smoke gates (``scripts/security_smoke.py`` and
``scripts/ops/security_smoke_ci.py``) need the same answer to one question:
which files in this tree are Dealix-authored and therefore worth scanning?

They previously each answered it with their own hand-maintained set of
directory names, and both sets carried the same two defects:

  1. Virtualenvs were excluded by name (``.venv``/``venv``), so a venv under
     any other name was walked into and credential-shaped strings inside
     installed third-party packages were reported as leaked secrets.
  2. Nested paths such as ``reports/runtime`` were stored in a set matched
     against single path components, so those exclusions never fired.

The mechanism lives here so it is fixed once. The *policy* — which directory
names a given scanner excludes — stays with each caller, because the two gates
deliberately differ (only the CI gate skips ``.github``; the standalone gate
scans workflow files for hardcoded credentials).
"""

from __future__ import annotations

import os
import subprocess
from collections.abc import Iterable, Iterator
from pathlib import Path

VENDORED_DIR_NAMES = frozenset(
    {
        "__pycache__",
        "dist-packages",
        "site-packages",
    }
)


def is_virtualenv(directory: Path) -> bool:
    """Detect a Python virtualenv by its marker file rather than by name."""
    try:
        return (directory / "pyvenv.cfg").is_file()
    except OSError:
        # PermissionError on root-owned 700 runtime dirs — treat as pruned
        return True


def _matches_path_prefix(rel: str, prefix: str) -> bool:
    """Match one repo-relative path or a descendant, never a sibling prefix."""
    normalized = prefix.rstrip("/")
    return rel == normalized or rel.startswith(f"{normalized}/")


def is_pruned_dir(
    directory: Path,
    rel: str,
    skip_dir_names: Iterable[str],
    skip_path_prefixes: tuple[str, ...] = (),
) -> bool:
    """Return True when ``directory`` must not be descended into."""
    name = directory.name
    if name in VENDORED_DIR_NAMES or name in skip_dir_names:
        return True
    if name.endswith(".egg-info"):
        return True
    if any(_matches_path_prefix(rel, prefix) for prefix in skip_path_prefixes):
        return True
    return is_virtualenv(directory)


def iter_candidate_files(
    root: Path,
    skip_dir_names: Iterable[str],
    skip_path_prefixes: tuple[str, ...] = (),
) -> Iterator[Path]:
    """Yield files under ``root`` while pruning excluded directories."""
    skip_names = frozenset(skip_dir_names)
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        rel_dir = current.relative_to(root).as_posix()
        kept: list[str] = []
        for name in sorted(dirnames):
            child_rel = name if rel_dir == "." else f"{rel_dir}/{name}"
            if not is_pruned_dir(
                current / name,
                child_rel,
                skip_names,
                skip_path_prefixes,
            ):
                kept.append(name)
        dirnames[:] = kept
        for name in sorted(filenames):
            yield current / name

def git_path_state(root: Path, path: Path) -> str:
    """Classify one path without reading its contents.

    Returns ``tracked``, ``ignored_untracked``, ``untracked`` or ``not_git``.
    Security gates can therefore fail on source-control risk without treating a
    deliberately ignored local secret file as if it were committed source.
    """

    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        return "not_git"

    quiet = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL, "check": False}
    try:
        probe = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
            timeout=2,
            **quiet,
        )
        if probe.returncode != 0:
            return "not_git"
        tracked = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", rel],
            timeout=2,
            **quiet,
        )
        if tracked.returncode == 0:
            return "tracked"
        ignored = subprocess.run(
            ["git", "-C", str(root), "check-ignore", "-q", "--", rel],
            timeout=2,
            **quiet,
        )
        return "ignored_untracked" if ignored.returncode == 0 else "untracked"
    except (OSError, subprocess.TimeoutExpired):
        return "not_git"
