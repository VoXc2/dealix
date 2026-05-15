"""Taxonomy of input signals that feed the board decision loop."""

from __future__ import annotations

BOARD_DECISION_INPUT_SIGNALS: tuple[str, ...] = (
    "sales_signals",
    "client_adoption_signals",
    "proof_signals",
    "governance_events",
    "data_patterns",
    "workflow_friction",
    "productization_candidates",
    "partner_signals",
    "market_trends",
    "financial_metrics",
)


def board_input_signal_valid(signal: str) -> bool:
    return signal in BOARD_DECISION_INPUT_SIGNALS
