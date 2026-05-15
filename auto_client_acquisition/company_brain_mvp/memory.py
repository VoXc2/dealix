"""Company Brain retrieval — workspace-scoped knowledge with citations + RBAC.

Enterprise Knowledge Center backend:
- Tenant isolation: every chunk is scoped to a ``workspace_id``.
- Permissions (RBAC): a chunk may carry ``allowed_roles``; a query only
  retrieves chunks the ``viewer_role`` is permitted to see. An empty
  ``allowed_roles`` means the chunk is visible to everyone (public).
- Citations: every answer carries the source chunks it was built from —
  no source, no answer.

Retrieval is a deterministic TF-IDF scorer over the workspace corpus
(dependency-free, CI-safe). When an embedding backend is available it can
rerank; the lexical path is always the reliable default.
"""

from __future__ import annotations

import math
import re
from threading import Lock
from typing import Any
from uuid import uuid4

_LOCK = Lock()
_STORE: dict[str, list[dict[str, Any]]] = {}

_MIN_TOKEN_LEN = 2


def _tokens(text: str) -> list[str]:
    return [t for t in re.split(r"\W+", text.lower()) if len(t) >= _MIN_TOKEN_LEN]


def ingest_chunk(
    *,
    workspace_id: str,
    text: str,
    source_id: str,
    title: str | None = None,
    allowed_roles: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Index one knowledge chunk into a workspace.

    ``allowed_roles`` empty = public (any viewer). Otherwise only a viewer
    whose role is in ``allowed_roles`` may retrieve this chunk.
    """
    if not source_id.strip():
        raise ValueError("source_id required")
    if not text.strip():
        raise ValueError("text required")
    chunk = {
        "chunk_id": f"chk_{uuid4().hex[:12]}",
        "source_id": source_id.strip(),
        "title": (title or source_id).strip(),
        "text": text.strip(),
        "allowed_roles": tuple(r.strip() for r in allowed_roles if r.strip()),
    }
    with _LOCK:
        _STORE.setdefault(workspace_id, []).append(chunk)
    return {
        "chunk_id": chunk["chunk_id"],
        "source_id": chunk["source_id"],
        "title": chunk["title"],
        "allowed_roles": list(chunk["allowed_roles"]),
    }


def _role_may_see(chunk: dict[str, Any], viewer_role: str) -> bool:
    roles = chunk.get("allowed_roles") or ()
    if not roles:
        return True  # public chunk
    return viewer_role in roles


def _idf(corpus_tokens: list[list[str]]) -> dict[str, float]:
    n = len(corpus_tokens)
    df: dict[str, int] = {}
    for toks in corpus_tokens:
        for t in set(toks):
            df[t] = df.get(t, 0) + 1
    return {t: math.log(1.0 + n / (1 + c)) for t, c in df.items()}


def query_workspace(
    *,
    workspace_id: str,
    question: str,
    top_k: int = 3,
    viewer_role: str = "",
) -> dict[str, Any]:
    """Answer a question from a workspace's indexed knowledge, with citations.

    Only chunks the ``viewer_role`` is permitted to see are retrieved.
    """
    q = question.strip()
    if not q:
        return _insufficient("لا يوجد سؤال واضح.", "No clear question.")

    with _LOCK:
        all_chunks = list(_STORE.get(workspace_id, []))
    visible = [c for c in all_chunks if _role_may_see(c, viewer_role)]
    if not all_chunks:
        return _insufficient(
            "لا توجد أدلة مفهرسة بعد — ارفع مستندات مع source_id.",
            "No indexed evidence yet — ingest documents with source_id.",
        )
    if not visible:
        return _insufficient(
            "لا توجد مقاطع ضمن صلاحيات هذا الدور.",
            "No chunks within this role's permissions.",
            governance="restricted_by_role",
        )

    corpus_tokens = [_tokens(c["text"] + " " + c.get("title", "")) for c in visible]
    idf = _idf(corpus_tokens)
    q_tokens = _tokens(q)
    q_lower = q.lower()

    scored: list[tuple[float, dict[str, Any]]] = []
    for chunk, toks in zip(visible, corpus_tokens):
        tf: dict[str, int] = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        score = sum(tf.get(t, 0) * idf.get(t, 0.0) for t in set(q_tokens))
        # Phrase bonus — exact substring of the question in the chunk.
        if q_lower in chunk["text"].lower():
            score += 5.0
        if score > 0:
            scored.append((score, chunk))

    if not scored:
        return _insufficient(
            "لا توجد مقاطع مطابقة بثقة لهذا السؤال.",
            "No confident chunk match for this question.",
        )

    scored.sort(key=lambda x: x[0], reverse=True)
    best = scored[:top_k]
    top_score, top = best[0]
    citations = [
        {
            "chunk_id": c["chunk_id"],
            "source_id": c["source_id"],
            "title": c.get("title"),
            "relevance": round(s, 3),
        }
        for s, c in best
    ]
    return {
        "answer_mode": "evidence_backed",
        "answer_ar": f"ملخص من المصدر {top['source_id']}: {top['text'][:400]}",
        "answer_en": f"Summary from source {top['source_id']}: {top['text'][:400]}",
        "citations": citations,
        "confidence": round(min(1.0, top_score / 10.0), 3),
        "governance_decision": "allow_with_review",
        "viewer_role": viewer_role or "unscoped",
    }


def _insufficient(
    ar: str, en: str, governance: str = "insufficient_evidence"
) -> dict[str, Any]:
    return {
        "answer_mode": "insufficient_evidence",
        "answer_ar": ar,
        "answer_en": en,
        "citations": [],
        "confidence": 0.0,
        "governance_decision": governance,
    }


def workspace_stats(workspace_id: str) -> dict[str, Any]:
    """Source/chunk counts for the Knowledge Center usage panel."""
    with _LOCK:
        chunks = list(_STORE.get(workspace_id, []))
    sources = sorted({c["source_id"] for c in chunks})
    return {
        "workspace_id": workspace_id,
        "chunk_count": len(chunks),
        "source_count": len(sources),
        "sources": sources,
        "restricted_chunk_count": sum(1 for c in chunks if c.get("allowed_roles")),
    }


def reset_workspace(workspace_id: str) -> None:
    with _LOCK:
        _STORE.pop(workspace_id, None)


__all__ = [
    "ingest_chunk",
    "query_workspace",
    "reset_workspace",
    "workspace_stats",
]
