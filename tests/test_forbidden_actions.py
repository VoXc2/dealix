"""Forbidden-actions policy file must stay explicit (audit + training)."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FORBIDDEN = REPO / "docs" / "governance" / "FORBIDDEN_ACTIONS.md"


def test_forbidden_actions_doc_covers_core_channels() -> None:
    text = FORBIDDEN.read_text(encoding="utf-8").lower()
    assert "whatsapp" in text
    assert "linkedin" in text or "linked" in text
    assert "scrap" in text
    assert "guarantee" in text or "guaranteed" in text
