"""Tests for scripts/run_revenue_intelligence_demo.py — governed, no external send."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_revenue_intelligence_demo.py"
_spec = importlib.util.spec_from_file_location("revenue_demo_mod", _SCRIPT)
demo = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(demo)


def test_demo_run_produces_proof_pack(tmp_path, monkeypatch):
    monkeypatch.setattr(demo, "DEMO_DIR", tmp_path)
    payload = demo.run_demo()
    assert payload["is_demo"] is True
    assert payload["proof_pack"]["is_demo"] is True
    assert len(payload["sample_accounts"]) >= 3
    assert len(payload["proof_pack"]["ranked_accounts"]) == len(payload["sample_accounts"])


def test_demo_blocks_account_without_consent(tmp_path, monkeypatch):
    """Doctrine #2 / #6 / #7: no outreach without consent."""
    monkeypatch.setattr(demo, "DEMO_DIR", tmp_path)
    payload = demo.run_demo()
    drafts = payload["proof_pack"]["drafts_governed"]
    blocked = [d for d in drafts if d["governance_status"] == "BLOCK"]
    # The synthetic dataset includes one no-consent account → must be blocked.
    assert any(
        "consent" in (d.get("reason") or "").lower() or "threshold" in (d.get("reason") or "").lower()
        for d in blocked
    )


def test_every_draft_is_draft_only_or_block(tmp_path, monkeypatch):
    """Doctrine #2: no draft is ever sent. All outputs are DRAFT_ONLY or BLOCK."""
    monkeypatch.setattr(demo, "DEMO_DIR", tmp_path)
    payload = demo.run_demo()
    for d in payload["proof_pack"]["drafts_governed"]:
        assert d["governance_status"] in ("DRAFT_ONLY", "BLOCK")
    eligible = [d for d in payload["proof_pack"]["drafts_governed"] if d["governance_status"] == "DRAFT_ONLY"]
    for d in eligible:
        assert d["approval_required_before_send"] is True


def test_doctrine_check_flags_are_set(tmp_path, monkeypatch):
    monkeypatch.setattr(demo, "DEMO_DIR", tmp_path)
    payload = demo.run_demo()
    checks = payload["proof_pack"]["doctrine_checks"]
    assert checks["no_scraping"] is True
    assert checks["no_cold_whatsapp"] is True
    assert checks["no_linkedin_automation"] is True
    assert checks["no_guaranteed_claims"] is True
    assert checks["human_approval_before_external_action"] is True


def test_capital_event_is_recorded(tmp_path, monkeypatch):
    monkeypatch.setattr(demo, "DEMO_DIR", tmp_path)
    payload = demo.run_demo()
    ce = payload["capital_event"]
    assert ce["asset_type"] == "proof_example"
    assert ce["is_demo"] is True
    assert ce["entry_id"]


def test_demo_writes_json_and_md(tmp_path, monkeypatch):
    monkeypatch.setattr(demo, "DEMO_DIR", tmp_path)
    payload = demo.run_demo()
    rid = payload["run_id"]
    assert (tmp_path / f"revenue_intelligence_demo_{rid}.json").exists()
    md = (tmp_path / f"revenue_intelligence_demo_{rid}.md").read_text()
    assert "Demo only" in md
    assert "Doctrine Checks" in md


def test_demo_md_contains_no_real_pii(tmp_path, monkeypatch):
    """The demo dataset is synthetic — must not include any real client name."""
    monkeypatch.setattr(demo, "DEMO_DIR", tmp_path)
    payload = demo.run_demo()
    rid = payload["run_id"]
    md = (tmp_path / f"revenue_intelligence_demo_{rid}.md").read_text()
    # All sample accounts must be prefixed with "Demo".
    for acct in payload["sample_accounts"]:
        assert acct["company"].lower().startswith("demo"), acct["company"]
