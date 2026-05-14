"""Tests for board_ready_os."""

from __future__ import annotations

from auto_client_acquisition.board_ready_os import (
    BOARD_DASHBOARD_METRICS,
    BOARD_MEMO_SECTIONS,
    BOARD_ROADMAP_PHASES,
    DUE_DILIGENCE_ARTIFACTS,
    BoardRiskEntry,
    BoardRiskId,
    RevenueLine,
    agent_autonomy_board_allowed,
    board_dashboard_coverage_score,
    board_memo_sections_complete,
    build_board_memo_markdown_skeleton,
    board_risk_entry_valid,
    board_roadmap_milestone_count,
    board_roadmap_phase_name,
    due_diligence_pack_coverage_score,
    privacy_runtime_board_checklist_passes,
    revenue_line_ok_for_scale,
    unit_economics_scale_ok,
)
from auto_client_acquisition.board_ready_os.privacy_runtime_board import (
    PRIVACY_RUNTIME_BOARD_SIGNALS,
)


def test_board_dashboard() -> None:
    full = frozenset(BOARD_DASHBOARD_METRICS)
    assert board_dashboard_coverage_score(full) == 100
    assert board_dashboard_coverage_score(frozenset()) == 0


def test_board_memo() -> None:
    body = dict.fromkeys(BOARD_MEMO_SECTIONS, "x")
    assert board_memo_sections_complete(body) == (True, ())
    partial = dict(body)
    partial["proof"] = ""
    ok, miss = board_memo_sections_complete(partial)
    assert not ok and miss == ("proof",)


def test_build_board_memo_markdown_skeleton() -> None:
    sk = build_board_memo_markdown_skeleton()
    assert sk.startswith("# Dealix Board Memo\n")
    assert sk.count("\n## ") == 12
    assert "## 1. Executive Summary" in sk
    assert "## 12. Next Strategic Bet" in sk
    assert len(BOARD_MEMO_SECTIONS) == 12
    custom = build_board_memo_markdown_skeleton(title="Q1 Memo")
    assert custom.startswith("# Q1 Memo\n")


def test_due_diligence_pack() -> None:
    assert due_diligence_pack_coverage_score(frozenset(DUE_DILIGENCE_ARTIFACTS)) == 100


def test_agent_risk_board() -> None:
    assert agent_autonomy_board_allowed(2, enterprise_tier=False, mvp_organization=True)[0]
    assert not agent_autonomy_board_allowed(4, enterprise_tier=False, mvp_organization=False)[0]
    assert not agent_autonomy_board_allowed(4, enterprise_tier=False, mvp_organization=True)[0]
    assert agent_autonomy_board_allowed(4, enterprise_tier=True, mvp_organization=False)[0]
    assert not agent_autonomy_board_allowed(6, enterprise_tier=True, mvp_organization=False)[0]


def test_privacy_runtime_board() -> None:
    full = dict.fromkeys(PRIVACY_RUNTIME_BOARD_SIGNALS, True)
    assert privacy_runtime_board_checklist_passes(full) == (True, ())


def test_financial_model() -> None:
    assert revenue_line_ok_for_scale(RevenueLine.SPRINTS)
    ok, errs = unit_economics_scale_ok(
        gross_margin_pct=70.0,
        proof_strength_ok=True,
        scope_creep_high=False,
    )
    assert ok and not errs
    assert not unit_economics_scale_ok(
        gross_margin_pct=20.0,
        proof_strength_ok=True,
        scope_creep_high=False,
    )[0]


def test_board_risk_v2() -> None:
    assert len(BoardRiskId) == 12
    entry = BoardRiskEntry(
        risk_id="R11",
        owner="ciso",
        likelihood="med",
        impact="high",
        early_warning_signal="too_many_tools",
        control="agent_card",
        response_plan="reduce_permissions",
    )
    assert board_risk_entry_valid(entry)


def test_roadmap() -> None:
    assert len(BOARD_ROADMAP_PHASES) == 6
    assert board_roadmap_phase_name(1) == "proof_engine"
    assert board_roadmap_milestone_count(1) == 6
    assert board_roadmap_milestone_count(4) == 6
