"""Tests for delivery change-request classifier and backlog."""

from __future__ import annotations

import pytest

from auto_client_acquisition.delivery_os import (
    ChangeRequestType,
    classify_scope_change,
    clear_retainer_backlog_for_tests,
    enqueue_retainer_backlog_item,
    forbidden_capability_requested,
    list_retainer_backlog,
)


@pytest.fixture(autouse=True)
def _clean_backlog() -> None:
    clear_retainer_backlog_for_tests()
    yield
    clear_retainer_backlog_for_tests()


def test_forbidden_capability_from_text() -> None:
    assert forbidden_capability_requested("نريد cold whatsapp automation")


def test_classify_minor_adjustment() -> None:
    t, _ = classify_scope_change(
        "تعديل صياغة بسيط في المسودة",
        within_contract=True,
        estimated_extra_hours=1.0,
    )
    assert t == ChangeRequestType.MINOR_ADJUSTMENT


def test_classify_retainer_backlog_for_large_effort() -> None:
    t, _ = classify_scope_change(
        "نريد تحسينات شهرية على نفس البيانات",
        within_contract=True,
        estimated_extra_hours=20,
    )
    assert t == ChangeRequestType.RETAINER_BACKLOG


def test_retainer_backlog_enqueue() -> None:
    enqueue_retainer_backlog_item(
        item_id="b1",
        engagement_id="e1",
        title="Extra segmentation",
        notes="After sprint",
    )
    assert len(list_retainer_backlog("e1")) == 1
