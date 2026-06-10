"""Founder weekly strategy refs YAML."""

from __future__ import annotations

from pathlib import Path

from dealix.commercial_ops.strategy_refs import (
    load_founder_strategy_refs,
    strategy_links_flat,
    strategy_refs_status,
)

REPO = Path(__file__).resolve().parents[1]


def test_strategy_refs_yaml_present() -> None:
    st = strategy_refs_status()
    assert st["ok"] is True
    assert st["daily_count"] >= 2
    assert st["weekly_count"] >= 1
    assert st["missing_paths"] == []


def test_strategy_links_include_master_and_gtm() -> None:
    links = strategy_links_flat()
    assert "master_commercial" in links
    assert "founder_strongest_plan" in links
    assert "sovereign_gtm" in links
    assert "gtm_saudi_playbook" in links
    assert (REPO / links["master_commercial"]).is_file()
    assert (REPO / links["gtm_saudi_playbook"]).is_file()


def test_load_has_morning_command() -> None:
    refs = load_founder_strategy_refs()
    cmd = refs.get("morning_command") or {}
    assert "windows" in cmd or "unix" in cmd
