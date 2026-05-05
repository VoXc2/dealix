"""V11 Phase 10 — truth labels never silently change.

Asserts that ``docs/phase-e/00_GO_NO_GO.md`` contains the canonical
GO/NO-GO labels with their canonical values. If a label flips, this
test forces the change to be intentional + reviewable.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOC = REPO_ROOT / "docs" / "phase-e" / "00_GO_NO_GO.md"


_EXPECTED = {
    "PRODUCTION_READY": "yes",
    "PHASE_E_GO": "yes",
    "FIRST_CUSTOMER_READY": "yes_for_warm_intro_and_diagnostic",
    "PAID_PILOT_READY": "yes_manual_payment_only",
    "PAID_BETA_READY": "no_until_payment_or_written_commitment",
    "REVENUE_LIVE": "no_until_real_money_or_signed_commitment",
    "LIVE_SEND_READY": "no",
    "LIVE_CHARGE_READY": "no",
    "LINKEDIN_AUTOMATION_READY": "no",
    "COLD_WHATSAPP_READY": "never",
}


def _parse_labels(text: str) -> dict[str, str]:
    """Extract LABEL = value pairs from the doc, ignoring whitespace."""
    out: dict[str, str] = {}
    pattern = re.compile(
        r"^([A-Z_]+)\s*=\s*([a-z_]+)\s*$",
        flags=re.MULTILINE,
    )
    for m in pattern.finditer(text):
        out[m.group(1)] = m.group(2)
    return out


def test_doc_exists() -> None:
    assert DOC.exists(), "docs/phase-e/00_GO_NO_GO.md is missing"


def test_every_canonical_label_present() -> None:
    text = DOC.read_text(encoding="utf-8")
    labels = _parse_labels(text)
    missing = set(_EXPECTED) - set(labels)
    assert not missing, f"missing labels in doc: {missing}"


def test_every_label_has_canonical_value() -> None:
    """If you want to flip a label, edit BOTH this test AND the doc in
    the same PR. NEVER flip silently."""
    text = DOC.read_text(encoding="utf-8")
    labels = _parse_labels(text)
    mismatches = []
    for k, v in _EXPECTED.items():
        if labels.get(k) != v:
            mismatches.append(f"{k}: doc={labels.get(k)!r} expected={v!r}")
    assert not mismatches, "label drift:\n" + "\n".join(mismatches)


def test_cold_whatsapp_is_never() -> None:
    """Hard pin — ``COLD_WHATSAPP_READY`` is hard-coded to `never`. This
    test exists to make a casual flip impossible."""
    text = DOC.read_text(encoding="utf-8")
    assert "COLD_WHATSAPP_READY = never" in text


def test_live_charge_and_live_send_are_no() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "LIVE_CHARGE_READY = no" in text
    assert "LIVE_SEND_READY = no" in text


def test_doc_has_bilingual_summary() -> None:
    """Founder-facing doc must be bilingual."""
    text = DOC.read_text(encoding="utf-8")
    assert "Arabic" in text
    assert "English" in text
    # Arabic content present
    assert any(
        ch in text
        for ch in "ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي".split()
    )
