"""Smoke tests for soft launch meeting preparation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


def test_prepare_soft_launch_meetings_dry_run(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[1]
    war = {
        "targets": {
            "items": [
                {
                    "company": "Test Agency Co",
                    "contact": "CEO",
                    "motion": "A",
                    "offer_id": "ten_lead_audit",
                }
            ]
        }
    }
    war_path = tmp_path / "war_room_today.json"
    war_path.write_text(json.dumps(war), encoding="utf-8")
    tracker = tmp_path / "soft_launch_meetings_tracker.yaml"

    monkeypatch.chdir(root)
    import scripts.prepare_soft_launch_meetings as mod

    monkeypatch.setattr(mod, "WAR_ROOM", war_path)
    monkeypatch.setattr(mod, "TRACKER", tracker)
    monkeypatch.setattr(
        sys,
        "argv",
        ["prepare_soft_launch_meetings.py", "--dry-run", "--top-n", "1"],
    )
    assert mod.main() == 0
    doc = yaml.safe_load(tracker.read_text(encoding="utf-8"))
    assert len(doc["meetings"]) == 1
    assert doc["meetings"][0]["company"] == "Test Agency Co"
