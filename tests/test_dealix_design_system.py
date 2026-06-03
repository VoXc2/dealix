"""Tests for the Dealix design-system spec and loader.

Phase 1 of DesignOps. These tests guard:

- the existence and structure of `design-systems/dealix/DESIGN.md`
- the canonical status-chip and forbidden-copy lists
- the absence of any forbidden marketing token in a *positive*
  context inside DESIGN.md (it must appear only as a
  literal/quoted forbidden item)
- the parser exposing colors / typography / spacing /
  status_chips / forbidden_copy keys.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from auto_client_acquisition.designops import load_design_system

# Reuse the same regex shape as tests/test_landing_forbidden_claims.py
# so the perimeter stays consistent. We add the v7 forbidden tokens
# the design system explicitly enumerates.
_FORBIDDEN_PATTERNS = [
    ("نضمن", re.compile(r"نضمن")),
    ("guaranteed", re.compile(r"\bguaranteed\b", re.IGNORECASE)),
    ("blast", re.compile(r"\bblast\b", re.IGNORECASE)),
    ("scrape", re.compile(r"\bscrape\b", re.IGNORECASE)),
    (
        "cold WhatsApp",
        re.compile(r"\bcold\s+whatsapp\b", re.IGNORECASE),
    ),
    (
        "revenue guaranteed",
        re.compile(r"\brevenue\s+guaranteed\b", re.IGNORECASE),
    ),
    (
        "ranking guaranteed",
        re.compile(r"\branking\s+guaranteed\b", re.IGNORECASE),
    ),
    (
        "fully automated external send",
        re.compile(
            r"\bfully\s+automated\s+external\s+send\b", re.IGNORECASE
        ),
    ),
]

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DESIGN_MD = _REPO_ROOT / "design-systems" / "dealix" / "DESIGN.md"
_LANGUAGE_MD = _REPO_ROOT / "docs" / "DEALIX_DESIGN_LANGUAGE.md"


def test_design_md_exists():
    assert _DESIGN_MD.is_file(), (
        f"DESIGN.md must live at {_DESIGN_MD}"
    )


def test_design_md_states_arabic_first_rule():
    text = _DESIGN_MD.read_text(encoding="utf-8")
    assert "Arabic-first" in text or "arabic-first" in text.lower()
    # And the literal RTL rule line.
    assert "RTL" in text


def test_design_md_lists_all_eight_status_chip_names():
    text = _DESIGN_MD.read_text(encoding="utf-8")
    expected = [
        "Live",
        "Pilot",
        "Partial",
        "Target",
        "Blocked",
        "Approval Required",
        "Draft Only",
        "Internal Only",
    ]
    for name in expected:
        assert f"`{name}`" in text, (
            f"missing canonical status chip {name!r} in DESIGN.md"
        )


def test_design_md_lists_all_forbidden_copy_items():
    text = _DESIGN_MD.read_text(encoding="utf-8")
    expected = [
        "نضمن",
        "guaranteed",
        "blast",
        "scrape",
        "cold WhatsApp",
        "revenue guaranteed",
        "ranking guaranteed",
        "fully automated external send",
    ]
    for item in expected:
        assert f"`{item}`" in text, (
            f"forbidden copy item {item!r} missing from DESIGN.md "
            "forbidden list"
        )


def test_design_md_states_evidence_first_principle():
    text = _DESIGN_MD.read_text(encoding="utf-8")
    # Either the DESIGN.md or the language doc must spell it out.
    combined = text + "\n" + _LANGUAGE_MD.read_text(encoding="utf-8")
    assert "evidence-first" in combined.lower() or (
        "evidence" in combined.lower()
        and "proof ledger" in combined.lower()
    )


def test_forbidden_marketing_tokens_only_appear_in_negation_or_list_context():
    """Re-uses the regex shape from `test_landing_forbidden_claims.py`.

    The DESIGN.md is allowed to *enumerate* the forbidden list in
    backticked code spans (e.g. ``- `guaranteed` ``). It is *not*
    allowed to use the term in positive prose. We strip backticked
    spans and the §7 forbidden-copy section before scanning the rest
    of the document.
    """
    text = _DESIGN_MD.read_text(encoding="utf-8")
    # Remove all `...` code spans (this strips the literal forbidden
    # enumerations, which are intentional).
    stripped = re.sub(r"`[^`]*`", "", text)
    # Drop §7 (Forbidden Copy List) outright, since its prose is
    # explicitly the negation/enumeration context.
    parts = re.split(r"^## ", stripped, flags=re.MULTILINE)
    kept: list[str] = []
    for part in parts:
        if part.startswith("7. Forbidden Copy List"):
            continue
        kept.append(part)
    scrubbed = "\n## ".join(kept)
    violations: list[str] = []
    for token, pattern in _FORBIDDEN_PATTERNS:
        if pattern.search(scrubbed):
            violations.append(token)
    assert not violations, (
        "Forbidden marketing tokens appear in positive context in "
        f"DESIGN.md outside the §7 enumeration: {violations}"
    )


def test_load_design_system_returns_expected_keys():
    data = load_design_system()
    for key in (
        "colors",
        "typography",
        "spacing",
        "status_chips",
        "forbidden_copy",
    ):
        assert key in data, f"design system loader missing key {key!r}"
    # Sanity on shapes.
    assert isinstance(data["colors"], dict) and data["colors"]
    assert isinstance(data["typography"], dict) and data["typography"]
    assert isinstance(data["spacing"], list) and data["spacing"]
    assert sorted(data["spacing"]) == [4, 8, 12, 16, 24, 32, 48]
    assert isinstance(data["status_chips"], list)
    # All eight canonical chips must round-trip through the loader.
    for chip in (
        "Live",
        "Pilot",
        "Partial",
        "Target",
        "Blocked",
        "Approval Required",
        "Draft Only",
        "Internal Only",
    ):
        assert chip in data["status_chips"], (
            f"status chip {chip!r} not picked up by loader"
        )
    assert isinstance(data["forbidden_copy"], list)
    for item in (
        "نضمن",
        "guaranteed",
        "blast",
        "scrape",
        "cold WhatsApp",
        "revenue guaranteed",
        "ranking guaranteed",
        "fully automated external send",
    ):
        assert item in data["forbidden_copy"], (
            f"forbidden copy item {item!r} not picked up by loader"
        )


def test_load_design_system_is_cached_and_idempotent():
    a = load_design_system()
    b = load_design_system()
    # lru_cache returns the same dict instance.
    assert a is b


@pytest.mark.parametrize(
    "color_token",
    [
        "primary",
        "accent",
        "success",
        "warn",
        "block",
        "surface",
        "surface-alt",
        "text-primary",
        "text-muted",
        "text-inverse",
    ],
)
def test_design_md_lists_named_color_token(color_token: str):
    text = _DESIGN_MD.read_text(encoding="utf-8")
    assert f"`{color_token}`" in text, (
        f"named color token {color_token!r} missing from DESIGN.md"
    )
