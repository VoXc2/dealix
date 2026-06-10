from __future__ import annotations

import logging
from typing import Any

from qdrant_client import QdrantClient as _QdrantClient
from qdrant_client.http import models as qdrant_models

from .client import VectorClient
from .schemas import SearchResult, VectorPoint

logger = logging.getLogger(__name__)


class QdrantVectorClient(VectorClient):
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        grpc_port: int = 6334,
        prefer_grpc: bool = False,
        api_key: str | None = None,
        timeout: int = 30,
    ):
        self.client = _QdrantClient(
            host=host,
            port=port,
            grpc_port=grpc_port,
            prefer_grpc=prefer_grpc,
            api_key=api_key,
            timeout=timeout,
        )

    async def upsert(self, collection: str, points: list[VectorPoint]) -> None:
        qdrant_points = []
        for p in points:
            qdrant_points.append(
                qdrant_models.PointStruct(
                    id=p.id,
                    vector=p.vector,
                    payload={**p.payload, **p.metadata},
                )
            )
        self.client.upsert(
            collection_name=collection,
            points=qdrant_points,
        )
        logger.debug("Upserted %d points to collection '%s'", len(points), collection)

    async def search(
        self,
        collection: str,
        query: list[float],
        top_k: int = 10,
        score_threshold: float | None = None,
    ) -> list[SearchResult]:
        results = self.client.search(
            collection_name=collection,
            query_vector=query,
            limit=top_k,
            score_threshold=score_threshold,
        )
        return [
            SearchResult(
                id=str(r.id),
                score=r.score,
                payload=r.payload or {},
                metadata=r.payload or {},
                distance=r.score,
            )
            for r in results
        ]

    async def delete(self, collection: str, point_ids: list[str]) -> None:
        self.client.delete(
            collection_name=collection,
            points_selector=qdrant_models.PointIdsList(
                points=point_ids,
            ),
        )
        logger.debug("Deleted %d points from collection '%s'", len(point_ids), collection)

    async def create_collection(self, name: str, dims: int = 1536) -> None:
        collections = self.client.get_collections().collections
        existing = {c.name for c in collections}
        if name not in existing:
            self.client.create_collection(
                collection_name=name,
                vectors_config=qdrant_models.VectorParams(
                    size=dims,
                    distance=qdrant_models.Distance.COSINE,
                ),
            )
            logger.info("Created collection '%s' with dims=%d", name, dims)

    async def delete_collection(self, name: str) -> None:
        self.client.delete_collection(collection_name=name)
        logger.info("Deleted collection '%s'", name)

    async def list_collections(self) -> list[str]:
        collections = self.client.get_collections().collections
        return [c.name for c in collections]

    async def collection_info(self, name: str) -> dict[str, Any]:
        info = self.client.get_collection(collection_name=name)
        return {
            "name": name,
            "status": str(info.status),
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "segments_count": info.segments_count,
        }

    async def scroll(
        self,
        collection: str,
        limit: int = 100,
        offset: str | None = None,
    ) -> tuple[list[SearchResult], str | None]:
        results, next_offset = self.client.scroll(
            collection_name=collection,
            limit=limit,
            offset=offset,
        )
        search_results = [
            SearchResult(
                id=str(r.id),
                score=1.0,
                payload=r.payload or {},
                metadata=r.payload or {},
            )
            for r in results
        ]
        return search_results, next_offset

    async def health_check(self) -> bool:
        try:
            self.client.get_collections()
            return True
        except Exception as e:
            logger.warning("Qdrant health check failed: %s", e)
            return False
