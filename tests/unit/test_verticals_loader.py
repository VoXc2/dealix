"""Unit tests for dealix/verticals/__init__.py."""

from __future__ import annotations

from dealix.verticals import Vertical, by_id, list_all

EXPECTED = {
    "real-estate",
    "hospitality",
    "construction",
    "healthcare",
    "education",
    "food-and-beverage",
    "legal",
    "financial-services",
}


def test_list_all_returns_eight_verticals() -> None:
    verticals = list_all()
    assert len(verticals) == 8
    assert {v.id for v in verticals} == EXPECTED
    assert all(isinstance(v, Vertical) for v in verticals)


def test_list_all_sorted_by_id() -> None:
    verticals = list_all()
    assert [v.id for v in verticals] == sorted(v.id for v in verticals)


def test_every_vertical_has_labels_and_lead_form() -> None:
    for v in list_all():
        assert v.label_ar
        assert v.label_en
        assert v.description_ar
        assert v.description_en
        assert isinstance(v.agents, list)
        assert isinstance(v.workflows, list)
        assert v.pricing_default_plan
        assert isinstance(v.lead_form_fields, list)
        # Every form field must declare an identifier (`id` is the canonical
        # key; `name` is accepted as legacy) and a type.
        for field in v.lead_form_fields:
            assert ("id" in field) or ("name" in field), field
            assert "type" in field, field


def test_by_id_returns_known_vertical() -> None:
    v = by_id("real-estate")
    assert v is not None
    assert v.id == "real-estate"


def test_by_id_returns_none_for_unknown() -> None:
    assert by_id("not-a-real-vertical") is None
