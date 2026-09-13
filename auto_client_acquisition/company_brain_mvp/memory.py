"""In-memory company brain chunks (MVP before pgvector tables)."""

from __future__ import annotations

import re
from threading import Lock
from typing import Any
from uuid import uuid4

from dealix.commercial.commercial_truth_authority import (
    classify_source,
    should_exclude_from_current_retrieval,
)

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
    normalized_text = text.strip()
    normalized_source = source_id.strip()
    chunk = {
        "chunk_id": f"chk_{uuid4().hex[:12]}",
        "source_id": normalized_source,
        "title": (title or source_id).strip(),
        "text": normalized_text,
        "commercial_authority_class": classify_source(normalized_source, text=normalized_text),
    }
    with _LOCK:
        _STORE.setdefault(workspace_id, []).append(chunk)
    return chunk


def query_workspace(
    *,
    workspace_id: str,
    question: str,
    top_k: int = 3,
    include_historical: bool = False,
) -> dict[str, Any]:
    """Retrieve evidence while quarantining known legacy commercial truth.

    Historical/deprecated/synthetic Dealix repository sources remain stored and
    can be requested explicitly with ``include_historical=True``. They are
    excluded from default current retrieval so old prices, fixed-five agent
    claims, or synthetic proof cannot silently become current authority.
    """
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

    if not include_historical:
        chunks = [
            chunk
            for chunk in chunks
            if not should_exclude_from_current_retrieval(
                str(chunk.get("source_id") or ""),
                text=str(chunk.get("text") or ""),
            )
        ]
        if not chunks:
            return {
                "answer_mode": "insufficient_evidence",
                "answer_ar": "المصادر المطابقة تاريخية أو غير مخولة كحقيقة تجارية حالية.",
                "answer_en": "Matching sources are historical or not authorized as current commercial truth.",
                "citations": [],
                "commercial_truth_mode": "CURRENT_ONLY",
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
    classification = classify_source(
        str(top.get("source_id") or ""), text=str(top.get("text") or "")
    )
    citations = [
        {
            "chunk_id": top["chunk_id"],
            "source_id": top["source_id"],
            "title": top.get("title"),
            "commercial_authority_class": classification,
        }
    ]
    mode = "HISTORICAL_LOOKUP_ONLY" if include_historical else "CURRENT_ONLY"
    return {
        "answer_mode": "evidence_backed",
        "answer_ar": f"ملخص من المصدر {top['source_id']}: {top['text'][:400]}",
        "answer_en": f"Summary from source {top['source_id']}: {top['text'][:400]}",
        "citations": citations,
        "commercial_truth_mode": mode,
    }


def reset_workspace(workspace_id: str) -> None:
    with _LOCK:
        _STORE.pop(workspace_id, None)
