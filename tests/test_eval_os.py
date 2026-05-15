"""Eval OS — 4-category taxonomy and YAML pack loader."""

from __future__ import annotations

import pytest

from auto_client_acquisition.eval_os import (
    TAXONOMY_PACKS,
    EvalCategory,
    get_metric,
    list_metrics,
    list_packs,
    load_pack,
    metrics_for_category,
    validate_pack,
    validate_taxonomy_packs,
)


def test_four_categories_exist() -> None:
    assert len(list(EvalCategory)) == 4
    assert {str(c) for c in EvalCategory} == {
        "retrieval_quality",
        "response_quality",
        "workflow_quality",
        "business_quality",
    }


def test_every_category_has_metrics() -> None:
    for category in EvalCategory:
        metrics = metrics_for_category(category)
        assert metrics, f"{category} has no metrics"
        assert all(m.category == category for m in metrics)


def test_list_metrics_non_empty() -> None:
    metrics = list_metrics()
    assert len(metrics) >= 8
    ids = {m.metric_id for m in metrics}
    assert "response_groundedness" in ids
    assert "workflow_task_success" in ids


def test_get_metric_unknown_raises() -> None:
    with pytest.raises(KeyError):
        get_metric("nonexistent_metric")


def test_taxonomy_packs_load_and_validate() -> None:
    results = validate_taxonomy_packs()
    for name in TAXONOMY_PACKS:
        assert results[name] == [], f"{name} has problems: {results[name]}"


def test_load_pack_returns_required_keys() -> None:
    pack = load_pack("retrieval_quality_eval")
    assert pack["eval_id"] == "retrieval_quality"
    assert "checks" in pack
    assert validate_pack(pack) == []


def test_load_pack_missing_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load_pack("does_not_exist_eval")


def test_validate_pack_flags_missing_keys() -> None:
    problems = validate_pack({"eval_id": "x"})
    assert any("version" in p for p in problems)
    assert any("checks" in p for p in problems)


def test_list_packs_includes_new_packs() -> None:
    packs = list_packs()
    for name in TAXONOMY_PACKS:
        assert name in packs
