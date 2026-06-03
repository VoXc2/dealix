"""Suppression list semantics: add reasons, block sending, no silent bypass."""

import pytest

from core.safety.suppression import SuppressionList
from core.safety.constants import SUPPRESSION_REASONS


def test_suppressed_contact_cannot_send():
    sl = SuppressionList()
    sl.add("ceo@example.sa", "unsubscribe")
    assert sl.is_suppressed("ceo@example.sa") is True
    assert sl.can_send("ceo@example.sa") is False


def test_case_and_space_insensitive():
    sl = SuppressionList()
    sl.add("  CEO@Example.sa ", "bounce")
    assert "ceo@example.sa" in sl


def test_all_reasons_supported():
    sl = SuppressionList()
    for i, reason in enumerate(SUPPRESSION_REASONS):
        sl.add(f"c{i}@example.sa", reason)
    assert len(sl) == len(SUPPRESSION_REASONS)


def test_unknown_reason_rejected():
    sl = SuppressionList()
    with pytest.raises(ValueError):
        sl.add("x@example.sa", "because_i_said_so")


def test_non_suppressed_contact_can_send():
    sl = SuppressionList()
    assert sl.can_send("new@example.sa") is True
