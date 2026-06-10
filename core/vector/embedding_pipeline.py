from __future__ import annotations

import asyncio
import logging
from typing import Any

import tiktoken
from openai import AsyncOpenAI, RateLimitError

from .schemas import (
    Document,
    DocumentEmbedding,
    EmbeddingConfig,
)

logger = logging.getLogger(__name__)


class EmbeddingPipeline:
    MODEL = "text-embedding-3-small"

    def __init__(
        self,
        api_key: str | None = None,
        config: EmbeddingConfig | None = None,
    ):
        self.client = AsyncOpenAI(api_key=api_key)
        self.config = config or EmbeddingConfig()
        self._tokenizer = tiktoken.get_encoding("cl100k_base")

    def _chunk_text(self, text: str, max_tokens: int = 8000) -> list[str]:
        tokens = self._tokenizer.encode(text)
        chunks = []
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i : i + max_tokens]
            chunks.append(self._tokenizer.decode(chunk_tokens))
        return chunks

    def _chunk_document(
        self,
        doc: Document,
        chunk_size: int = 1000,
        overlap: int = 200,
    ) -> list[Document]:
        content = doc.content
        chunks = []
        start = 0
        while start < len(content):
            end = min(start + chunk_size, len(content))
            chunk_content = content[start:end]
            chunk = Document(
                content=chunk_content,
                metadata={**doc.metadata, "chunk_index": len(chunks)},
                doc_type=doc.doc_type,
                source=doc.source,
                chunk_index=len(chunks),
            )
            chunks.append(chunk)
            start = end - overlap if end < len(content) else end
        return chunks

    async def embed(self, text: str) -> list[float]:
        for attempt in range(self.config.max_retries):
            try:
                response = await self.client.embeddings.create(
                    model=self.config.model,
                    input=text,
                    dimensions=self.config.dimensions,
                )
                return response.data[0].embedding
            except RateLimitError:
                wait = self.config.retry_delay * (2**attempt)
                logger.warning("Rate limited, retrying in %.1fs", wait)
                await asyncio.sleep(wait)
            except Exception:
                if attempt == self.config.max_retries - 1:
                    raise
                await asyncio.sleep(self.config.retry_delay)
        raise RuntimeError("Failed to embed after retries")

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        all_embeddings: list[list[float]] = []
        for i in range(0, len(texts), self.config.batch_size):
            batch = texts[i : i + self.config.batch_size]
            for attempt in range(self.config.max_retries):
                try:
                    response = await self.client.embeddings.create(
                        model=self.config.model,
                        input=batch,
                        dimensions=self.config.dimensions,
                    )
                    embeddings = [d.embedding for d in response.data]
                    all_embeddings.extend(embeddings)
                    break
                except RateLimitError:
                    wait = self.config.retry_delay * (2**attempt)
                    logger.warning("Rate limited on batch, retrying in %.1fs", wait)
                    await asyncio.sleep(wait)
                except Exception:
                    if attempt == self.config.max_retries - 1:
                        raise
                    await asyncio.sleep(self.config.retry_delay)
        return all_embeddings

    async def embed_document(self, doc: Document) -> list[DocumentEmbedding]:
        chunks = self._chunk_document(doc)
        texts = [c.content for c in chunks]
        embeddings = await self.embed_batch(texts)
        return [
            DocumentEmbedding(
                document_id=doc.id,
                chunk_index=chunks[i].chunk_index,
                embedding=embeddings[i],
                content=chunks[i].content,
                metadata=chunks[i].metadata,
            )
            for i in range(len(chunks))
        ]

    async def embed_with_chunking(self, text: str) -> list[list[float]]:
        chunks = self._chunk_text(text)
        return await self.embed_batch(chunks)

    def count_tokens(self, text: str) -> int:
        return len(self._tokenizer.encode(text))
