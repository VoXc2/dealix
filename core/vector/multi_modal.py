from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from .client import VectorClient
from .embedding_pipeline import EmbeddingPipeline
from .schemas import MultiModalDocument, SearchResult, VectorPoint

logger = logging.getLogger(__name__)


class MultiModalRAG:
    def __init__(
        self,
        vector_client: VectorClient,
        embedding_pipeline: EmbeddingPipeline,
        image_model: str = "clip-vit-base-patch32",
        text_collection: str = "multi_modal_text",
        image_collection: str = "multi_modal_image",
    ):
        self.vector_client = vector_client
        self.embedding = embedding_pipeline
        self.image_model = image_model
        self.text_collection = text_collection
        self.image_collection = image_collection

    async def embed_text(self, text: str) -> list[float]:
        return await self.embedding.embed(text)

    async def embed_image(self, image_path: str) -> list[float]:
        try:
            import torch
            import torchvision.transforms as transforms
            from PIL import Image
            from transformers import CLIPModel, CLIPProcessor
        except ImportError:
            raise ImportError(
                "torch, torchvision, pillow, and transformers are required "
                "for image embeddings: pip install torch torchvision pillow transformers"
            )

        model_name = self.image_model
        if not hasattr(self, "_clip_model"):
            self._clip_model = CLIPModel.from_pretrained(model_name)
            self._clip_processor = CLIPProcessor.from_pretrained(model_name)

        image = Image.open(image_path).convert("RGB")
        inputs = self._clip_processor(images=image, return_tensors="pt")
        with torch.no_grad():
            embedding = self._clip_model.get_image_features(**inputs)
        return embedding[0].tolist()

    async def search_multi(
        self,
        query: str,
        top_k: int = 10,
        collections: list[str] | None = None,
    ) -> list[SearchResult]:
        targets = collections or [self.text_collection, self.image_collection]
        query_vector = await self.embed_text(query)

        all_results: list[SearchResult] = []
        for coll in targets:
            try:
                results = await self.vector_client.search(
                    collection=coll,
                    query=query_vector,
                    top_k=top_k,
                )
                for r in results:
                    r.metadata["source_collection"] = coll
                all_results.extend(results)
            except Exception as e:
                logger.warning("Search failed on collection '%s': %s", coll, e)

        all_results.sort(key=lambda r: r.score, reverse=True)
        return all_results[:top_k]

    async def index_text(
        self,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        await self.vector_client.create_collection(self.text_collection)
        embedding = await self.embed_text(text)
        doc = MultiModalDocument(
            text=text,
            embedding=embedding,
            metadata=metadata or {},
            modality="text",
        )
        point = VectorPoint(
            vector=embedding,
            payload={"content": text, "modality": "text", **(metadata or {})},
            metadata=metadata or {},
        )
        await self.vector_client.upsert(self.text_collection, [point])
        return doc.id

    async def index_image(
        self,
        image_path: str,
        caption: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        await self.vector_client.create_collection(self.image_collection)
        embedding = await self.embed_image(image_path)
        path = Path(image_path)
        doc = MultiModalDocument(
            image_path=image_path,
            text=caption or path.name,
            embedding=embedding,
            metadata=metadata or {},
            modality="image",
        )
        point = VectorPoint(
            vector=embedding,
            payload={
                "image_path": image_path,
                "caption": caption or path.name,
                "modality": "image",
                **(metadata or {}),
            },
            metadata=metadata or {},
        )
        await self.vector_client.upsert(self.image_collection, [point])
        return doc.id
