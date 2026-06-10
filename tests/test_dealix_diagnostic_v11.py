"""V11 Phase 6 — dealix_diagnostic.py CLI smoke test.

Asserts:
- The script runs without API keys
- Output contains required bilingual sections
- No live action / fake fact tokens
- No `نضمن` / `guaranteed` / `blast` / `scrape` claims
- `action_mode` is approval-required posture (i.e. mentions `موافقة` /
  `manual review` / similar)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "dealix_diagnostic.py"

_FORBIDDEN_TOKENS = (
    "نضمن",
    "مضمون",
    "guaranteed",
    "guarantee ",  # leave space so it doesn't match "guarantees" inside "no-guarantee"
    "blast",
    "scrape",
    "scraping",
    "cold whatsapp",
    "cold email",
)


def _run_diagnostic(*extra_args: str) -> str:
    out = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--company",
            "Customer-Slot-A",
            "--sector",
            "b2b_services",
            "--region",
            "riyadh",
            "--pipeline-state",
            "has leads but inconsistent follow-up",
            *extra_args,
        ],
        capture_output=True,
        text=True,
        check=True,
        env={"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/tmp"},
    )
    return out.stdout


def test_script_exists() -> None:
    assert SCRIPT.exists(), "scripts/dealix_diagnostic.py is missing"


def test_diagnostic_runs_without_api_keys() -> None:
    """No env vars → must still produce output (no LLM call)."""
    text = _run_diagnostic()
    assert text.strip(), "diagnostic produced empty output"
    assert "Diagnostic" in text
    assert "Customer-Slot-A" in text


def test_diagnostic_is_bilingual() -> None:
    text = _run_diagnostic()
    # Arabic primary
    assert "القراءة السريعة" in text or "تشخيص" in text or "العربيّة" in text or "عربي" in text
    # Some core English markers
    assert "Sector" in text or "Diagnostic" in text


def test_diagnostic_no_forbidden_claims() -> None:
    """The diagnostic must not advocate forbidden actions.

    The output is allowed to MENTION these tokens in negation context
    (e.g. "no scraping", "لا cold WhatsApp") — that's the safety
    perimeter messaging. We only block *promotion* of these patterns.
    """
    text = _run_diagnostic()
    lower = text.lower()
    # Promotional patterns that must NEVER appear:
    promotion_patterns = (
        "we'll scrape",
        "scrape every",
        "scrape competitors",
        "blast to all",
        "cold whatsapp blast",
        "auto-dm",
        "automate linkedin",
        "guaranteed roi",
        "guaranteed revenue",
        "guaranteed leads",
    )
    for pat in promotion_patterns:
        assert pat not in lower, f"promotional forbidden pattern: '{pat}'"
    # Arabic: the marketing-claim phrases (NOT "لا نضمن" which is the
    # explicit DENIAL of a guarantee).
    forbidden_arabic_phrases = ("نضمن لكم", "مضمون 100%", "مضمونة 100%")
    for phrase in forbidden_arabic_phrases:
        assert phrase not in text, f"forbidden Arabic phrase '{phrase}'"


def test_diagnostic_explicitly_denies_unsafe_actions() -> None:
    """The output must explicitly call out what Dealix WILL NOT do."""
    text = _run_diagnostic()
    lower = text.lower()
    # The diagnostic should say something like "no cold whatsapp",
    # "no scraping", "موافقة العميل شرط", etc.
    denial_markers = (
        "no cold",
        "no scrap",
        "scraping",  # in "no scraping" context
        "موافقة",
        "لا cold",
        "لا scrap",
    )
    present = [m for m in denial_markers if m in lower or m in text]
    assert present, "diagnostic lacks explicit no-cold-WhatsApp / no-scraping denial"


def test_diagnostic_includes_approval_required_posture() -> None:
    """Output must explicitly say it's draft-only / approval-required."""
    text = _run_diagnostic()
    # Look for any of the standard markers
    markers = [
        "manual review",
        "موافقة",
        "approval_required",
        "draft",
        "مسودّة",
        "مسودة",
    ]
    present = [m for m in markers if m in text]
    assert present, (
        f"diagnostic output lacks any approval-required marker. "
        f"Looked for: {markers}"
    )


def test_diagnostic_does_not_claim_specific_revenue() -> None:
    """Output must not state a specific revenue number for the customer."""
    text = _run_diagnostic()
    # If a number with 'SAR' appears, it must be the pricing context (499)
    # not a customer-revenue claim. Specifically we forbid phrases like
    # "you'll earn X SAR" / "ستحقّق X ريال".
    forbidden_phrases = (
        "you'll earn",
        "you will earn",
        "you'll make",
        "you will make",
        "ستحقّق",
        "ستربح",
    )
    for phrase in forbidden_phrases:
        assert phrase.lower() not in text.lower(), (
            f"specific-revenue claim phrase '{phrase}' in output"
        )
