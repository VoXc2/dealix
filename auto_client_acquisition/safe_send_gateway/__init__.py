"""Wave 7.5 §24.2 Fix 4 — safe_send_gateway.

Centralizes the existing block-pattern across whatsapp_safe_send +
email_send compliance check. Both paths already block via early
return; this module:

  1. Provides a single canonical decision: `enforce_consent_or_block()`
     that raises `SendBlocked` if consent missing + audit-logs the block.
  2. Documents the existing 6 + 8 gates in one place.
  3. Adds a uniform return shape so customer-portal can render
     "blocked" reasoning consistently.

NO new behavior — every refusal already happens via existing modules.
This module just makes the rule discoverable + raises an exception
(rather than returning a result) for callers that want to fail fast.

Hard rules:
  - NO_LIVE_SEND: respected (existing whatsapp_safe_send + email_send both check)
  - NO_LIVE_CHARGE: not in scope (handled by payment_ops)
  - NO_COLD_WHATSAPP: opt-out gate
  - NO_FAKE_PROOF: not in scope (proof_ledger handles)
"""
from __future__ import annotations

from .doctrine import (
    DOCTRINE_REASONS,
    doctrine_violations_for_revenue_intelligence,
    enforce_doctrine_non_negotiables,
)
from .middleware import (
    SendBlocked,
    SendDecision,
    enforce_consent_or_block,
    summarize_gates,
)

__all__ = [
    "DOCTRINE_REASONS",
    "SendBlocked",
    "SendDecision",
    "doctrine_violations_for_revenue_intelligence",
    "enforce_consent_or_block",
    "enforce_doctrine_non_negotiables",
    "summarize_gates",
]
