"""Governed full-ops autopilot status."""

from __future__ import annotations

from dealix.commercial_ops.governed_autopilot import (
    build_governed_autopilot_status,
    write_autopilot_status_file,
)


def test_build_governed_autopilot_status_keys():
    blob = build_governed_autopilot_status()
    assert blob["mode"] == "draft_only_governed_autopilot"
    assert "expansion" in blob
    assert "phases" in blob
    assert blob["phases"]["daily_morning"]
    assert "human_required" in blob
    assert blob.get("comparison_note_ar")


def test_write_autopilot_status_file(tmp_path, monkeypatch):
    import dealix.commercial_ops.governed_autopilot as ga

    monkeypatch.setattr(ga, "FOUNDER_BRIEFS_DIR", tmp_path)
    path = write_autopilot_status_file()
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "draft_only_governed_autopilot" in text
