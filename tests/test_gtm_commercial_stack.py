"""GTM sovereign stack — KPI snapshot, daily pack, auto-send gate."""

from __future__ import annotations

import json
from pathlib import Path

from dealix.commercial_ops.daily_pack import pack_status, write_daily_pack_index
from dealix.commercial_ops.kpi_snapshot import load_kpi_commercial_status
from dealix.commercial_ops.social_queue import load_social_queue


def test_kpi_snapshot_reads_registry():
    status = load_kpi_commercial_status()
    assert status["registry_exists"] is True
    assert "pending_count" in status
    assert "ready_count" in status


def test_social_queue_eight_week_cycle():
    q = load_social_queue()
    assert int(q.get("cycle_weeks") or 0) >= 8
    posts = q.get("posts") or []
    assert len(posts) >= 35
    weeks = {int(p["week"]) for p in posts if p.get("week")}
    assert max(weeks) >= 8


def test_daily_pack_index_writes(tmp_path: Path, monkeypatch) -> None:
    import dealix.commercial_ops.daily_pack as dp

    monkeypatch.setattr(dp, "FOUNDER_BRIEFS_DIR", tmp_path)
    path = write_daily_pack_index(date_str="2026-05-17")
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "evidence_events_tracker" in text
    assert "DEALIX_API_BASE" in text
    index = json.loads((tmp_path / "index.json").read_text(encoding="utf-8"))
    assert index["first_paid_diagnostic"]["verdict"] in (
        "PIPELINE_OPEN",
        "IN_PROGRESS",
        "CLOSED",
    )
    assert index["ops_ui"]["founder"] == "/ar/ops/founder"
    assert (index.get("full_autonomous_ops") or {}).get("automation_readiness", {}).get("verdict")


def test_gtm_import_payload_valid():
    payload_path = (
        Path(__file__).resolve().parents[1]
        / "docs/commercial/operations/targeting/gtm_revenue_machine_import.json"
    )
    body = json.loads(payload_path.read_text(encoding="utf-8"))
    assert body["allowed_use"] == "business_contact_research_only"
    assert len(body["rows"]) >= 5


def test_auto_send_low_risk_disabled_by_default(monkeypatch) -> None:
    from api.routers.drafts import _auto_send_low_risk_enabled

    monkeypatch.delenv("DEALIX_ENABLE_AUTO_SEND_LOW_RISK", raising=False)
    assert _auto_send_low_risk_enabled("draft_only") is False
    assert _auto_send_low_risk_enabled("auto_send_low_risk") is False


def test_auto_send_low_risk_requires_env(monkeypatch) -> None:
    from api.routers.drafts import _auto_send_low_risk_enabled

    monkeypatch.setenv("DEALIX_ENABLE_AUTO_SEND_LOW_RISK", "1")
    assert _auto_send_low_risk_enabled("auto_send_low_risk") is True
    assert _auto_send_low_risk_enabled("draft_only") is False


def test_targeting_rotation_p0():
    from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets

    items = select_daily_p0_targets(top_n=10)
    assert isinstance(items, list)
    assert len(items) <= 10


def test_outreach_yaml_templates_merge():
    from dealix.revenue_ops_autopilot.outreach_templates import (
        _load_yaml_templates,
        build_outreach_draft,
    )

    yaml_tpl = _load_yaml_templates()
    assert "agency_wedge" in yaml_tpl or len(yaml_tpl) == 0
    text = build_outreach_draft(company="Test", contact="Ali", segment="agency_wedge")
    assert len(text) > 20


def test_digest_includes_kpi_section():
    from dealix.commercial_ops.digest import build_commercial_digest, render_digest_markdown

    digest = build_commercial_digest(skip_no_build=True)
    assert "kpi_commercial" in digest
    md = render_digest_markdown(digest)
    assert "KPI" in md or "kpi" in md.lower()
