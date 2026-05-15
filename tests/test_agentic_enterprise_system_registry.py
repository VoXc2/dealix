"""Tests for Agentic Enterprise Systems 16–25 capability registry."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_client_acquisition.agentic_enterprise_os import (
    SYSTEMS_16_25,
    all_required_paths,
    dominance_coverage_percent,
    missing_capabilities,
    most_critical_gaps,
    readiness_by_system,
    system_completion_ratio,
)


def test_system_ids_cover_16_to_25() -> None:
    ids = [system.system_id for system in SYSTEMS_16_25]
    assert ids == list(range(16, 26))


def test_manifest_matches_python_registry() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = repo_root / "platform" / "system_16_25_registry.json"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    from_json = {
        int(item["system_id"]): tuple(item["required_paths"])
        for item in payload["systems"]
    }
    from_code = {system.system_id: system.required_paths for system in SYSTEMS_16_25}
    assert from_json == from_code


def test_unique_required_paths_count() -> None:
    # 10 systems with one intentional duplicate path (/platform/strategic_reasoning).
    assert len(all_required_paths()) == 43


def test_missing_capabilities_and_coverage() -> None:
    available = {
        "/platform/reality_engine",
        "/platform/operational_health",
        "/platform/org_pressure_detection",
        "/platform/workflow_congestion",
        "/platform/execution_monitoring",
    }
    missing = missing_capabilities(available)
    assert "/platform/revenue_optimization" in missing
    assert dominance_coverage_percent(available) == pytest.approx(11.63, abs=0.01)


def test_system_completion_ratio_and_errors() -> None:
    available = {
        "/platform/org_reasoning",
        "/platform/causal_analysis",
        "/platform/impact_modeling",
    }
    ratio = system_completion_ratio(17, available)
    assert ratio == 0.6
    with pytest.raises(ValueError, match="Unknown system_id"):
        system_completion_ratio(99, available)


def test_readiness_and_critical_gaps() -> None:
    available = {
        "/platform/reality_engine",
        "/platform/operational_health",
        "/platform/org_pressure_detection",
        "/platform/workflow_congestion",
        "/platform/execution_monitoring",
        "/platform/org_reasoning",
        "/platform/causal_analysis",
        "/platform/impact_modeling",
        "/platform/strategic_reasoning",
        "/platform/decision_graph",
    }
    readiness = readiness_by_system(available, threshold=1.0)
    assert readiness[16] is True
    assert readiness[17] is True
    assert readiness[18] is False

    critical = most_critical_gaps(available, top_n=3)
    assert critical
    assert critical[0][1] >= critical[-1][1]
