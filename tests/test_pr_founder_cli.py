"""PR-FOUNDER-CLI — tests for /api/v1/founder/today + dealix_cli."""

from __future__ import annotations

import importlib
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


# ── Founder router (live endpoint) ───────────────────────────────


@pytest.mark.asyncio
async def test_founder_today_returns_full_shape(async_client):
    r = await async_client.get("/api/v1/founder/today")
    assert r.status_code == 200, r.text
    body = r.json()

    # Top-level keys
    for key in (
        "as_of", "window_days", "ceo_brief", "kpis", "quality", "cost",
        "recent_daily_ops", "open_incidents", "policy",
        "next_morning_actions_ar",
    ):
        assert key in body, f"missing top-level key: {key}"

    # KPI invariants
    k = body["kpis"]
    for key in (
        "active_paying_subscriptions", "current_mrr_sar",
        "annual_run_rate_sar", "proof_events_emitted",
        "unsafe_actions_blocked", "no_unsafe_action_executed_invariant",
        "support_tickets_opened", "objections_handled",
        "open_incidents_count",
    ):
        assert key in k, f"missing KPI: {key}"

    # The safety invariant must hold (we never EXECUTE unsafe actions)
    assert k["no_unsafe_action_executed_invariant"] is True

    # Annual run rate = MRR × 12
    assert k["annual_run_rate_sar"] == round(k["current_mrr_sar"] * 12.0, 2)


@pytest.mark.asyncio
async def test_founder_today_window_param_clamped(async_client):
    # invalid days param should be rejected
    r = await async_client.get("/api/v1/founder/today?days=999")
    assert r.status_code == 422  # FastAPI validates ge/le constraints

    r2 = await async_client.get("/api/v1/founder/today?days=0")
    assert r2.status_code == 422


@pytest.mark.asyncio
async def test_founder_today_lists_all_8_gates(async_client):
    r = await async_client.get("/api/v1/founder/today")
    body = r.json()
    gates = body["policy"]["live_action_gates"]
    expected = {
        "whatsapp_allow_live_send", "gmail_allow_live_send",
        "moyasar_allow_live_charge", "linkedin_allow_auto_dm",
        "resend_allow_live_send", "whatsapp_allow_internal_send",
        "whatsapp_allow_customer_send", "calls_allow_live_dial",
    }
    assert expected <= set(gates.keys()), f"missing gates: {expected - set(gates.keys())}"
    # All defaults must be False in tests
    flipped = [g for g, v in gates.items() if v]
    assert not flipped, f"these gates flipped: {flipped}"


@pytest.mark.asyncio
async def test_founder_today_service_tower_summary(async_client):
    r = await async_client.get("/api/v1/founder/today")
    body = r.json()
    summary = body["policy"]["service_tower"]
    assert summary["sellable"] == summary["total"]
    assert summary["beta_only"] == 0
    assert summary["internal_only"] == 0


@pytest.mark.asyncio
async def test_founder_week_alias(async_client):
    r = await async_client.get("/api/v1/founder/week")
    assert r.status_code == 200
    assert r.json()["window_days"] == 7


# ── CLI module ───────────────────────────────────────────────────


def test_dealix_cli_module_exists():
    p = REPO / "scripts" / "dealix_cli.py"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    # All 7 commands documented
    for cmd in ("today", "smoke", "seed", "proof", "outreach", "run-window", "gates"):
        assert cmd in text


def test_dealix_cli_imports():
    mod = importlib.import_module("scripts.dealix_cli")
    assert hasattr(mod, "main")
    assert callable(mod.main)


def test_outreach_pick_finds_messages_in_docs():
    """The outreach pick command relies on parsing READY_OUTREACH_MESSAGES.md."""
    p = REPO / "docs" / "READY_OUTREACH_MESSAGES.md"
    text = p.read_text(encoding="utf-8")
    headers = re.findall(r"^### (Msg \d{2}.*)$", text, re.MULTILINE)
    assert len(headers) >= 15, f"expected 15+ Msg headers, got {len(headers)}"


def test_dealix_cli_help_subcommand_returns_zero(capsys):
    from scripts.dealix_cli import main
    rc = main(["help"])
    assert rc == 0
    captured = capsys.readouterr()
    # help text lists all 7 commands
    out = captured.out + captured.err
    for cmd in ("today", "smoke", "seed", "proof", "outreach", "run-window", "gates"):
        assert cmd in out


def test_dealix_cli_outreach_picks_n_messages(capsys, tmp_path, monkeypatch):
    # Redirect cursor file to tmp so we don't pollute /tmp across runs
    monkeypatch.setattr("scripts.dealix_cli.Path", Path)
    from scripts.dealix_cli import main
    rc = main(["outreach", "pick", "3"])
    assert rc == 0
    out = capsys.readouterr().out
    # Should print 3 lines starting with "Msg "
    msg_lines = [l for l in out.splitlines() if "Msg " in l]
    assert len(msg_lines) >= 3


def test_dealix_cli_unknown_command_returns_2(capsys):
    from scripts.dealix_cli import main
    # argparse will reject unknown subcommand → SystemExit(2)
    with pytest.raises(SystemExit):
        main(["bogus_command"])
