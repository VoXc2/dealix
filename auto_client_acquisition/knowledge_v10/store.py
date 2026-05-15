"""Knowledge chunk store — one async interface, pluggable backend.

`KnowledgeStore` is the single interface `retrieve()` and `ingest_text()`
depend on. Two backends share it:

  - `JsonlKnowledgeStore` — append-only JSONL; cosine ranking in Python.
    Default; verifiable without a database. Mirrors the value_ledger store.
  - `PgKnowledgeStore`    — PostgreSQL-backed (db.models.KnowledgeChunkRecord),
    selected via DEALIX_KNOWLEDGE_BACKEND=pgvector. Cosine ranking stays in
    Python; a pgvector ANN index is a later ALTER.

Storage path (JSONL): $DEALIX_KNOWLEDGE_STORE_PATH (default var/knowledge-chunks.jsonl).
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol
from uuid import uuid4


@dataclass
class KnowledgeChunk:
    """One retrievable unit of a document, with its embedding vector."""

    chunk_id: str = field(default_factory=lambda: f"chk_{uuid4().hex[:12]}")
    document_id: str = ""
    customer_handle: str = ""
    source_type: str = "internal_doc"
    text: str = ""
    embedding: list[float] = field(default_factory=list)
    language: str = "ar"
    ingested_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class KnowledgeStore(Protocol):
    """Backend-agnostic async chunk store interface."""

    async def add_chunks(self, chunks: list[KnowledgeChunk]) -> int: ...

    async def iter_chunks(
        self, customer_handle: str | None = None
    ) -> list[KnowledgeChunk]: ...


_DEFAULT_PATH = "var/knowledge-chunks.jsonl"
_lock = threading.Lock()


def _resolve_path() -> Path:
    p = Path(os.environ.get("DEALIX_KNOWLEDGE_STORE_PATH", _DEFAULT_PATH))
    if not p.is_absolute():
        # store.py → knowledge_v10 → auto_client_acquisition → repo root
        p = Path(__file__).resolve().parents[2] / p
    return p


class JsonlKnowledgeStore:
    """Append-only JSONL store. Cosine ranking is done by the caller."""

    def __init__(self, path: Path | None = None) -> None:
        self._path = path or _resolve_path()

    async def add_chunks(self, chunks: list[KnowledgeChunk]) -> int:
        if not chunks:
            return 0
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with _lock, self._path.open("a", encoding="utf-8") as f:
            for c in chunks:
                f.write(json.dumps(c.to_dict(), ensure_ascii=False) + "\n")
        return len(chunks)

    async def iter_chunks(
        self, customer_handle: str | None = None
    ) -> list[KnowledgeChunk]:
        if not self._path.exists():
            return []
        out: list[KnowledgeChunk] = []
        with _lock, self._path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    chunk = KnowledgeChunk(**json.loads(line))
                except Exception:  # noqa: S112 — best-effort: skip a corrupt line
                    continue
                if customer_handle and chunk.customer_handle != customer_handle:
                    continue
                out.append(chunk)
        return out


class PgKnowledgeStore:
    """PostgreSQL-backed store over db.models.KnowledgeChunkRecord."""

    async def add_chunks(self, chunks: list[KnowledgeChunk]) -> int:
        if not chunks:
            return 0
        from db.models import KnowledgeChunkRecord
        from db.session import get_session

        async with get_session() as session:
            for c in chunks:
                session.add(
                    KnowledgeChunkRecord(
                        chunk_id=c.chunk_id,
                        document_id=c.document_id,
                        customer_handle=c.customer_handle,
                        source_type=c.source_type,
                        text=c.text,
                        embedding_json=c.embedding,
                        language=c.language,
                        meta_json=c.metadata,
                    )
                )
            await session.commit()
        return len(chunks)

    async def iter_chunks(
        self, customer_handle: str | None = None
    ) -> list[KnowledgeChunk]:
        from sqlalchemy import select

        from db.models import KnowledgeChunkRecord
        from db.session import get_session

        async with get_session() as session:
            stmt = select(KnowledgeChunkRecord)
            if customer_handle:
                stmt = stmt.where(
                    KnowledgeChunkRecord.customer_handle == customer_handle
                )
            rows = (await session.execute(stmt)).scalars().all()

        return [
            KnowledgeChunk(
                chunk_id=r.chunk_id,
                document_id=r.document_id,
                customer_handle=r.customer_handle,
                source_type=r.source_type,
                text=r.text,
                embedding=list(r.embedding_json or []),
                language=r.language,
                ingested_at=r.created_at.isoformat() if r.created_at else "",
                metadata=dict(r.meta_json or {}),
            )
            for r in rows
        ]


def clear_for_test() -> None:
    """Test-only: truncate the JSONL store."""
    p = _resolve_path()
    if p.exists():
        with _lock:
            p.write_text("", encoding="utf-8")


def get_store() -> KnowledgeStore:
    """Return the configured knowledge store (DEALIX_KNOWLEDGE_BACKEND)."""
    backend = os.environ.get("DEALIX_KNOWLEDGE_BACKEND", "jsonl").lower()
    if backend == "jsonl":
        return JsonlKnowledgeStore()
    if backend in ("pgvector", "postgres", "pg"):
        return PgKnowledgeStore()
    raise ValueError(f"unknown DEALIX_KNOWLEDGE_BACKEND: {backend!r}")


__all__ = [
    "JsonlKnowledgeStore",
    "KnowledgeChunk",
    "KnowledgeStore",
    "PgKnowledgeStore",
    "clear_for_test",
    "get_store",
]
