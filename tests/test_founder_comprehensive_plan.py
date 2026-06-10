"""Founder comprehensive plan — anchors, gates, GTM, PDPL, weekly decision."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from dealix.commercial_ops.founder_comprehensive_plan import (
    analyze_gtm_codification,
    analyze_pdpl_compliance_pass,
    analyze_phase_0_1_gate,
    analyze_weekly_one_decision,
    build_comprehensive_status,
    daily_anchor_docs,
    init_weekly_decision,
)
from dealix.commercial_ops.paths import REPO_ROOT


def test_daily_anchor_docs_exist():
    anchors = daily_anchor_docs()["anchors"]
    for key in ("founder_operating_system", "master_commercial_plan", "revenue_war_room"):
        assert anchors[key]["exists"] is True


def test_build_comprehensive_status_keys():
    blob = build_comprehensive_status()
    for key in (
        "daily_anchors",
        "daily_cadence",
        "phase_0_1_gate",
        "gtm_codification",
        "pdpl_compliance_pass",
        "weekly_one_decision",
    ):
        assert key in blob


def test_phase_gate_structure():
    phase = analyze_phase_0_1_gate()
    assert phase["verdict"] in ("PASS", "IN_PROGRESS", "BLOCKED")
    assert "no_build_until_closed" in phase
    assert "first_paid" in phase


def test_pdpl_pass_reads_yaml():
    pdpl = analyze_pdpl_compliance_pass()
    assert pdpl["total"] >= 5
    assert pdpl["verdict"] in ("OPEN", "IN_PROGRESS", "PASS", "EMPTY", "MISSING_CONFIG")


def test_gtm_codification_open_by_default():
    gtm = analyze_gtm_codification()
    assert gtm["verdict"] in ("OPEN", "IN_PROGRESS", "READY")
    assert gtm["target_deals"] == 10


def test_init_weekly_decision(tmp_path, monkeypatch):
    import dealix.commercial_ops.founder_comprehensive_plan as mod

    tpl = REPO_ROOT / "docs/commercial/operations/founder_weekly_decision_template.yaml"
    assert tpl.is_file()
    monkeypatch.setattr(mod, "FOUNDER_WEEKLY_DECISION_DIR", tmp_path)
    monkeypatch.setattr(mod, "FOUNDER_WEEKLY_DECISION_TEMPLATE", tpl)
    path = init_weekly_decision(week_id="2099-W01")
    assert path.is_file()
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert data["week_id"] == "2099-W01"


def test_weekly_decision_reads_config_yaml():
    weekly = analyze_weekly_one_decision()
    assert weekly["verdict"] in ("FILLED", "STALE", "MISSING")
    latest = weekly.get("latest") or {}
    if weekly["verdict"] == "FILLED":
        assert (latest.get("one_decision") or "").strip()
    config = REPO_ROOT / "dealix/config/founder_weekly_one_decision.yaml"
    assert config.is_file()


def test_status_script_importable():
    root = Path(__file__).resolve().parents[1]
    script = root / "scripts/founder_comprehensive_plan_status.py"
    assert script.is_file()
