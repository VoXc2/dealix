"""
Embedding provider chain: Voyage → Cohere → OpenAI.

Voyage is the Arabic + English retrieval winner per 2026 benchmarks;
Cohere multilingual is the open fallback; OpenAI text-embedding-3-small
keeps the chain alive when neither is configured.

Returns a 1024-dim vector for Voyage / Cohere, 1536-dim for OpenAI.
The dimension is recorded next to each chunk so we never mix sizes.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class EmbedResult:
    vector: list[float]
    model: str
    provider: Literal["voyage", "cohere", "openai", "none"]


_VOYAGE_URL = "https://api.voyageai.com/v1/embeddings"
_COHERE_URL = "https://api.cohere.ai/v1/embed"
_OPENAI_URL = "https://api.openai.com/v1/embeddings"


async def embed(text: str, *, input_type: str = "search_document") -> EmbedResult:
    """Embed a single string. Picks the first configured provider."""
    voyage_key = os.getenv("VOYAGE_API_KEY", "").strip()
    if voyage_key:
        try:
            async with httpx.AsyncClient(timeout=20) as c:
                r = await c.post(
                    _VOYAGE_URL,
                    headers={"Authorization": f"Bearer {voyage_key}"},
                    json={"model": "voyage-3", "input": [text], "input_type": input_type},
                )
                r.raise_for_status()
                data = r.json()
            vec = data["data"][0]["embedding"]
            return EmbedResult(vector=vec, model="voyage-3", provider="voyage")
        except Exception:
            log.exception("voyage_embed_failed")

    cohere_key = os.getenv("COHERE_API_KEY", "").strip()
    if cohere_key:
        try:
            async with httpx.AsyncClient(timeout=20) as c:
                r = await c.post(
                    _COHERE_URL,
                    headers={"Authorization": f"Bearer {cohere_key}"},
                    json={
                        "model": "embed-multilingual-v3.0",
                        "texts": [text],
                        "input_type": "search_document"
                        if input_type == "search_document"
                        else "search_query",
                    },
                )
                r.raise_for_status()
                data = r.json()
            vec = data["embeddings"][0]
            return EmbedResult(vector=vec, model="cohere-embed-v3", provider="cohere")
        except Exception:
            log.exception("cohere_embed_failed")

    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key:
        try:
            async with httpx.AsyncClient(timeout=20) as c:
                r = await c.post(
                    _OPENAI_URL,
                    headers={"Authorization": f"Bearer {openai_key}"},
                    json={"model": "text-embedding-3-small", "input": text},
                )
                r.raise_for_status()
                data = r.json()
            vec = data["data"][0]["embedding"]
            return EmbedResult(vector=vec, model="text-embedding-3-small", provider="openai")
        except Exception:
            log.exception("openai_embed_failed")

    return EmbedResult(vector=[], model="none", provider="none")
