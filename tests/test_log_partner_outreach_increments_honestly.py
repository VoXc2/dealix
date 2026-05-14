"""Tests for scripts/log_partner_outreach.py — the honest-marker discipline.

The whole point of this script is that it CANNOT be tricked into
inflating `outreach_sent_count`. These tests enforce that.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "log_partner_outreach.py"
_spec = importlib.util.spec_from_file_location("log_partner_outreach_mod", _SCRIPT)
logger = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(logger)


def test_refuses_without_really_flag(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(logger, "LOG_PATH", tmp_path / "log.json")
    rc = logger.main([
        "--partner", "Test",
        "--archetype", "Big 4 / Assurance Partner",
        "--channel", "email",
    ])
    assert rc == 2  # REFUSED
    err = capsys.readouterr().err
    assert "REFUSED" in err
    # No file written.
    assert not (tmp_path / "log.json").exists()


def test_with_really_flag_creates_entry_and_increments(monkeypatch, tmp_path):
    log_path = tmp_path / "log.json"
    monkeypatch.setattr(logger, "LOG_PATH", log_path)
    rc = logger.main([
        "--really-i-sent-this",
        "--partner", "Test Partner",
        "--archetype", "Big 4 / Assurance Partner",
        "--channel", "email",
    ])
    assert rc == 0
    data = json.loads(log_path.read_text())
    assert data["outreach_sent_count"] == 1
    assert len(data["entries"]) == 1
    assert data["entries"][0]["partner_name"] == "Test Partner"
    assert data["entries"][0]["entry_id"]
    assert data["entries"][0]["git_author"]
    assert data["ceo_complete"] is True


def test_counter_stays_in_lockstep_with_entries(monkeypatch, tmp_path):
    log_path = tmp_path / "log.json"
    monkeypatch.setattr(logger, "LOG_PATH", log_path)
    for i in range(3):
        rc = logger.main([
            "--really-i-sent-this",
            "--partner", f"P{i}",
            "--archetype", "SAMA / Regulated Technology Processor",
            "--channel", "linkedin_human",
        ])
        assert rc == 0
    data = json.loads(log_path.read_text())
    assert data["outreach_sent_count"] == len(data["entries"]) == 3


def test_invalid_archetype_refused(monkeypatch, tmp_path):
    monkeypatch.setattr(logger, "LOG_PATH", tmp_path / "log.json")
    with pytest.raises(SystemExit):
        logger.log_outreach(
            partner="X", archetype="Made up archetype", channel="email",
        )


def test_invalid_channel_refused(monkeypatch, tmp_path):
    monkeypatch.setattr(logger, "LOG_PATH", tmp_path / "log.json")
    with pytest.raises(SystemExit):
        logger.log_outreach(
            partner="X",
            archetype="Big 4 / Assurance Partner",
            channel="sms_blast",  # not in VALID_CHANNELS
        )
