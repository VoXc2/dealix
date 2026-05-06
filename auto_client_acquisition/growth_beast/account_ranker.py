"""Account Ranker — sorts accounts by ICP score + recency."""
from __future__ import annotations

from auto_client_acquisition.growth_beast.icp_score import ICPScore


def rank_accounts(scored: list[tuple[str, ICPScore]]) -> list[dict]:
    """Sort (placeholder, ICPScore) pairs by score desc; return top
    structured list with rank + reason."""
    sorted_items = sorted(scored, key=lambda kv: kv[1].score, reverse=True)
    out: list[dict] = []
    for i, (placeholder, sc) in enumerate(sorted_items, start=1):
        out.append({
            "rank": i,
            "placeholder": placeholder,
            "score": sc.score,
            "reason_ar": sc.reason_ar,
            "reason_en": sc.reason_en,
            "action_mode": "suggest_only",
        })
    return out
