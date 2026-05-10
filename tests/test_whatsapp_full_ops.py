"""Wave 13 Phase 7 — WhatsApp Decision Layer Full Ops tests.

Asserts:
  - build_morning_brief() produces valid structure (5 numbered items)
  - format_morning_brief() output matches §32.4A.5 template
  - render_approval_card() produces 3-action menu
  - parse_approval_response() never returns 'live_send' / 'auto_send'
  - 5 action modes: suggest_only/draft_only/approval_required/approved_manual/blocked
  - NEVER auto-sends (no SMS/WhatsApp API calls in code path)

Sandbox-safe: imports morning_brief module only.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _load():
    repo_root = Path(__file__).resolve().parent.parent
    mod_path = repo_root / "auto_client_acquisition" / "whatsapp_decision_bot" / "morning_brief.py"
    spec = importlib.util.spec_from_file_location("_test_w13_p7_mb", mod_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_test_w13_p7_mb"] = mod
    spec.loader.exec_module(mod)
    return mod


_MB = _load()
build_morning_brief = _MB.build_morning_brief
format_morning_brief = _MB.format_morning_brief
render_approval_card = _MB.render_approval_card
parse_approval_response = _MB.parse_approval_response
ACTION_MODES = _MB.ACTION_MODES


# ── Test 1 ────────────────────────────────────────────────────────────
def test_build_morning_brief_structure():
    brief = build_morning_brief(
        customer_handle="acme",
        p0_leads_count=3,
        pending_approvals_count=2,
        proof_packs_due_count=1,
        support_alerts_count=1,
        top_decision_summary="اعتماد رسالة شركة الأحمد",
    )
    assert brief["customer_handle"] == "acme"
    assert brief["counts"]["p0_leads"] == 3
    assert brief["counts"]["pending_approvals"] == 2
    assert brief["counts"]["proof_packs_due"] == 1
    assert brief["counts"]["support_alerts"] == 1
    assert "اعتماد رسالة شركة الأحمد" in brief["top_decision_summary_ar"]
    assert brief["action_mode"] == "suggest_only"
    assert brief["is_estimate"] is True
    assert set(brief["suggested_replies"]) == {"1", "2", "3", "4"}


# ── Test 2 ────────────────────────────────────────────────────────────
def test_format_morning_brief_matches_template():
    brief = build_morning_brief(
        customer_handle="acme",
        p0_leads_count=3,
        pending_approvals_count=2,
        proof_packs_due_count=1,
        support_alerts_count=1,
        top_decision_summary="اعتماد رسالة شركة الأحمد",
    )
    text = format_morning_brief(brief)
    # 5 numbered items + menu options 1-4
    assert text.startswith("صباح الخير 👋")
    assert "ملخص Dealix اليوم:" in text
    for n in ("1.", "2.", "3.", "4.", "5."):
        assert n in text, f"missing numbered item: {n}"
    # Menu options
    for opt in ("1 لعرض الفرص", "2 للموافقات", "3 للدعم", "4 للتقرير"):
        assert opt in text, f"missing menu option: {opt}"


# ── Test 3 ────────────────────────────────────────────────────────────
def test_render_approval_card_format():
    card = render_approval_card(
        approval_id="ap_t3",
        text_ar="مرحباً، رغبت بمتابعة استفساركم الأخير.",
        risk_ar="لا ترسل عبر واتساب بدون consent.",
        action_index=2,
    )
    assert "الرسالة 2:" in card
    assert "مرحباً" in card
    assert "المخاطر:" in card
    assert "القرار:" in card
    # All 3 numbered options present with correct action_mode tags
    assert "1 اعتماد" in card and "approved_manual" in card
    assert "2 تعديل" in card and "draft_only" in card
    assert "3 رفض" in card and "blocked" in card
    assert "ap_t3" in card


# ── Test 4 ────────────────────────────────────────────────────────────
def test_parse_approval_response_action_modes():
    """Article 4: parse must never return live_send/auto_send."""
    # 1 = approved_manual
    r = parse_approval_response(response="1")
    assert r["action_mode"] == "approved_manual"
    # 2 = draft_only (edit)
    r = parse_approval_response(response="2")
    assert r["action_mode"] == "draft_only"
    # 3 = blocked
    r = parse_approval_response(response="3")
    assert r["action_mode"] == "blocked"
    # Unrecognized → suggest_only (safest default)
    r = parse_approval_response(response="hello")
    assert r["action_mode"] == "suggest_only"

    # Article 4: forbidden modes never returned
    forbidden = {"live_send", "auto_send", "auto_charge", "live_charge"}
    for resp in ["1", "2", "3", "hello", "اعتمد", "ارفض"]:
        result = parse_approval_response(response=resp)
        assert result["action_mode"] not in forbidden


# ── Test 5 ────────────────────────────────────────────────────────────
def test_no_live_send_in_module_code_path():
    """Module must not import any WhatsApp send API or call any send fn.

    Article 4 NO_LIVE_SEND: scan the morning_brief module source for
    forbidden tokens.
    """
    repo_root = Path(__file__).resolve().parent.parent
    src = (repo_root / "auto_client_acquisition" / "whatsapp_decision_bot" / "morning_brief.py").read_text(encoding="utf-8")
    # Forbidden function names / API calls
    forbidden_calls = [
        re.compile(r"\bsend_text\s*\("),
        re.compile(r"\bsend_message\s*\("),
        re.compile(r"\bwhatsapp_send\s*\("),
        re.compile(r"\bsmtp\b", re.IGNORECASE),
        re.compile(r"\brequests\.\s*post\s*\("),
        re.compile(r"\bhttpx\.\s*post\s*\("),
    ]
    for pat in forbidden_calls:
        m = pat.search(src)
        assert m is None, f"morning_brief.py calls forbidden API: {m.group(0) if m else ''}"
    # Verify ACTION_MODES taxonomy correct
    assert ACTION_MODES == ("suggest_only", "draft_only", "approval_required",
                            "approved_manual", "blocked")
    assert "live_send" not in ACTION_MODES
    assert "auto_send" not in ACTION_MODES
