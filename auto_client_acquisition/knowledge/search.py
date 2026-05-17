"""Deterministic keyword search over knowledge articles.

No LLM: a query is tokenised and scored against each article's title,
body and tags by token overlap. Deterministic so CI is stable without
any model keys.
"""

from __future__ import annotations

import re

from auto_client_acquisition.knowledge.article_store import (
    ArticleStore,
    KnowledgeArticle,
    get_default_article_store,
)

# Arabic + Latin word characters.
_TOKEN_RE = re.compile(r"[\w؀-ۿ]+", re.UNICODE)
_STOPWORDS: frozenset[str] = frozenset(
    {
        "the", "a", "an", "is", "are", "of", "to", "and", "or", "in", "on",
        "for", "what", "how", "do", "i", "my", "we", "you",
        "ما", "هو", "هي", "كيف", "في", "من", "على", "هل", "و", "عن",
    }
)


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens with stopwords removed."""
    return [
        t for t in (m.group(0).lower() for m in _TOKEN_RE.finditer(text or ""))
        if t and t not in _STOPWORDS
    ]


def score_article(query_tokens: list[str], article: KnowledgeArticle) -> float:
    """Token-overlap score in [0, 1]. Title + tag hits weigh more than body."""
    if not query_tokens:
        return 0.0
    title_tokens = set(tokenize(article.title_ar) + tokenize(article.title_en))
    tag_tokens = {t.lower() for t in article.tags}
    body_tokens = set(tokenize(article.body_ar) + tokenize(article.body_en))

    hits = 0.0
    for tok in query_tokens:
        if tok in title_tokens or tok in tag_tokens:
            hits += 1.0
        elif tok in body_tokens:
            hits += 0.5
    return min(1.0, hits / len(query_tokens))


def search_articles(
    query: str,
    *,
    status: str | None = "approved",
    limit: int = 5,
    store: ArticleStore | None = None,
) -> list[tuple[KnowledgeArticle, float]]:
    """Return ``(article, score)`` pairs ranked by relevance, score > 0.

    Defaults to ``status="approved"`` — callers wanting drafts must opt in.
    """
    store = store or get_default_article_store()
    query_tokens = tokenize(query)
    scored = [
        (art, score_article(query_tokens, art))
        for art in store.list(status=status)
    ]
    ranked = [(art, s) for art, s in scored if s > 0.0]
    ranked.sort(key=lambda pair: pair[1], reverse=True)
    return ranked[: max(1, min(int(limit), 25))]
