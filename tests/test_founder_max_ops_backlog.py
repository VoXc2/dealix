"""Founder max-ops backlog and comprehensive plan extensions."""

from __future__ import annotations

from dealix.commercial_ops.founder_comprehensive_plan import (
    build_comprehensive_status,
    infer_master_execution_phase,
)
from dealix.commercial_ops.founder_max_ops_backlog import summarize_backlog


def test_backlog_has_tasks():
    s = summarize_backlog()
    assert s["total"] >= 50
    assert s["yaml_path"].endswith("founder_max_ops_backlog.yaml")


def test_comprehensive_status_includes_backlog_and_master_phase():
    blob = build_comprehensive_status()
    assert "max_ops_backlog" in blob
    assert blob["max_ops_backlog"]["total"] >= 50
    assert "master_execution_phase" in blob
    assert blob["master_execution_phase"]["active_phase"] in range(0, 6)
    assert "dogfooding" in blob


def test_infer_master_phase_respects_supports_phase():
    phase = infer_master_execution_phase(
        phase_gate={"gate_open": True, "verdict": "PASS"},
        weekly={"latest": {"supports_phase": "3"}},
    )
    assert phase["active_phase"] == 3
