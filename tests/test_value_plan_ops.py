"""Commercial value-plan ops — weekly scorecard + first-paid evidence (no invented CRM)."""

from __future__ import annotations

from dealix.commercial_ops.evidence_csv import is_placeholder_evidence_row, real_evidence_rows
from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.value_plan import build_value_plan_snapshot
from dealix.commercial_ops.weekly_scorecard_commercial import (
    build_weekly_scorecard,
    render_weekly_scorecard_markdown,
)


def test_analyze_first_paid_diagnostic_shape():
    blob = analyze_first_paid_diagnostic()
    assert blob["verdict"] in ("CLOSED", "IN_PROGRESS", "PIPELINE_OPEN")
    assert "payment_received_real" in blob
    assert "proof_pack_delivered_real" in blob
    assert blob["total_events"] >= 0


def test_build_weekly_scorecard_shape():
    blob = build_weekly_scorecard()
    assert blob["week_end"]
    assert blob["week_start"]
    assert "kpi_week" in blob
    assert blob["first_paid_verdict"] in ("CLOSED", "IN_PROGRESS", "PIPELINE_OPEN")
    assert blob["template_doc"].endswith("COMMERCIAL_WEEKLY_SCORECARD_AR.md")


def test_render_weekly_scorecard_markdown_includes_kpis():
    blob = build_weekly_scorecard()
    md = render_weekly_scorecard_markdown(blob)
    assert "Commercial Weekly Scorecard" in md
    assert "payment_received" in md
    assert blob["week_end"] in md


def test_placeholder_evidence_rows_excluded_from_real():
    rows = [
        {"company": "", "notes": "template_funnel_seed", "event_type": "invoice_sent"},
        {"company": "Acme Agency", "notes": "warm intro", "event_type": "invoice_sent"},
    ]
    assert is_placeholder_evidence_row(rows[0])
    assert not is_placeholder_evidence_row(rows[1])
    assert len(real_evidence_rows(rows)) == 1


def test_build_value_plan_snapshot_schema():
    snap = build_value_plan_snapshot(motion_top_n=3)
    assert snap["schema_version"] == "1.0"
    assert "first_paid_diagnostic" in snap
    assert "evidence" in snap
    assert "evidence_all_rows" in snap
    assert snap["ops_ui"]["founder"] == "/ar/ops/founder"


def test_build_value_plan_snapshot_shape():
    from dealix.commercial_ops.value_plan import build_value_plan_snapshot

    snap = build_value_plan_snapshot(motion_top_n=3)
    assert snap["schema_version"] == "1.0"
    assert snap["motion_a"]["targets"]
    assert "warnings_ar" in snap
    assert snap["ops_ui"]["founder"] == "/ar/ops/founder"


def test_motion_a_pipeline_plan_shape():
    from dealix.commercial_ops.motion_a_pipeline import build_motion_a_pipeline_plan

    plan = build_motion_a_pipeline_plan(top_n=3)
    assert plan["motion"] == "A"
    assert plan.get("targets")


def test_evening_reminder_ar():
    from dealix.commercial_ops.evidence_append import evening_reminder_ar

    blob = evening_reminder_ar(rows=[])
    assert "logged_today" in blob
