"""Summaries over scored account lists (deterministic)."""

from __future__ import annotations

from typing import Any


def summarize_scored_accounts(
    scored: list[dict[str, Any]],
    *,
    top_n: int = 10,
) -> dict[str, Any]:
    """
    ``scored`` items match ``score_account_row`` output shape plus ``row`` key
    (as produced by the revenue-intelligence router).
    """
    if not scored:
        return {"count": 0, "top": [], "summary": ""}
    ordered = sorted(scored, key=lambda x: float(x.get("score") or 0.0), reverse=True)
    top = ordered[:top_n]
    summary = ", ".join(
        str((item.get("row") or {}).get("company_name") or "?") for item in top[:3]
    )
    return {"count": len(scored), "top": top, "summary": summary}


__all__ = ["summarize_scored_accounts"]
