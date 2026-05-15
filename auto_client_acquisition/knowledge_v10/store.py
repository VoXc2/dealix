"""Knowledge chunk store — one interface, pluggable backend.

`KnowledgeStore` is the single interface `retrieve()` and `ingest_text()`
depend on. Two backends share it:

  - `JsonlKnowledgeStore`  — append-only JSONL; cosine ranking in Python.
    Default; verifiable without a database. Mirrors the store pattern of
    value_ledger.py / capital_ledger.py.
  - pgvector               — production backend (next Phase-1 increment),
    selected via DEALIX_KNOWLEDGE_BACKEND=pgvector.

Storage path: $DEALIX_KNOWLEDGE_STORE_PATH (default var/knowledge-chunks.jsonl).
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
    """Backend-agnostic chunk store interface."""

    def add_chunks(self, chunks: list[KnowledgeChunk]) -> int: ...

    def iter_chunks(self, customer_handle: str | None = None) -> list[KnowledgeChunk]: ...


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

    def add_chunks(self, chunks: list[KnowledgeChunk]) -> int:
        if not chunks:
            return 0
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with _lock, self._path.open("a", encoding="utf-8") as f:
            for c in chunks:
                f.write(json.dumps(c.to_dict(), ensure_ascii=False) + "\n")
        return len(chunks)

    def iter_chunks(self, customer_handle: str | None = None) -> list[KnowledgeChunk]:
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
    if backend == "pgvector":
        raise NotImplementedError(
            "pgvector knowledge backend ships in the next Phase-1 increment; "
            "set DEALIX_KNOWLEDGE_BACKEND=jsonl until then."
        )
    raise ValueError(f"unknown DEALIX_KNOWLEDGE_BACKEND: {backend!r}")


__all__ = [
    "JsonlKnowledgeStore",
    "KnowledgeChunk",
    "KnowledgeStore",
    "clear_for_test",
    "get_store",
]
