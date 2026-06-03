"""Minimal CRM board snapshot (deterministic MVP; no live CRM)."""

from __future__ import annotations

from typing import Any


def crm_board_mvp_snapshot(
    *,
    opportunities: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return a Kanban-style structure for UI demos.

    Stages are fixed; items are passed through or empty example slots.
    """
    stages = ("discovery", "qualified", "proposal", "won", "lost")
    board: dict[str, list[dict[str, Any]]] = {s: [] for s in stages}
    for raw in opportunities or []:
        stage = str(raw.get("stage", "discovery")).lower()
        if stage not in board:
            stage = "discovery"
        board[stage].append(
            {
                "id": raw.get("id", "opp_unknown"),
                "title": raw.get("title", "Opportunity"),
                "amount_sar": raw.get("amount_sar"),
                "owner": raw.get("owner", "founder"),
            }
        )
    if not opportunities:
        board["discovery"] = [
            {
                "id": "demo_1",
                "title": "Lead Intelligence follow-up",
                "amount_sar": None,
                "owner": "founder",
            }
        ]
    return {
        "schema_version": 1,
        "stages": list(stages),
        "board": board,
        "source": "revenue_crm_board_mvp",
    }
