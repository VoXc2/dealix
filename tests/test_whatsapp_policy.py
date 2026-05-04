"""
WhatsApp policy invariants — purely static checks (no live send).

Verifies:
- The classifier blocks the canonical Saudi/Arabic and English unsafe phrasings.
- The classifier returns the safe-alternatives set for every blocked decision.
- The `WHATSAPP_ALLOW_LIVE_SEND` setting defaults to False.
"""

from __future__ import annotations

import importlib

from auto_client_acquisition.safety import ActionMode, classify_intent


CANONICAL_UNSAFE = [
    "أبي أرسل واتساب لأرقام مشتريها",
    "عندي أرقام واجد أبغى أرسل لهم واتساب",
    "خل البوت يكلم الناس بالواتس",
    "أبي حملة واتساب على أرقام من السوق",
    "أبي أرسل للناس واتساب بدون ما يكلموني",
    "عندي لستة أرقام من برا وأبي أرسل لهم",
    "أبي واتساب جماعي للعملاء المحتملين",
    "أبي البوت يشطح على الناس بالواتساب",
    "أرسل واتساب بارد",
    "أبي البوت يفتح محادثات واتساب مع ناس ما يعرفوني",
    "أبي أرمي رسايل واتساب على كل اللي عندي",
    "أرسل لهم كلهم واتساب حتى لو ما وافقوا",
    "cold whatsapp blast",
    "blast whatsapp",
    "bulk whatsapp",
    "whatsapp blast",
    "scrape and message on whatsapp",
    "auto DM on whatsapp",
]


def test_canonical_unsafe_all_blocked() -> None:
    fails = []
    for s in CANONICAL_UNSAFE:
        d = classify_intent(s)
        if d.action_mode != ActionMode.BLOCKED:
            fails.append(s)
    assert not fails, f"Should block but didn't: {fails}"


def test_safe_alternatives_complete_for_every_block() -> None:
    expected = {
        "linkedin_manual_warm_intro",
        "inbound_wa_me_link",
        "opt_in_form",
        "email_draft_with_approval",
        "customer_initiated_whatsapp",
    }
    for s in CANONICAL_UNSAFE:
        d = classify_intent(s)
        assert expected.issubset(set(d.safe_alternatives)), \
            f"missing alternatives for {s!r}: got {d.safe_alternatives}"


def test_whatsapp_live_send_setting_defaults_false() -> None:
    settings_mod = importlib.import_module("core.config.settings")
    Settings = getattr(settings_mod, "Settings", None)
    if Settings is None:
        s = settings_mod.get_settings()
    else:
        s = Settings()
    assert getattr(s, "whatsapp_allow_live_send", True) is False
