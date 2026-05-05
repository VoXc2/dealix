"""Finance guardrails — single place that answers the live-charge question.

Reads only env state; never mutates. The CLI in scripts/dealix_invoice.py
already enforces this at runtime; this module exposes the same logic
to other Python callers (e.g. tests, dashboards).
"""
from __future__ import annotations

import os
from typing import Any


def _moyasar_key() -> str:
    return os.getenv("MOYASAR_SECRET_KEY", "") or ""


def _is_live_key(key: str) -> bool:
    return key.startswith("sk_live_")


def is_live_charge_allowed() -> dict[str, Any]:
    """Return a structured answer with the ENV-state reasoning."""
    key = _moyasar_key()
    has_explicit_allow = os.getenv("DEALIX_ALLOW_LIVE_CHARGE", "").strip().lower() in {
        "1", "true", "yes", "on",
    }
    if not key:
        return {
            "allowed": False,
            "reason": "MOYASAR_SECRET_KEY not set",
            "key_mode": None,
            "explicit_flag_set": has_explicit_allow,
        }
    if _is_live_key(key):
        return {
            "allowed": False,
            "reason": (
                "Moyasar key is sk_live_*. The CLI requires explicit "
                "--allow-live; no env flag enables auto-charge anywhere."
            ),
            "key_mode": "live",
            "explicit_flag_set": has_explicit_allow,
        }
    return {
        "allowed": False,
        "reason": "test-mode key — only test invoices supported",
        "key_mode": "test",
        "explicit_flag_set": has_explicit_allow,
    }


def finance_guardrails() -> dict[str, Any]:
    """Documentation of the finance-side hard rules."""
    return {
        "schema_version": 1,
        "moyasar_state": is_live_charge_allowed(),
        "rules": {
            "no_moyasar_allow_live_charge_env": True,
            "cli_refuses_live_key_without_allow_live": True,
            "no_card_data_handled_directly": True,
            "no_auto_charge": True,
            "amount_cap_per_invoice_sar": 50000,
            "pilot_price_locked_until_S1": 499,
        },
    }
