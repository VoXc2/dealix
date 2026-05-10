"""Wave 10.7 §28.1 Issue A — whole-repo Article 4 lock-down test.

After PR #187 (Wave 10.6) Codex review flagged that the original
`_SCAN_GLOBS` was too narrow (skipped tests/, alembic/, .github/,
autonomous_growth/, root files), this rewrite uses ``git ls-files``
to enumerate every tracked file then filters to a text-content-only
subset.

That guarantees the forbidden token never reappears anywhere in the
codebase — not just in the previously-named directories.

Why ``git ls-files`` rather than recursive glob:
  - Whole-repo coverage by definition (matches what GitHub serves)
  - Honors .gitignore automatically (skips data/ + node_modules/ etc.)
  - No surprise additions when new top-level dirs are added
  - Deterministic + fast

The forbidden string is ``linkedin_scraper`` (case-insensitive,
hyphen or underscore). The fix uses ``linkedin_company_search``
(manual public-data search, founder-approved per call).
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Files allowed to mention the string for documentation purposes only.
# Any new file added here MUST have a code-review reason.
_ALLOWLIST_PATHS = frozenset({
    # The test itself (allowlisted by basename match — see _is_allowlisted)
    "tests/test_no_linkedin_scraper_string_anywhere.py",
    # The Master Matrix audit doc records the historic finding
    "docs/DEALIX_MASTER_EXECUTION_MATRIX.md",
    "docs/DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md",
    # Wave 10.6 + 10.7 sprint reports record the fix and its review
    "docs/WAVE10_6_COHERENCE_SPRINT_REPORT.md",
    "docs/WAVE10_7_PR187_CLEANUP_REPORT.md",
    "docs/FRONTEND_COHERENCE_AUDIT_REPORT.md",
    # Wave 10.8 PR triage doc references the historic finding
    "docs/PR_MERGE_TRIAGE_2026_05_09.md",
    # Wave 11 evidence table — records the lockdown audit row by name
    "docs/WAVE11_FIRST3_PAID_PILOTS_EVIDENCE_TABLE.md",
    # Wave 11 E2E pytest — invokes the lockdown test by file path string
    "tests/test_dealix_master_customer_journey_e2e.py",
    # Wave 11 verifier scripts — they invoke the lockdown test by file path
    "scripts/wave11_hard_gate_audit.sh",
    "scripts/wave11_first3_paid_pilots_verify.sh",
    # Wave 12 master verifier + founder report — invoke the lockdown by name
    "scripts/wave12_saudi_revenue_command_center_verify.sh",
    "docs/WAVE12_SAUDI_REVENUE_COMMAND_CENTER_REPORT.md",
    # Wave 12.7 evidence table — references the test file path
    "docs/WAVE12_EVIDENCE_TABLE.md",
    # The plan file lives outside the repo (in /root/.claude/plans/) so
    # never appears in git ls-files; no allowlist needed.
})

_FORBIDDEN_RE = re.compile(r"linkedin[_\-]scraper", re.IGNORECASE)

# Binary / non-text extensions skipped because the forbidden-token
# regex doesn't apply (and reading them as text wastes time).
_SKIP_EXTENSIONS = frozenset({
    # Images
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp", ".bmp", ".tiff",
    # Fonts
    ".woff", ".woff2", ".ttf", ".otf", ".eot",
    # Archives / compiled
    ".zip", ".tar", ".gz", ".tgz", ".pyc", ".pyo", ".so", ".dylib", ".dll",
    # Docs binaries
    ".pdf", ".docx", ".pptx", ".xlsx",
    # Audio / video
    ".mp3", ".mp4", ".mov", ".wav", ".webm",
    # JSON Schema artefact / lock
    ".lock", ".lockb",
})


def _git_ls_files() -> list[str]:
    """Return every tracked file path relative to the repo root.

    Uses ``git ls-files`` which automatically honors .gitignore and
    is deterministic. Falls back to an empty list if not in a git
    checkout (test then no-ops, since there's nothing to scan).
    """
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def _is_allowlisted(rel_path: str) -> bool:
    """A file is allowlisted only if its full repo-relative path matches."""
    return rel_path in _ALLOWLIST_PATHS


def _should_scan(rel_path: str) -> bool:
    """Skip binaries + obviously-non-text files."""
    suffix = Path(rel_path).suffix.lower()
    return suffix not in _SKIP_EXTENSIONS


def test_no_linkedin_scraper_string_anywhere() -> None:
    """Hard gate: no tracked file outside the audit allowlist may
    contain the string 'linkedin_scraper' (case-insensitive, hyphen
    or underscore).

    Why: NO_LINKEDIN_AUTO + NO_SCRAPING are immutable hard gates.
    Even metadata strings count, because:
      1. Customers reading the registry assume Dealix uses what's listed
      2. SDAIA inquiry / lawyer review relies on accurate disclosure
      3. Drift starts as a label and ends as a feature

    Coverage: this scan uses ``git ls-files`` so it covers EVERY
    tracked file (tests/, alembic/, .github/, autonomous_growth/,
    root-level files, etc.) — not just selected globs.
    """
    files = _git_ls_files()
    # Sanity: in a real repo we should always find files. If the list
    # is empty, the test would silently pass — refuse that.
    assert files, (
        "git ls-files returned 0 files; this test cannot run in a "
        "non-git or empty checkout. Run from a real Dealix git tree."
    )

    hits: list[tuple[str, int, str]] = []
    for rel_path in files:
        if _is_allowlisted(rel_path):
            continue
        if not _should_scan(rel_path):
            continue
        path = REPO_ROOT / rel_path
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if _FORBIDDEN_RE.search(line):
                hits.append((rel_path, line_no, line.strip()))

    assert not hits, (
        "Forbidden string 'linkedin_scraper' found outside the audit allowlist:\n"
        + "\n".join(f"  {p}:{n}: {snippet[:120]}" for p, n, snippet in hits)
        + "\n\nNO_LINKEDIN_AUTO + NO_SCRAPING are immutable hard gates."
        " Use 'linkedin_company_search' (manual, founder-approved per call) instead."
    )


# Allowlist entries that can legitimately not exist YET because they
# are introduced by companion PRs that may land separately:
#   - WAVE10_7 report — created by this PR (Wave 10.7)
#   - DEALIX_MASTER_EXECUTION_{MATRIX,EVIDENCE_TABLE} — created by
#     PR #185 (Master Matrix); may merge before or after this PR
_FORWARD_REFERENCE_PATHS = frozenset({
    "docs/WAVE10_7_PR187_CLEANUP_REPORT.md",
    "docs/DEALIX_MASTER_EXECUTION_MATRIX.md",
    "docs/DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md",
})


def test_allowlist_paths_actually_exist_or_are_forward_references() -> None:
    """Defensive: every path in _ALLOWLIST_PATHS must either exist OR
    be a known forward reference (companion PR pending merge).

    Stops drift where the allowlist accidentally protects a deleted /
    renamed file. A new file with the same intended path would slip
    through silently otherwise.
    """
    missing = [
        p for p in _ALLOWLIST_PATHS
        if p not in _FORWARD_REFERENCE_PATHS
        and not (REPO_ROOT / p).exists()
    ]
    assert not missing, (
        "Allowlisted paths that don't exist + aren't known forward refs:\n"
        + "\n".join(f"  {p}" for p in missing)
        + "\n\nFix: either restore the file, remove the allowlist entry, "
        "or add it to _FORWARD_REFERENCE_PATHS with a comment naming the PR."
    )


def test_scan_actually_covers_tests_directory() -> None:
    """Smoke test: the new whole-repo scan MUST include tests/ files
    (this was the original Codex finding that motivated the rewrite).
    """
    files = _git_ls_files()
    test_files = [f for f in files if f.startswith("tests/")]
    assert len(test_files) > 5, (
        f"Expected git ls-files to surface many tests/ files; got {len(test_files)}. "
        "If this fails, the scan logic regressed and we're back to glob-based partial coverage."
    )
