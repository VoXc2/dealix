"""
Knowledge ingestion — splits content into chunks, embeds, and stores
in `knowledge_chunks` (pgvector).

LlamaIndex is used when installed; otherwise we fall back to a naive
recursive splitter so the pipeline keeps working in dev.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class Chunk:
    text: str
    order: int
    meta: dict[str, str]


def _naive_split(text: str, chunk_chars: int = 1200, overlap: int = 120) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    out: list[str] = []
    i = 0
    while i < len(text):
        out.append(text[i : i + chunk_chars])
        i += chunk_chars - overlap
    return out


def split(text: str) -> list[Chunk]:
    """Return ordered chunks with order index + empty meta."""
    try:
        from llama_index.core.node_parser import SentenceSplitter  # type: ignore

        splitter = SentenceSplitter(chunk_size=512, chunk_overlap=64)
        pieces = [n.text for n in splitter.get_nodes_from_documents(
            __import__("llama_index").core.Document(text=text) for _ in [0]
        )]
    except Exception:
        pieces = _naive_split(text)
    return [Chunk(text=p, order=i, meta={}) for i, p in enumerate(pieces) if p.strip()]


async def embed_chunks(chunks: Iterable[Chunk]) -> list[tuple[Chunk, list[float], str]]:
    """Return (chunk, vector, model) tuples."""
    from dealix.rag.embeddings import embed

    out: list[tuple[Chunk, list[float], str]] = []
    for chunk in chunks:
        r = await embed(chunk.text)
        if r.provider == "none" or not r.vector:
            log.warning("embed_skipped_no_provider")
            continue
        out.append((chunk, r.vector, r.model))
    return out
