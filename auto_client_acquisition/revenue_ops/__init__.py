"""Governed Revenue Ops domain — engagement state machine + diagnostics.

This package backs the `/api/v1/revenue-ops` HTTP surface that implements the
Governed Revenue & AI Operations Company repositioning (2026-05-16). It is
pure, deterministic logic — no live sends, no scraping, no external action.

The engagement state machine enforces the doctrine flow:

    draft → approved → sent → used_in_meeting → scope_requested
          → invoice_sent → invoice_paid

Every transition is recorded as an evidence event. No external action is
permitted without an explicit `approved` transition (founder approval).
"""

from __future__ import annotations

from auto_client_acquisition.revenue_ops.state_machine import (
    ENGAGEMENT_STATES,
    VALID_TRANSITIONS,
    EngagementStateError,
    next_states,
    validate_transition,
)

__all__ = [
    "ENGAGEMENT_STATES",
    "VALID_TRANSITIONS",
    "EngagementStateError",
    "next_states",
    "validate_transition",
]
