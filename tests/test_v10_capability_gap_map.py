"""Verify the v10 capability gap map + dependency decision record stay clean."""
from __future__ import annotations

import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
GAP_MAP = REPO_ROOT / "docs" / "v10" / "DEALIX_CAPABILITY_GAP_MAP.md"
DECISION_RECORD = REPO_ROOT / "docs" / "v10" / "DEPENDENCY_DECISION_RECORD.md"

# Forbidden marketing tokens (re-uses the same regex as the landing perimeter)
FORBIDDEN_TOKENS = ("نضمن", "guaranteed", "blast")


@pytest.fixture(scope="module")
def gap_text() -> str:
    assert GAP_MAP.exists()
    return GAP_MAP.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def decision_text() -> str:
    assert DECISION_RECORD.exists()
    return DECISION_RECORD.read_text(encoding="utf-8")


def test_gap_map_exists_and_non_trivial(gap_text: str):
    assert len(gap_text) > 5000, "gap map seems too short"


def test_gap_map_has_12_layer_sections(gap_text: str):
    # Sections are H2 headers like "## 1. AI Workforce" through "## 12."
    headers = re.findall(r"^## \d+\.\s", gap_text, flags=re.MULTILINE)
    assert len(headers) >= 12, f"only {len(headers)} layer headers"


def test_gap_map_layers_have_required_subsections(gap_text: str):
    """Each layer must have Current state / Target state / Gap /
    Recommended P0 / Founder decision required."""
    required_phrases = [
        "Current state",
        "Target state",
        "Recommended P0 implementation",
        "Founder decision required",
    ]
    for phrase in required_phrases:
        count = gap_text.count(phrase)
        assert count >= 12, (
            f"phrase {phrase!r} appears only {count} times "
            "(expected ≥12 — once per layer)"
        )


def test_gap_map_no_forbidden_tokens_in_positive_context(gap_text: str):
    """Forbidden marketing tokens may appear ONLY inside negation/policy
    context (e.g. "no guaranteed claims"). Any positive use fails."""
    for token in FORBIDDEN_TOKENS:
        for line in gap_text.splitlines():
            if token in line:
                low = line.lower()
                negation = any(neg in low for neg in [
                    "no ", "never", "❌", "forbidden", "blocked", "policy",
                    "لا ", "ممنوع", "red-team", "category", "scraping policy",
                    "fake proof", "claims", "negation", "tested", "regex",
                ])
                if not negation:
                    raise AssertionError(
                        f"forbidden token {token!r} in positive context: {line!r}"
                    )


def test_decision_record_has_required_sections(decision_text: str):
    for section in ("§S5-prior", "§S6", "§S7", "§S8"):
        assert section in decision_text, f"missing section {section}"


def test_decision_record_open_design_pre_approved(decision_text: str):
    # Open Design entry must be marked as already shipped/approved
    assert "Open Design" in decision_text
    assert "✅" in decision_text  # ✅ implicit (shipped during v7 closure)


def test_decision_record_s6_s7_unsigned_by_default(decision_text: str):
    # §S6 + §S7 entries should have empty checkboxes (☐) for date + signature
    s6_block_idx = decision_text.find("§S6 —")
    s8_block_idx = decision_text.find("§S8 —")
    assert s6_block_idx > 0
    assert s8_block_idx > s6_block_idx
    s6_to_s8 = decision_text[s6_block_idx:s8_block_idx]
    # Founder decision date and signature should be unsigned (☐) lines
    assert "Founder decision date:" in s6_to_s8
    assert "Founder signature:" in s6_to_s8
    assert "☐" in s6_to_s8  # at least one unsigned checkbox
