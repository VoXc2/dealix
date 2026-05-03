"""
Live-action gates must default to safe (false / blocked) at module import.

This test pins the safe defaults so a future commit that flips a gate
without an explicit migration path is caught immediately.
"""

from __future__ import annotations

import importlib

from auto_client_acquisition.customer_ops import build_demo_company_brain
from auto_client_acquisition.safety import classify_intent, ActionMode


def test_settings_whatsapp_allow_live_send_defaults_false() -> None:
    """`Settings.whatsapp_allow_live_send` must default False."""
    settings_mod = importlib.import_module("core.config.settings")
    Settings = getattr(settings_mod, "Settings", None)
    if Settings is None:
        # Fallback to function get_settings()
        s = settings_mod.get_settings()
    else:
        # Build with no env to isolate the model default
        s = Settings()
    assert getattr(s, "whatsapp_allow_live_send", True) is False


def test_company_brain_blocks_unsafe_channels_by_default() -> None:
    b = build_demo_company_brain()
    blocked = set(b["blocked_channels"])
    must_be_blocked = {
        "cold_whatsapp",
        "purchased_lists_whatsapp",
        "scraped_lists_whatsapp",
        "linkedin_automation",
    }
    missing = must_be_blocked - blocked
    assert not missing, f"channels missing from blocked floor: {missing}"


def test_classifier_default_path_does_not_unlock_execute() -> None:
    d = classify_intent("أبي عملاء أكثر")
    assert d.action_mode != ActionMode.APPROVED_EXECUTE
