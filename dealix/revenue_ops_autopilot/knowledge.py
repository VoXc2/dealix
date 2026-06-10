"""Load and query seeded knowledge articles (YAML)."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


def _seed_path() -> Path:
    return Path(__file__).resolve().parent / "knowledge_seed.yaml"


@lru_cache(maxsize=1)
def load_knowledge_articles() -> list[dict[str, Any]]:
    data = yaml.safe_load(_seed_path().read_text(encoding="utf-8"))
    return list(data.get("articles") or [])


def score_article_match(query_lc: str, article: dict[str, Any]) -> int:
    """Naive lexical score — deterministic, offline."""
    hay = " ".join(
        str(article.get(k) or "")
        for k in (
            "question_ar",
            "question_en",
            "answer_ar",
            "answer_en",
            "category",
            "slug",
            "title_ar",
            "title_en",
        )
    ).lower()
    tokens = [t for t in query_lc.split() if len(t) > 2]
    score = 0
    for t in tokens:
        if t in hay:
            score += 2
        if hay.startswith(t[:4]) and len(t) > 3:
            score += 1
    return score


def search_kb(query: str, *, limit: int = 5) -> list[tuple[float, dict[str, Any]]]:
    qc = query.strip().lower()
    ranked: list[tuple[float, dict[str, Any]]] = []
    for art in load_knowledge_articles():
        sc = score_article_match(qc, art)
        if sc > 0:
            ranked.append((float(sc), art))
    ranked.sort(key=lambda x: (-x[0], x[1].get("id", "")))
    return ranked[:limit]
