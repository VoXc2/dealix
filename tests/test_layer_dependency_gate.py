"""Tests for the strict layer-by-layer dependency gate and cross-layer caps."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from dealix.layer_validation import validation_engine as ve
from dealix.layer_validation.cross_layer import apply_cross_layer_caps, run_cross_layer_checks
from dealix.layer_validation.loader import load_all
from dealix.layer_validation.spec import ENTERPRISE_LAYERS
from dealix.layer_validation.validation_engine import (
    BLOCKED,
    PARTIAL,
    READY,
    LayerResult,
    all_ready,
    validate_all_layers,
)

REPO = Path(__file__).resolve().parents[1]


def _result(layer_id: str, score: int, status: str) -> LayerResult:
    spec = next(s for s in ENTERPRISE_LAYERS if s.id == layer_id)
    return LayerResult(layer_id, spec.order, spec.title, score, status)


def _all_ready_results() -> dict[str, LayerResult]:
    return {spec.id: _result(spec.id, 95, READY) for spec in ENTERPRISE_LAYERS}


def test_dependency_gate_blocks_layer_above_a_failed_layer() -> None:
    results = _all_ready_results()
    results["foundation"] = _result("foundation", 50, PARTIAL)

    ve._apply_dependency_gate(results)

    assert results["foundation"].status == PARTIAL
    # Every layer above Foundation is blocked even with a perfect own score.
    for spec in ENTERPRISE_LAYERS:
        if spec.id == "foundation":
            continue
        assert results[spec.id].status == BLOCKED
        assert results[spec.id].capped_by == "foundation"


def test_dependency_gate_capped_by_nearest_failed_dependency() -> None:
    results = _all_ready_results()
    results["governance"] = _result("governance", 30, ve.MISSING)

    ve._apply_dependency_gate(results)

    # Layers 1-4 stay READY; governance fails; 6-8 are blocked by governance.
    assert results["memory_knowledge"].status == READY
    assert results["observability"].capped_by == "governance"
    assert results["evaluation"].capped_by == "governance"
    assert results["executive_intelligence"].capped_by == "governance"


def test_cross_layer_critical_failure_caps_owner_to_partial() -> None:
    results = _all_ready_results()
    cross_checks = [
        {
            "gate": "memory_respects_tenant_isolation",
            "owner_layer": "memory_knowledge",
            "severity": "critical",
            "passed": False,
            "blockers": ["memory_knowledge_no_tenant_isolation_reference"],
        }
    ]
    apply_cross_layer_caps(results, cross_checks)
    assert results["memory_knowledge"].status == PARTIAL
    assert results["memory_knowledge"].capped_by == "cross_layer:memory_respects_tenant_isolation"


def test_high_severity_cross_layer_failure_does_not_cap() -> None:
    results = _all_ready_results()
    cross_checks = [
        {
            "gate": "workflows_respect_permissions",
            "owner_layer": "workflow_engine",
            "severity": "high",
            "passed": False,
            "blockers": ["x"],
        }
    ]
    apply_cross_layer_caps(results, cross_checks)
    assert results["workflow_engine"].status == READY


def test_simulated_regression_blocks_the_whole_stack(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_validate = ve.validate_layer

    def fake_validate(layer_id: str, *, run_tests: bool = False) -> LayerResult:
        result = real_validate(layer_id, run_tests=run_tests)
        if layer_id == "foundation":
            result.score = 10
            result.status = ve.MISSING
        return result

    monkeypatch.setattr(ve, "validate_layer", fake_validate)
    results = validate_all_layers()
    assert not all_ready(results)
    assert results["foundation"].status == ve.MISSING
    assert results["executive_intelligence"].status == BLOCKED


def test_current_cross_layer_checks_all_pass() -> None:
    cross_checks = run_cross_layer_checks(load_all())
    failed = [c["gate"] for c in cross_checks if not c["passed"]]
    assert failed == [], f"cross-layer failures: {failed}"


def test_verify_layers_script_report_only_exits_zero() -> None:
    proc = subprocess.run(  # noqa: S603
        [sys.executable, str(REPO / "scripts" / "verify_layers.py"), "--report-only"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "ENTERPRISE_LAYER_VALIDATION" in proc.stdout
