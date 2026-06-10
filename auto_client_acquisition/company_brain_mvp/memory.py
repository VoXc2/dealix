"""In-memory company brain chunks (MVP before pgvector tables)."""

from __future__ import annotations

import re
from threading import Lock
from typing import Any
from uuid import uuid4

_LOCK = Lock()
_STORE: dict[str, list[dict[str, Any]]] = {}


def ingest_chunk(
    *,
    workspace_id: str,
    text: str,
    source_id: str,
    title: str | None = None,
) -> dict[str, Any]:
    if not source_id.strip():
        raise ValueError("source_id required")
    if not text.strip():
        raise ValueError("text required")
    chunk = {
        "chunk_id": f"chk_{uuid4().hex[:12]}",
        "source_id": source_id.strip(),
        "title": (title or source_id).strip(),
        "text": text.strip(),
    }
    with _LOCK:
        _STORE.setdefault(workspace_id, []).append(chunk)
    return chunk


def query_workspace(
    *,
    workspace_id: str,
    question: str,
    top_k: int = 3,
) -> dict[str, Any]:
    q = question.strip().lower()
    if not q:
        return {
            "answer_mode": "insufficient_evidence",
            "answer_ar": "لا يوجد سؤال واضح.",
            "answer_en": "No clear question.",
            "citations": [],
        }
    with _LOCK:
        chunks = list(_STORE.get(workspace_id, []))
    if not chunks:
        return {
            "answer_mode": "insufficient_evidence",
            "answer_ar": "لا توجد أدلة مفهرسة بعد — ارفع مستندات مع source_id.",
            "answer_en": "No indexed evidence yet — ingest documents with source_id.",
            "citations": [],
        }

    tokens = [t for t in re.split(r"\W+", q) if len(t) > 2]
    scored: list[tuple[float, dict[str, Any]]] = []
    for c in chunks:
        blob = (c["text"] + " " + c.get("title", "")).lower()
        score = sum(1 for t in tokens if t in blob)
        scored.append((float(score), c))
    scored.sort(key=lambda x: x[0], reverse=True)
    best = [c for s, c in scored if s > 0][:top_k]
    if not best:
        return {
            "answer_mode": "insufficient_evidence",
            "answer_ar": "لا توجد مقاطع مطابقة بثقة لهذا السؤال.",
            "answer_en": "No confident chunk match for this question.",
            "citations": [],
        }

    top = best[0]
    citations = [
        {"chunk_id": top["chunk_id"], "source_id": top["source_id"], "title": top.get("title")}
    ]
    return {
        "answer_mode": "evidence_backed",
        "answer_ar": f"ملخص من المصدر {top['source_id']}: {top['text'][:400]}",
        "answer_en": f"Summary from source {top['source_id']}: {top['text'][:400]}",
        "citations": citations,
    }


def reset_workspace(workspace_id: str) -> None:
    with _LOCK:
        _STORE.pop(workspace_id, None)
