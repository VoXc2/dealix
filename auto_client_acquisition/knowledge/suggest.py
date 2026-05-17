"""Source-grounded answer suggestion.

``suggest_answer`` returns an answer ONLY when an approved KB article
matches the query with sufficient confidence. No match → ``found=False``
with reason ``insufficient_evidence`` and the query is recorded as a gap.
This is the strict source-grounding the support replies and chat widget
depend on — never answer without a cited approved source.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.knowledge.article_store import ArticleStore
from auto_client_acquisition.knowledge.gaps import GapStore, record_gap
from auto_client_acquisition.knowledge.search import search_articles

# Minimum token-overlap score for an answer to be considered grounded.
CONFIDENCE_THRESHOLD: float = 0.34


def suggest_answer(
    query: str,
    *,
    store: ArticleStore | None = None,
    gap_store: GapStore | None = None,
    record_gaps: bool = True,
) -> dict[str, Any]:
    """Suggest a KB-grounded answer for ``query``.

    Returns a dict with ``found``; when found, ``article_id``, ``answer_ar``,
    ``answer_en``, ``confidence`` and ``citations``. When not found,
    ``reason="insufficient_evidence"`` and a gap is recorded.
    """
    ranked = search_articles(query, status="approved", limit=3, store=store)
    top = ranked[0] if ranked else None

    if top is None or top[1] < CONFIDENCE_THRESHOLD:
        if record_gaps:
            if gap_store is not None:
                gap_store.record(query)
            else:
                record_gap(query)
        return {
            "found": False,
            "reason": "insufficient_evidence",
            "query": query,
            "confidence": round(top[1], 3) if top else 0.0,
        }

    article, score = top
    return {
        "found": True,
        "query": query,
        "article_id": article.article_id,
        "answer_ar": article.body_ar,
        "answer_en": article.body_en,
        "confidence": round(score, 3),
        "citations": [
            {"article_id": a.article_id, "slug": a.slug, "score": round(s, 3)}
            for a, s in ranked
        ],
    }
