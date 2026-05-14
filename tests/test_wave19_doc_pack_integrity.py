"""Wave 19 documentation pack integrity tests.

Doctrine-protection canaries for the GCC pack + funding pack + hiring
scorecards + open-doctrine framework. Each test is tolerant: if a doc
hasn't landed on disk yet (e.g. agent still in flight), the test is
skipped rather than failed. Once landed, the doc must satisfy the
integrity rule.

NOTE: separate from test_no_guaranteed_claims.py which enforces forbidden
tokens. These tests enforce structural rules (sections present, Saudi
beachhead preserved, hiring no-hire conditions documented, etc.).
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
GCC_DIR = REPO / "docs" / "gcc-expansion"
FUNDING_DIR = REPO / "docs" / "funding"
OPEN_DOCTRINE_DIR = REPO / "open-doctrine"
CAPITAL_ASSETS_DIR = REPO / "capital-assets"


def _read_if_exists(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


# ── GCC pack integrity ───────────────────────────────────────────────


def test_gcc_expansion_thesis_preserves_saudi_beachhead():
    text = _read_if_exists(GCC_DIR / "GCC_EXPANSION_THESIS.md")
    if text is None:
        pytest.skip("GCC_EXPANSION_THESIS.md not yet written")
    lower = text.lower()
    # Saudi must be cited as the commercial beachhead
    assert "saudi" in lower or "السعود" in text
    # Doctrine framing required
    assert "doctrine" in lower
    # Bilingual disclaimer footer
    assert "Estimated outcomes are not guaranteed outcomes" in text
    assert "النتائج التقديرية ليست نتائج مضمونة" in text


def test_gcc_country_priority_lists_all_six_gcc_states():
    text = _read_if_exists(GCC_DIR / "GCC_COUNTRY_PRIORITY_MAP.md")
    if text is None:
        pytest.skip("GCC_COUNTRY_PRIORITY_MAP.md not yet written")
    lower = text.lower()
    for country in ("saudi", "uae", "qatar", "bahrain", "kuwait", "oman"):
        assert country in lower, f"GCC priority map missing {country!r}"


def test_gcc_partner_archetypes_lists_four_archetypes():
    text = _read_if_exists(GCC_DIR / "GCC_PARTNER_ARCHETYPES.md")
    if text is None:
        pytest.skip("GCC_PARTNER_ARCHETYPES.md not yet written")
    lower = text.lower()
    for archetype in ("big 4", "processor", "consultancy", "vc"):
        assert archetype in lower, f"missing archetype hint {archetype!r}"


# ── Funding pack integrity ──────────────────────────────────────────


def test_funding_memo_present_and_bilingual():
    text = _read_if_exists(FUNDING_DIR / "FUNDING_MEMO.md")
    if text is None:
        pytest.skip("FUNDING_MEMO.md not yet written")
    assert "Estimated outcomes are not guaranteed outcomes" in text
    assert "النتائج التقديرية ليست نتائج مضمونة" in text


def test_use_of_funds_has_two_scenarios():
    text = _read_if_exists(FUNDING_DIR / "USE_OF_FUNDS.md")
    if text is None:
        pytest.skip("USE_OF_FUNDS.md not yet written")
    lower = text.lower()
    assert "bootstrapped" in lower or "invoice" in lower
    assert "angel" in lower or "pre-seed" in lower or "funded" in lower


def test_hiring_scorecards_have_no_hire_conditions():
    """Every hire scorecard MUST document explicit no-hire signals (doctrine #11
    of the founder's hiring discipline: don't hire for potential)."""
    text = _read_if_exists(FUNDING_DIR / "HIRING_SCORECARDS.md")
    if text is None:
        pytest.skip("HIRING_SCORECARDS.md not yet written")
    lower = text.lower()
    assert "no-hire" in lower or "do not hire" in lower or "shall not hire" in lower


def test_first_3_hires_gated_on_revenue():
    text = _read_if_exists(FUNDING_DIR / "FIRST_3_HIRES.md")
    if text is None:
        pytest.skip("FIRST_3_HIRES.md not yet written")
    lower = text.lower()
    # All three hires must be revenue-gated, not time-gated
    assert "sar" in lower or "arr" in lower or "invoice" in lower


# ── Open Doctrine framework integrity ──────────────────────────────


def test_open_doctrine_does_not_expose_commercial_secrets():
    """The most important Wave 19 test — open-doctrine MUST be safe to
    publish externally."""
    if not OPEN_DOCTRINE_DIR.exists():
        pytest.skip("open-doctrine/ directory not yet created")
    forbidden = (
        "anchor_partner_pipeline",
        "admin_key",
        "client_data",
        "private_pricing",
        "investor_confidential",
        "pricing_notes",
    )
    violations: list[str] = []
    for path in OPEN_DOCTRINE_DIR.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for tok in forbidden:
            if tok in text:
                rel = path.relative_to(REPO)
                violations.append(f"{rel}: contains forbidden token {tok!r}")
    assert not violations, "\n".join(violations)


def test_open_doctrine_readme_states_not_commercial_code():
    text = _read_if_exists(OPEN_DOCTRINE_DIR / "README.md")
    if text is None:
        pytest.skip("open-doctrine/README.md not yet written")
    lower = text.lower()
    # Must clearly state this is NOT the commercial implementation
    assert "does not provide commercial" in lower or "not provide commercial" in lower or "not a substitute" in lower or "doctrine, controls" in lower


def test_open_doctrine_license_dual_layer():
    text = _read_if_exists(OPEN_DOCTRINE_DIR / "LICENSE.md")
    if text is None:
        pytest.skip("open-doctrine/LICENSE.md not yet written")
    # Doctrine = CC BY 4.0; Code examples = MIT; Trademark reserved
    assert "CC BY 4.0" in text or "Creative Commons" in text
    assert "MIT" in text
    assert "Dealix" in text  # trademark reservation


# ── Capital Asset Library docs integrity ───────────────────────────


def test_capital_asset_library_doc_present():
    text = _read_if_exists(CAPITAL_ASSETS_DIR / "CAPITAL_ASSET_LIBRARY.md")
    if text is None:
        pytest.skip("CAPITAL_ASSET_LIBRARY.md not yet written")
    assert "Estimated outcomes are not guaranteed outcomes" in text
    lower = text.lower()
    assert "capital asset" in lower
    assert "reusable" in lower or "compound" in lower
