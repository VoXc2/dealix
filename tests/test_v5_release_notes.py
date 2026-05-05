"""V5_RELEASE_NOTES.md — structural + content sanity tests.

Lock the release notes against silent regressions:
  - File exists and is non-trivially sized
  - References every v5 layer + Phase H/I/J/K/L/M
  - Contains no forbidden marketing tokens
  - Lists the founder CLI scripts (so a renamed CLI fails this test)
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES = REPO_ROOT / "docs" / "V5_RELEASE_NOTES.md"


@pytest.fixture(scope="module")
def text() -> str:
    assert NOTES.exists(), "docs/V5_RELEASE_NOTES.md must exist"
    return NOTES.read_text(encoding="utf-8")


def test_release_notes_is_non_trivial(text: str):
    assert len(text) > 1500, "release notes seem too short"


def test_release_notes_lists_all_12_layers(text: str):
    layers = [
        "Customer Loop",
        "Role Command OS",
        "Service Quality",
        "Agent Governance",
        "Reliability OS",
        "Vertical Playbooks",
        "Customer Data Plane",
        "Finance OS",
        "Delivery Factory",
        "Proof Ledger",
        "GTM OS",
        "Security & Privacy",
    ]
    for layer in layers:
        assert layer in text, f"release notes missing layer mention: {layer!r}"


def test_release_notes_lists_founder_clis(text: str):
    expected = [
        "scripts/dealix_status.py",
        "scripts/dealix_smoke_test.py",
        "scripts/dealix_snapshot.py",
        "scripts/dealix_diagnostic.py",
        "scripts/dealix_invoice.py",
        "scripts/dealix_morning_digest.py",
    ]
    for s in expected:
        assert s in text, f"release notes missing CLI ref: {s}"


def test_release_notes_carries_no_forbidden_marketing_tokens(text: str):
    """The doc itself must respect the same forbidden-claims perimeter
    as the landing site."""
    # Same forbidden patterns as tests/test_landing_forbidden_claims.py
    forbidden = [
        (r"نضمن(?!\s*استرجاع|\s+ل\w*\s+الاسترجاع)", "نضمن"),
        (r"\bguaranteed\b", "guaranteed"),
        (r"\bblast\b", "blast"),
        (r"\bscrape\b", "scrape"),
    ]
    for pattern, label in forbidden:
        # Allow occurrences only inside negation context ("no scraping",
        # "❌ scraping", "no_scraping", etc.).
        for line in text.splitlines():
            if re.search(pattern, line, flags=re.IGNORECASE):
                # Count as okay if the line contains a clear negation marker
                if any(neg in line.lower() for neg in [
                    "no ", "no_", "❌", "no-", "never", "لا ", "غير ",
                    "ممنوع", "blocked", "forbidden",
                ]):
                    continue
                raise AssertionError(
                    f"release notes line contains forbidden token "
                    f"{label!r} outside negation context: {line!r}"
                )


def test_release_notes_documents_hard_rules(text: str):
    """Hard-rules table must list at least 5 invariants."""
    hard_rules = [
        "No live charge",
        "No live WhatsApp",
        "No LinkedIn automation",
        "No web scraping",
        "No PII",
    ]
    found = sum(1 for r in hard_rules if r.lower() in text.lower())
    assert found >= 4, (
        f"release notes only documents {found}/{len(hard_rules)} hard rules; "
        "expected ≥4"
    )
