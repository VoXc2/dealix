"""v7 Phase 8 hardening — LinkedIn automation must remain platform-blocked.

Three perimeter assertions:

  1. ``agent_governance.FORBIDDEN_TOOLS`` contains ``LINKEDIN_AUTOMATION``.
  2. ``evaluate_action`` returns ``permitted=False`` for
     ``LINKEDIN_AUTOMATION`` at every defined autonomy level.
  3. Repo-wide check: no module imports ``linkedin_api`` or
     ``unipile``-style automation libraries.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from auto_client_acquisition.agent_governance import (
    AutonomyLevel,
    FORBIDDEN_TOOLS,
    ToolCategory,
    evaluate_action,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_linkedin_automation_in_forbidden_tools_set():
    """The platform-level FORBIDDEN_TOOLS frozenset must include
    LINKEDIN_AUTOMATION. No autonomy level may override it."""
    assert ToolCategory.LINKEDIN_AUTOMATION in FORBIDDEN_TOOLS


@pytest.mark.parametrize("level", list(AutonomyLevel))
def test_evaluate_action_blocks_linkedin_at_every_level(level: AutonomyLevel):
    """Even L4 internal automation cannot run linkedin_automation."""
    result = evaluate_action(
        agent_id="prospecting",
        tool=ToolCategory.LINKEDIN_AUTOMATION,
        autonomy_level=level,
        # Even if explicitly allow-listed, the FORBIDDEN_TOOLS check wins.
        allowed_tools=[ToolCategory.LINKEDIN_AUTOMATION],
    )
    assert result.permitted is False, (
        f"LINKEDIN_AUTOMATION must be blocked at autonomy {level.value}; "
        f"got permitted=True (reason={result.reason!r})"
    )


def test_no_linkedin_or_unipile_imports_in_repo():
    """Search every Python source file for forbidden automation imports.

    Patterns we ban:
      - ``from linkedin_api import …``
      - ``import linkedin_api``
      - ``from unipile``
      - ``import unipile``
    """
    forbidden = [
        re.compile(r"^\s*from\s+linkedin_api(\.|\s)", re.MULTILINE),
        re.compile(r"^\s*import\s+linkedin_api\b", re.MULTILINE),
        re.compile(r"^\s*from\s+unipile(\.|\s)", re.MULTILINE),
        re.compile(r"^\s*import\s+unipile\b", re.MULTILINE),
    ]
    skip_dirs = {".git", ".claude", "node_modules", "__pycache__", ".pytest_cache", ".venv", "venv"}
    violations: list[str] = []

    # Restrict scan to the obvious source roots.
    scan_roots = [
        REPO_ROOT / "auto_client_acquisition",
        REPO_ROOT / "api",
        REPO_ROOT / "core",
        REPO_ROOT / "scripts",
        REPO_ROOT / "integrations",
    ]
    for root in scan_roots:
        if not root.exists():
            continue
        for py_file in root.rglob("*.py"):
            if any(part in skip_dirs for part in py_file.parts):
                continue
            # Don't flag this very test file as a hit if it ever got
            # bundled into the same scan tree.
            if py_file.name == "test_v7_no_linkedin_automation.py":
                continue
            try:
                text = py_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for pat in forbidden:
                if pat.search(text):
                    violations.append(
                        f"{py_file.relative_to(REPO_ROOT)} matches {pat.pattern!r}"
                    )
    assert not violations, (
        "Forbidden LinkedIn-automation imports detected:\n"
        + "\n".join(sorted(violations))
    )
