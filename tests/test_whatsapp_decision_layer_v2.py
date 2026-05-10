"""Wave 12 §32.3.5 (Engine 5) — WhatsApp Decision Layer v2 tests.

Validates the 4 new founder-vision commands + Saudi-dialect alternates,
all per plan §32.3.5.

Hard rule preserved: every command returns one of the 5 canonical
ActionModes (preview_only / draft_only / approval_required /
approved_manual / blocked). NO auto-send. NO cold WhatsApp.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.whatsapp_decision_bot.command_parser import (
    SUPPORTED_COMMANDS,
    parse_command,
)
from auto_client_acquisition.whatsapp_decision_bot.schemas import CommandResult


# ─────────────────────────────────────────────────────────────────────
# Wave 12 §32.3.5 — 4 new commands (4 tests)
# ─────────────────────────────────────────────────────────────────────


def test_show_proof_this_week_command_recognized() -> None:
    """اعرض Proof هذا الأسبوع → show_proof_this_week (preview_only)."""
    result = parse_command(text="اعرض Proof هذا الأسبوع")
    assert isinstance(result, CommandResult)
    assert result.intent == "show_proof_this_week"
    assert result.action_mode == "preview_only"


def test_what_is_overdue_command_recognized() -> None:
    """وش المتأخر → what_is_overdue (preview_only).

    Saudi-dialect alt to overdue_deals; doesn't conflict with
    'وش الصفقات المتأخرة' (which still routes to overdue_deals).
    """
    result = parse_command(text="وش المتأخر؟")
    assert result.intent == "what_is_overdue"
    assert result.action_mode == "preview_only"


def test_prepare_exec_report_command_recognized() -> None:
    """جهز تقرير الإدارة → prepare_exec_report (draft_only — founder
    reviews + sends manually; never auto-distributed)."""
    result = parse_command(text="جهز تقرير الإدارة")
    assert result.intent == "prepare_exec_report"
    assert result.action_mode == "draft_only"


def test_show_top_decision_today_command_recognized() -> None:
    """اعرض القرار الأهم اليوم → show_top_decision_today (preview_only)."""
    result = parse_command(text="اعرض القرار الأهم اليوم")
    assert result.intent == "show_top_decision_today"
    assert result.action_mode == "preview_only"


# ─────────────────────────────────────────────────────────────────────
# Saudi-dialect alternates (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_today_status_saudi_dialect_summary() -> None:
    """ملخص اليوم → today_status (Saudi alt for وش الوضع اليوم)."""
    result = parse_command(text="ملخص اليوم")
    assert result.intent == "today_status"
    assert result.action_mode == "preview_only"


def test_top_decisions_saudi_dialect_top_n() -> None:
    """أفضل 5 فرص → top_3_decisions (Saudi alt for وش أهم 3 قرارات)."""
    result = parse_command(text="أفضل 5 فرص")
    assert result.intent == "top_3_decisions"
    assert result.action_mode == "preview_only"


def test_overdue_alt_dialects() -> None:
    """شو المتأخر / أيش المتأخر → what_is_overdue (Saudi-dialect alts)."""
    for text in ("شو المتأخر؟", "أيش المتأخر اليوم"):
        result = parse_command(text=text)
        assert result.intent == "what_is_overdue", \
            f"text={text!r} → expected what_is_overdue, got {result.intent}"


# ─────────────────────────────────────────────────────────────────────
# Hard-rule guard (3 tests)
# ─────────────────────────────────────────────────────────────────────


def test_no_command_returns_live_send_action_mode() -> None:
    """Hard rule (Article 4): WhatsApp Decision Layer NEVER returns
    a live-send action mode. Every parse must return one of the 5
    canonical modes — none of which trigger an actual send."""
    canonical_modes = {
        "preview_only", "draft_only", "approval_required",
        "approved_manual", "blocked",
    }
    test_inputs = [
        "وش الوضع اليوم",
        "ملخص اليوم",
        "أفضل 5 فرص",
        "وش المتأخر؟",
        "اعرض Proof هذا الأسبوع",
        "جهز تقرير الإدارة",
        "اعرض القرار الأهم اليوم",
        "جهز رد للعميل",
        "اعتمد الرد",
        "صعّد التذكرة",
        "وش المخاطر",
    ]
    for text in test_inputs:
        result = parse_command(text=text)
        assert result.action_mode in canonical_modes, \
            f"text={text!r} returned non-canonical action_mode={result.action_mode!r}"
        # Specifically: never a live-send variant
        assert "live" not in result.action_mode.lower(), \
            f"text={text!r} returned live-* action_mode={result.action_mode!r}"
        assert "auto_send" not in result.action_mode.lower(), \
            f"text={text!r} returned auto_send-* action_mode={result.action_mode!r}"


def test_blocked_unsafe_still_works_with_new_commands() -> None:
    """Hard rule: unsafe modifiers (blast/cold/scrape) STILL block even
    when paired with new Wave 12 commands."""
    # Try to inject an unsafe pattern alongside a new command
    result = parse_command(text="اعرض Proof للجميع blast")
    # Should be classified as blocked_unsafe (policy gate runs first)
    assert result.intent == "blocked_unsafe"
    assert result.action_mode == "blocked"


def test_supported_commands_list_includes_new_commands() -> None:
    """SUPPORTED_COMMANDS list must surface the new Wave 12 commands
    so they show up in the WhatsApp /help-style status endpoint."""
    new_commands = [
        "اعرض Proof هذا الأسبوع",
        "جهز تقرير الإدارة",
        "اعرض القرار الأهم اليوم",
    ]
    for cmd in new_commands:
        assert cmd in SUPPORTED_COMMANDS, \
            f"New Wave 12 command {cmd!r} missing from SUPPORTED_COMMANDS list"


# ─────────────────────────────────────────────────────────────────────
# Total: 10 tests (4 new commands + 3 dialect alts + 3 hard-rule guards)
# ─────────────────────────────────────────────────────────────────────
