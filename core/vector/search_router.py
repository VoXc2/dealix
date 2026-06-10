from __future__ import annotations

import asyncio
import logging
from typing import Any

from .client import VectorClient
from .embedding_pipeline import EmbeddingPipeline
from .schemas import SearchResult

logger = logging.getLogger(__name__)


class KeywordSearchEngine:
    def __init__(self, index_dir: str | None = None):
        self.index_dir = index_dir

    async def search(
        self,
        collection: str,
        query: str,
        top_k: int = 10,
    ) -> list[SearchResult]:
        query_lower = query.lower()
        tokens = set(query_lower.split())
        if not tokens:
            return []
        scored: list[tuple[float, dict[str, Any], str]] = []
        for doc_id, doc_text, doc_payload in self._iter_docs(collection):
            doc_lower = (doc_text or "").lower()
            score = sum(1 for t in tokens if t in doc_lower) / len(tokens)
            if score > 0:
                scored.append((score, doc_payload, doc_id))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            SearchResult(
                id=doc_id,
                score=score,
                payload=payload,
                metadata=payload,
            )
            for score, payload, doc_id in scored[:top_k]
        ]

    def _iter_docs(self, collection: str):
        return []

    async def index_document(
        self,
        collection: str,
        doc_id: str,
        content: str,
        payload: dict[str, Any] | None = None,
    ) -> None:
        pass


class SearchRouter:
    def __init__(
        self,
        vector_client: VectorClient,
        embedding_pipeline: EmbeddingPipeline,
        keyword_engine: KeywordSearchEngine | None = None,
        hybrid_alpha: float = 0.7,
    ):
        self.vector_client = vector_client
        self.embedding = embedding_pipeline
        self.keyword = keyword_engine or KeywordSearchEngine()
        self.hybrid_alpha = hybrid_alpha

    async def search(
        self,
        query: str,
        collection: str,
        top_k: int = 10,
        score_threshold: float | None = None,
    ) -> list[SearchResult]:
        query_vector = await self.embedding.embed(query)
        return await self.vector_client.search(
            collection=collection,
            query=query_vector,
            top_k=top_k,
        )

    async def hybrid_search(
        self,
        query: str,
        collection: str,
        top_k: int = 10,
        alpha: float | None = None,
    ) -> list[SearchResult]:
        alpha = alpha or self.hybrid_alpha
        query_vector = await self.embedding.embed(query)

        vector_results, keyword_results = await asyncio.gather(
            self.vector_client.search(
                collection=collection,
                query=query_vector,
                top_k=top_k * 2,
            ),
            self.keyword.search(
                collection=collection,
                query=query,
                top_k=top_k * 2,
            ),
        )

        merged = self._fuse_results(
            vector_results,
            keyword_results,
            alpha=alpha,
            top_k=top_k,
        )
        return merged

    def _fuse_results(
        self,
        vector_results: list[SearchResult],
        keyword_results: list[SearchResult],
        alpha: float,
        top_k: int,
    ) -> list[SearchResult]:
        scores: dict[str, dict[str, Any]] = {}

        max_v = max((r.score for r in vector_results), default=1.0)
        for r in vector_results:
            norm = r.score / max_v if max_v > 0 else 0
            scores[r.id] = {
                "result": r,
                "score": alpha * norm,
            }

        max_k = max((r.score for r in keyword_results), default=1.0)
        for r in keyword_results:
            norm = r.score / max_k if max_k > 0 else 0
            if r.id in scores:
                scores[r.id]["score"] += (1 - alpha) * norm
            else:
                scores[r.id] = {
                    "result": r,
                    "score": (1 - alpha) * norm,
                }

        sorted_results = sorted(
            scores.values(),
            key=lambda x: x["score"],
            reverse=True,
        )
        return [s["result"] for s in sorted_results[:top_k]]

    async def multi_collection_search(
        self,
        query: str,
        collections: list[str],
        top_k: int = 10,
    ) -> dict[str, list[SearchResult]]:
        results = {}
        for coll in collections:
            try:
                results[coll] = await self.search(query, coll, top_k)
            except Exception as e:
                logger.warning("Search failed for collection '%s': %s", coll, e)
                results[coll] = []
        return results
