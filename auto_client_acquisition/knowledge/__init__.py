"""Knowledge Base — DB-of-record for approved answers + gap detection.

The KB is the single source support replies and the chat widget draw from.
Hard rule: only ``status="approved"`` articles are ever surfaced to a
customer-facing answer; publishing a draft is approval-gated.

Backend: in-memory store with JSONL persistence (stopgap, mirrors the
approval_center pattern). The public API stays stable for a DB swap.
"""

from __future__ import annotations

from auto_client_acquisition.knowledge.article_store import (
    ArticleStore,
    KnowledgeArticle,
    get_default_article_store,
    reset_default_article_store,
)
from auto_client_acquisition.knowledge.gaps import (
    GapStore,
    KnowledgeGap,
    get_default_gap_store,
    record_gap,
    reset_default_gap_store,
)
from auto_client_acquisition.knowledge.search import search_articles
from auto_client_acquisition.knowledge.suggest import suggest_answer

__all__ = [
    "ArticleStore",
    "GapStore",
    "KnowledgeArticle",
    "KnowledgeGap",
    "get_default_article_store",
    "get_default_gap_store",
    "record_gap",
    "reset_default_article_store",
    "reset_default_gap_store",
    "search_articles",
    "suggest_answer",
]
