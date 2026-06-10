from dealix.commercial_ops.founder_agent_tasks import analyze_agent_queue_status
from dealix.commercial_ops.founder_master_strategic_os import (
    run_founder_master_strategic_os,
    wave_d_cadence_unify,
)
from dealix.commercial_ops.phase_01_close_path import build_phase_01_close_path
from dealix.commercial_ops.platform_v10_readiness import analyze_platform_v10_readiness


def test_agent_queue() -> None:
    s = analyze_agent_queue_status()
    assert s["verdict"] in ("PASS", "WARN", "FAIL")


def test_strategic_os() -> None:
    p = run_founder_master_strategic_os(skip_live=True)
    assert p["verdict"] in ("PASS", "WARN", "FAIL")


def test_wave_d() -> None:
    assert wave_d_cadence_unify()["verdict"] == "OK"


def test_phase_01() -> None:
    assert build_phase_01_close_path()["verdict"] in ("PASS", "IN_PROGRESS", "BLOCKED")


def test_v10_blocked() -> None:
    b = analyze_platform_v10_readiness()
    if not b.get("phase_01", {}).get("gate_open"):
        assert b["verdict"] == "BLOCKED"
