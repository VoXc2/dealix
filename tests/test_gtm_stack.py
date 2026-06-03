"""GTM stack module — ABM scoring, dual track, debrief."""

from __future__ import annotations

from dealix.commercial_ops.founder_debrief import init_debrief, list_debriefs
from dealix.commercial_ops.gtm_stack import (
    build_abm_wave1_status,
    build_gtm_stack_snapshot,
    is_placeholder_target,
    proof_stack_for_status,
    recommend_dual_track,
    score_abm_wave1_row,
)


def test_placeholder_target_detected() -> None:
    row = {"company": "REPLACE:foo", "notes": "warm"}
    assert is_placeholder_target(row) is True


def test_score_abm_warm_row() -> None:
    row = {
        "company": "وكالة حقيقية",
        "segment": "agency_wedge",
        "pain_hypothesis": "العميل يسأل ماذا حدث بعد الحملة",
        "channel": "email_warm",
        "status": "not_contacted",
        "next_action": "مسودة",
        "priority": "high",
        "notes": "warm intro",
    }
    s = score_abm_wave1_row(row)
    assert s["score"] >= 50
    assert s["eligible"] is True


def test_gtm_snapshot_shape() -> None:
    snap = build_gtm_stack_snapshot(abm_top_n=3)
    assert snap["dual_track"]["recommended_track"] in {"A", "B"}
    assert "abm_wave1" in snap
    assert "ttv" in snap
    assert snap["playbook_path"].endswith("GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md")


def test_proof_stack_tiers() -> None:
    p = proof_stack_for_status("meeting_booked")
    assert p["minimum_tier"] == 3
    assert any("proof-pack" in a or "SAMPLE" in a for a in p["required_assets"])


def test_dual_track_returns_reason() -> None:
    d = recommend_dual_track()
    assert d["reason_ar"]
    assert d["recommended_track"] in {"A", "B"}


def test_init_debrief_writes_file(tmp_path) -> None:
    path = init_debrief(
        company="اختبار وكالة",
        contact="مدير",
        motion="A",
        offer_id="ten_lead_audit",
        out_dir=tmp_path,
    )
    assert path.is_file()
    listed = list_debriefs(limit=1)
    assert isinstance(listed, list)


def test_abm_wave_status_counts() -> None:
    st = build_abm_wave1_status(top_n=5)
    assert st["pool_rows"] >= 20
    assert "wave1_ready" in st
