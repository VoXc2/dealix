"""Wave 10.6 §27.4 — Article 4 lock-down test.

After the PR #185 audit identified `"linkedin_scraper"` as a real
NO_LINKEDIN_AUTO + NO_SCRAPING violation in agent metadata, this test
asserts the string never reappears anywhere in the codebase outside
the test file itself and audit/retrospective documentation.

Why a separate test instead of extending test_landing_forbidden_claims:
The forbidden-tokens test scans `landing/*.html` only. Agent metadata
lives in `auto_client_acquisition/`. We need a dedicated guard for
the agent-registry surface that matches the AI-tool naming convention.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Files/dirs allowed to mention the string for documentation purposes only.
_ALLOWLIST_PATHS = (
    # The test itself
    "tests/test_no_linkedin_scraper_string_anywhere.py",
    # The Master Matrix audit doc records the historic finding
    "docs/DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md",
    "docs/DEALIX_MASTER_EXECUTION_MATRIX.md",
    # Wave 10.6 sprint report records the fix
    "docs/WAVE10_6_COHERENCE_SPRINT_REPORT.md",
    "docs/FRONTEND_COHERENCE_AUDIT_REPORT.md",
)

_FORBIDDEN_RE = re.compile(r"linkedin[_\-]scraper", re.IGNORECASE)

_SCAN_GLOBS = (
    "auto_client_acquisition/**/*.py",
    "api/**/*.py",
    "core/**/*.py",
    "dealix/**/*.py",
    "scripts/**/*.py",
    "scripts/**/*.sh",
    "landing/**/*.html",
    "landing/**/*.js",
    "frontend/**/*.ts",
    "frontend/**/*.tsx",
    "docs/**/*.md",
)


def _is_allowlisted(rel_path: str) -> bool:
    return any(rel_path == allowed or rel_path.endswith(allowed) for allowed in _ALLOWLIST_PATHS)


def test_no_linkedin_scraper_string_anywhere() -> None:
    """Hard gate: no file outside the audit allowlist may contain the
    string 'linkedin_scraper' (case-insensitive, with hyphen or underscore).

    Why: NO_LINKEDIN_AUTO + NO_SCRAPING are immutable hard gates. Even
    metadata strings count, because:
      1. Customers reading the registry assume Dealix uses what's listed
      2. SDAIA inquiry / lawyer review relies on accurate disclosure
      3. Drift starts as a label and ends as a feature
    """
    hits: list[tuple[str, int, str]] = []
    for pattern in _SCAN_GLOBS:
        for path in REPO_ROOT.glob(pattern):
            try:
                rel = str(path.relative_to(REPO_ROOT))
            except ValueError:
                continue
            if _is_allowlisted(rel):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if _FORBIDDEN_RE.search(line):
                    hits.append((rel, line_no, line.strip()))
    assert not hits, (
        "Forbidden string 'linkedin_scraper' found outside the audit allowlist:\n"
        + "\n".join(f"  {p}:{n}: {snippet[:120]}" for p, n, snippet in hits)
        + "\n\nNO_LINKEDIN_AUTO + NO_SCRAPING are immutable hard gates."
        " Use 'linkedin_company_search' (manual, founder-approved per call) instead."
    )
