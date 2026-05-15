"""Engine registry — structural integrity of the 12-engine platform."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from dealix.engines import ENGINE_CLASSES, ENGINE_REGISTRY, all_status_reports
from dealix.engines.base import BaseEngine, EngineStatus


def test_registry_has_twelve_engines() -> None:
    assert len(ENGINE_REGISTRY) == 12


def test_engine_ids_are_unique() -> None:
    ids = [s.engine_id for s in ENGINE_REGISTRY.all()]
    assert len(ids) == len(set(ids))


def test_engine_numbers_are_gap_free_one_to_twelve() -> None:
    numbers = sorted(s.number for s in ENGINE_REGISTRY.all())
    assert numbers == list(range(1, 13))


def test_every_engine_declares_governance_hooks() -> None:
    # no_unbounded_agents — every engine must be reachable by governance.
    for spec in ENGINE_REGISTRY.all():
        assert spec.governance_hooks, f"{spec.engine_id} has no governance hooks"


def test_exactly_one_production_engine_is_governance() -> None:
    production = ENGINE_REGISTRY.by_status(EngineStatus.PRODUCTION)
    assert [s.engine_id for s in production] == ["governance"]


def test_engine_classes_cover_every_registered_engine() -> None:
    assert set(ENGINE_CLASSES) == {s.engine_id for s in ENGINE_REGISTRY.all()}


def test_every_engine_class_is_a_base_engine_and_binds_its_spec() -> None:
    for engine_id, cls in ENGINE_CLASSES.items():
        assert issubclass(cls, BaseEngine)
        engine = cls()
        assert engine.spec.engine_id == engine_id


def test_status_report_works_for_every_engine() -> None:
    reports = all_status_reports()
    assert len(reports) == 12
    for report in reports:
        assert "engine" in report
        assert "wraps_available" in report
        assert "domain" in report


def test_unknown_engine_raises() -> None:
    with pytest.raises(KeyError):
        ENGINE_REGISTRY.get("does_not_exist")


def test_registry_status_matches_no_overclaim_register() -> None:
    """Anti-overclaim gate — every engine's registry status matches the register."""
    register_path = (
        Path(__file__).resolve().parents[2]
        / "dealix"
        / "registers"
        / "no_overclaim.yaml"
    )
    claims = yaml.safe_load(register_path.read_text(encoding="utf-8"))["claims"]
    by_id = {c["id"]: c["status"] for c in claims}
    for spec in ENGINE_REGISTRY.all():
        claim_id = f"engine_{spec.engine_id}"
        assert claim_id in by_id, f"{claim_id} missing from no_overclaim.yaml"
        assert by_id[claim_id].lower() == spec.status.value, (
            f"{claim_id}: register says {by_id[claim_id]}, registry says {spec.status.value}"
        )
