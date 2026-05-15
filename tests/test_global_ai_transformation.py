"""Global AI transformation program verification tests."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from subprocess import run
from types import SimpleNamespace

from auto_client_acquisition.delivery_os.control_tower import (
    DeliveryRisk,
    compute_delivery_risk_score,
    delivery_risk_band,
    stage_gate_passes,
)
from auto_client_acquisition.observability_v10 import _reset_v10_buffer
from auto_client_acquisition.observability_v10.contract_registry import validate_observability_event
from auto_client_acquisition.observability_v10.contract_trace_hook import (
    record_contract_trace_event,
)
from auto_client_acquisition.operating_finance_os.lifecycle_unit_economics import (
    LifecycleEconomicsInputs,
    compute_lifecycle_economics,
    margin_floor_violation,
)
from auto_client_acquisition.reliability_os.mission_critical_program import (
    DrillResult,
    compute_mission_critical_score,
)
from auto_client_acquisition.revenue_os.data_flywheel import (
    FlywheelInputs,
    compute_flywheel_score,
    flywheel_inputs_from_preview,
)
from dealix.execution.weekly_cross_os_snapshot import weekly_cross_os_snapshot


def test_global_transformation_verifier_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    proc = run(
        [sys.executable, "scripts/verify_global_ai_transformation.py"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "GLOBAL AI TRANSFORMATION: PASS" in proc.stdout


def test_delivery_control_tower_risk_logic() -> None:
    ok, missing = stage_gate_passes(dict.fromkeys(("intake_ready", "scope_ready", "data_ready", "governance_ready", "qa_ready", "proof_ready", "handoff_ready"), True))
    assert ok and missing == ()

    risk = DeliveryRisk(
        engagement_id="eng-1",
        blocker_count=2,
        quality_exceptions=1,
        governance_exceptions=1,
        schedule_delay_days=3,
    )
    score = compute_delivery_risk_score(risk)
    assert score > 0
    assert delivery_risk_band(score) in {"medium", "high", "critical"}


def test_observability_contract_validation() -> None:
    event = {
        "tenant_id": "tenant-a",
        "correlation_id": "corr-1",
        "run_id": "run-1",
        "event_type": "approval.submitted",
        "source_module": "approval_center",
        "actor": "agent-x",
        "occurred_at": "2026-05-15T00:00:00Z",
        "payload_schema_version": 1,
    }
    result = validate_observability_event(event)
    assert result.valid


def test_unit_economics_snapshot() -> None:
    snapshot = compute_lifecycle_economics(
        LifecycleEconomicsInputs(
            monthly_revenue_sar=12000,
            monthly_delivery_cost_sar=7000,
            acquisition_cost_sar=10000,
            retention_months=8,
            expansion_revenue_sar=8000,
        )
    )
    assert snapshot.gross_margin_pct > 0
    assert snapshot.ltv_sar > 0
    assert not margin_floor_violation(snapshot, floor_pct=30.0)


def test_flywheel_and_reliability_scores() -> None:
    flywheel = compute_flywheel_score(
        FlywheelInputs(
            source_reliability=90,
            dedupe_precision=88,
            signal_freshness=84,
            actionability_precision=82,
            outcome_conversion=75,
            learning_adoption=80,
        )
    )
    assert flywheel.overall >= 70

    mission = compute_mission_critical_score(
        drills=(
            DrillResult("rollback", True),
            DrillResult("kill_switch", True),
            DrillResult("approval_center", True),
        ),
        slo_breaches_open=0,
    )
    assert mission.status in {"enterprise_ready", "mission_critical_ready"}


def test_contract_trace_hook_records_trace() -> None:
    _reset_v10_buffer()
    try:
        stored = record_contract_trace_event(
            tenant_id="t1",
            correlation_id="c1",
            run_id="r1",
            event_type="workflow.registered",
            source_module="control_plane",
            actor="system",
            occurred_at="2026-05-15T12:00:00Z",
        )
        assert stored.correlation_id == "c1"
        assert stored.redacted_payload.get("tenant_id") == "t1"
    finally:
        _reset_v10_buffer()


def test_flywheel_inputs_from_preview_wiring() -> None:
    preview = SimpleNamespace(row_count=20, missing_pct={"field_a": 0.05, "field_b": 0.1})
    inputs = flywheel_inputs_from_preview(preview=preview, duplicates_found=2, source_passport=object())
    score = compute_flywheel_score(inputs)
    assert score.overall > 0


def test_weekly_cross_os_snapshot_integration() -> None:
    snap = weekly_cross_os_snapshot(gtm_discovery_to_pilot_conversion_pct=33.0)
    assert snap.gross_margin_pct > 0
    assert snap.flywheel_band in {"stable", "developing", "fragile", "compounding"}
    assert snap.reliability_posture_status in {"enterprise_ready", "mission_critical_ready", "not_ready"}


def test_category_expansion_gate_checker_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    proc = run(
        [sys.executable, "scripts/verify_global_ai_transformation.py", "--check-category-expansion"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_verify_category_expansion_shell_wrapper() -> None:
    root = Path(__file__).resolve().parents[1]
    bash = shutil.which("bash") or "/usr/bin/bash"
    proc = run(  # noqa: S603
        [bash, str(root / "scripts/verify_category_expansion_before_scale.sh")],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "CATEGORY_EXPANSION_GATES: PASS" in proc.stdout


def test_verify_ceo_signal_readiness_routes_transformation() -> None:
    root = Path(__file__).resolve().parents[1]
    bash = shutil.which("bash") or "/usr/bin/bash"
    proc = run(  # noqa: S603
        [bash, str(root / "scripts/verify_ceo_signal_readiness.sh"), "transformation"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    assert "GLOBAL AI TRANSFORMATION: PASS" in proc.stdout
