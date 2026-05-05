"""v7 Phase 8 hardening — guaranteed/blast/scrape claims must not leak.

Three perimeter assertions:

  1. Repo-wide scan of ``landing/*.html`` for the four forbidden tokens
     (نضمن / guaranteed / blast / scrape) outside the per-file
     ALLOWLIST returns 0 violations. This re-uses the helper from
     ``tests/test_landing_forbidden_claims.py`` so any broadening of
     that allowlist flows through here too.
  2. Repo-wide scan of ``docs/V*.md`` (the v5/v6/v7 docs) for the same
     four tokens currently turns up many *negation/policy* hits — the
     scan tool does not yet recognize negation context for Markdown.
     Marked ``xfail`` until a doc-scanner with negation awareness ships.
  3. Defensive — assert that no FUTURE test added a ``pytest.skip``
     containing the literal phrase ``"TODO: implement guarantee"``,
     which would silently bypass the guarantee perimeter.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
LANDING = REPO_ROOT / "landing"
DOCS = REPO_ROOT / "docs"
TESTS = REPO_ROOT / "tests"

# Same 4 tokens the landing perimeter test enforces.
_FORBIDDEN = [
    ("نضمن", re.compile(r"نضمن")),
    ("guaranteed", re.compile(r"\bguaranteed\b", re.IGNORECASE)),
    ("blast", re.compile(r"\bblast\b", re.IGNORECASE)),
    ("scrape", re.compile(r"\bscrape\b", re.IGNORECASE)),
]


def _scan(text: str) -> set[str]:
    hits: set[str] = set()
    for token, pat in _FORBIDDEN:
        if pat.search(text):
            hits.add(token)
    return hits


def test_landing_pages_have_no_unallowlisted_forbidden_claims():
    """Re-runs the existing landing-page allowlist sweep with the same
    4-token regex. Any new file with one of these tokens not on the
    allowlist fails this test as a regression signal."""
    # Import the existing helper if available, else inline the same logic.
    try:
        from tests.test_landing_forbidden_claims import (
            ALLOWLIST,
            FORBIDDEN_PATTERNS,
            _scan as helper_scan,
        )
    except ImportError:  # pragma: no cover
        ALLOWLIST = {}
        FORBIDDEN_PATTERNS = _FORBIDDEN
        helper_scan = _scan

    violations: list[str] = []
    for path in sorted(LANDING.glob("*.html")):
        html = path.read_text(encoding="utf-8")
        hits = helper_scan(html)
        if not hits:
            continue
        allowed = set(ALLOWLIST.get(path.name, {}).keys())
        unexpected = hits - allowed
        if unexpected:
            for u in sorted(unexpected):
                violations.append(f"{path.name}: token {u!r} not allowlisted")
    assert not violations, (
        "Forbidden tokens leaked into landing pages outside the allowlist:\n"
        + "\n".join(violations)
    )


@pytest.mark.xfail(
    reason=(
        "TODO: V5/V6/V7 markdown docs reference these tokens in policy/"
        "negation contexts (e.g. 'no guaranteed claims', 'regex bans "
        "blast'). The runtime gap is a context-aware doc scanner that "
        "can distinguish negation/quote from positive claim. Until that "
        "ships, V*.md docs are in a tracked-debt state."
    ),
    strict=False,
)
def test_v_docs_have_no_forbidden_claims():
    """Scan docs/V*.md (v5/v6/v7) for any forbidden token. Expected to
    fail today because policy docs name the forbidden tokens to ban
    them — fixing this means writing a context-aware scanner."""
    violations: list[str] = []
    for path in sorted(DOCS.glob("V*.md")):
        text = path.read_text(encoding="utf-8")
        hits = _scan(text)
        if hits:
            for u in sorted(hits):
                violations.append(f"{path.name}: token {u!r}")
    assert not violations, (
        "Forbidden tokens present in V*.md docs:\n" + "\n".join(violations)
    )


def test_no_test_skips_with_implement_guarantee_todo():
    """Defensive perimeter: if a future test adds a ``pytest.skip("TODO:
    implement guarantee …")``, that test would silently bypass the
    guarantee policy. Fail loud if any such skip exists."""
    forbidden_marker = re.compile(
        r"pytest\.skip\([^\)]*TODO:\s*implement\s+guarantee", re.IGNORECASE
    )
    offenders: list[str] = []
    for py_file in TESTS.rglob("*.py"):
        if py_file.name == "test_v7_no_guaranteed_claims.py":
            # The pattern below appears as the regex literal in this
            # test source; skip self.
            continue
        try:
            text = py_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if forbidden_marker.search(text):
            offenders.append(str(py_file.relative_to(REPO_ROOT)))
    assert not offenders, (
        "Tests must not skip with 'TODO: implement guarantee' — that "
        "silently bypasses the guarantee perimeter:\n"
        + "\n".join(offenders)
    )
