"""
Bilingual operator regression — full Arabic/English/mixed pass set.

These extend the safety battery in `test_operator_saudi_safety.py` with
positive-path classification and language detection regression checks.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.safety import (
    ActionMode,
    Language,
    classify_intent,
)


@pytest.mark.parametrize("text,expected_bundle", [
    ("أبي عملاء أكثر لشركتي", "growth_starter"),
    ("نبي pipeline مرتب", "growth_starter"),
    ("عندي SaaS وأبي pipeline مرتب", "growth_starter"),
    ("عندي شركة تدريب وأبي مواعيد", "growth_starter"),
    ("I need more B2B leads in Saudi", "growth_starter"),
    ("we want to grow our pipeline", "growth_starter"),
])
def test_growth_starter_route_safe(text: str, expected_bundle: str) -> None:
    d = classify_intent(text)
    assert d.action_mode != ActionMode.BLOCKED, f"safe text wrongly blocked: {text!r}"
    assert d.recommended_bundle == expected_bundle


@pytest.mark.parametrize("text", [
    "عندي ملف فيه 200 lead من عملائي السابقين وعندي موافقة",
    "عندي قائمة عملاء سابقين وعندي موافقة أتواصل معهم",
    "We have a consented list of 500 old customers",
    "we have a list of 500 leads from our past customers",
])
def test_data_to_revenue_with_consent_safe(text: str) -> None:
    d = classify_intent(text)
    assert d.action_mode != ActionMode.BLOCKED
    assert d.recommended_bundle == "data_to_revenue"
    assert d.action_mode == ActionMode.APPROVAL_REQUIRED


@pytest.mark.parametrize("text", [
    "أبي شراكات مع وكالات",
    "أبي أسوي شراكات مع وكالات",
    "We want partner channels",
    "build channel partners",
])
def test_partnership_growth_safe(text: str) -> None:
    d = classify_intent(text)
    assert d.action_mode != ActionMode.BLOCKED
    assert d.recommended_bundle == "partnership_growth"


@pytest.mark.parametrize("text", [
    "Need proof report for management",
    "executive report for the board",
    "أبي تقرير تنفيذي",
])
def test_proof_route_safe(text: str) -> None:
    d = classify_intent(text)
    assert d.action_mode != ActionMode.BLOCKED
    assert d.recommended_bundle == "executive_growth_os"


@pytest.mark.parametrize("text,lang", [
    ("أبي عملاء أكثر", Language.AR),
    ("we need leads", Language.EN),
    ("أبي SaaS pipeline", Language.MIXED),
])
def test_language_detection_basic(text: str, lang: Language) -> None:
    d = classify_intent(text)
    assert d.language == lang


def test_classifier_handles_empty_text() -> None:
    d = classify_intent("")
    # An empty string is NOT a cold-WA request — should default safely
    assert d.action_mode != ActionMode.BLOCKED
    assert d.recommended_bundle == "growth_starter"


def test_intake_required_on_recommendation() -> None:
    """Whenever a service is recommended, intake should be required."""
    for txt in ("أبي عملاء أكثر", "I need more leads", "أبي شراكات"):
        d = classify_intent(txt)
        if d.recommended_bundle:
            assert d.requires_intake is True
