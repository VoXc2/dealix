"""Tests for the scale-readiness harness — guards the scale-system map."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_client_acquisition.scale_os import (
    FINAL_SCALE_TEST,
    SCALE_SYSTEMS,
    compute_scale_readiness,
    evaluate_final_scale_test,
    evaluate_scale_system,
)

REPO = Path(__file__).resolve().parents[1]


def test_ten_scale_systems_with_unique_ids() -> None:
    assert len(SCALE_SYSTEMS) == 10
    ids = [s.system_id for s in SCALE_SYSTEMS]
    assert ids == list(range(1, 11))


def test_final_scale_test_has_ten_items() -> None:
    assert len(FINAL_SCALE_TEST) == 10
    assert [c.item_id for c in FINAL_SCALE_TEST] == list(range(1, 11))


@pytest.mark.parametrize("system", SCALE_SYSTEMS, ids=lambda s: s.name)
def test_primary_packages_exist(system) -> None:
    """The scale-system → package map must point at real package directories."""
    for pkg in system.primary_packages:
        path = REPO / pkg
        assert path.is_dir(), f"{system.name}: missing package {pkg}"
        assert any(path.glob("*.py")), f"{system.name}: empty package {pkg}"


@pytest.mark.parametrize("system", SCALE_SYSTEMS, ids=lambda s: s.name)
def test_routers_exist_when_declared(system) -> None:
    if system.router:
        assert (REPO / system.router).is_file(), f"{system.name}: missing {system.router}"


def test_compute_scale_readiness_on_repo() -> None:
    report = compute_scale_readiness(REPO)
    assert report.verdict in {"PASS", "PARTIAL", "BLOCKED"}
    assert len(report.systems) == 10
    assert len(report.final_scale) == 10
    # Every primary package exists, so no system should be a hard failure.
    assert report.systems_failed == 0
    assert 0 <= report.final_scale_score <= 10


def test_empty_repo_is_blocked(tmp_path: Path) -> None:
    report = compute_scale_readiness(tmp_path)
    assert report.verdict == "BLOCKED"
    assert report.systems_failed == 10
    assert report.final_scale_score == 0


def test_system_status_values_are_valid() -> None:
    for system in SCALE_SYSTEMS:
        result = evaluate_scale_system(system, REPO)
        assert result.status in {"pass", "partial", "fail"}


def test_final_scale_probes_resolve_consistently(tmp_path: Path) -> None:
    """An empty repo fails every Final Scale Test item."""
    results = evaluate_final_scale_test(tmp_path)
    assert len(results) == 10
    assert all(not passed for _, passed in results)
