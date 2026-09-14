"""Current-only retrieval wrapper. Source/provenance + evidence state carried.

Missing current evidence -> HOLD or ASK, never hallucinate. Reuses
knowledge_v10 allow-list; no scraping; no relationship inference.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal

Decision = Literal["answer", "ask", "hold"]


@dataclass(frozen=True)
class KnowledgeSnapshot:
    snapshot_id: str
    retrieved_at: str
    as_of: str
    chunk_ids: tuple[str, ...] = ()
    source_types: tuple[str, ...] = ()
    current_only: bool = True
    provenance: tuple[str, ...] = ()

    def is_empty(self) -> bool:
        return len(self.chunk_ids) == 0

    def to_ref(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "retrieved_at": self.retrieved_at,
            "as_of": self.as_of,
            "chunk_ids": list(self.chunk_ids),
            "source_types": list(self.source_types),
            "current_only": self.current_only,
        }


def _utcnow() -> str:
    return datetime.now(UTC).isoformat()


def current_only_retrieve(
    *,
    query: str,
    allowed_sources: list[str] | None = None,
    top_k: int = 5,
) -> tuple[KnowledgeSnapshot, Decision, list[dict[str, Any]]]:
    """Retrieve current-only evidence via knowledge_v10 allow-list.

    Returns (snapshot, decision, evidence). Empty backend -> ('ask').
    Blocked sources are dropped before any query.
    """
    from auto_client_acquisition.knowledge_v10.retrieval_contract import retrieve
    from auto_client_acquisition.knowledge_v10.schemas import RetrievalRequest, SourceType
    from auto_client_acquisition.knowledge_v10.source_policy import is_source_allowed

    raw_sources = allowed_sources or [
        SourceType.OFFICIAL_PUBLIC_SITE.value,
        SourceType.CUSTOMER_PROVIDED_URL.value,
        SourceType.INTERNAL_DOC.value,
    ]
    allowed = [s for s in raw_sources if is_source_allowed(s)]
    now = _utcnow()
    snap_id = f"snap_{uuid.uuid4().hex[:12]}"

    if not query or len(query.strip()) < 3 or not allowed:
        snap = KnowledgeSnapshot(
            snapshot_id=snap_id, retrieved_at=now, as_of=now, provenance=tuple(allowed)
        )
        return snap, "ask", []

    try:
        req = RetrievalRequest(
            query=query[:500],
            top_k=max(1, min(int(top_k), 20)),
            allowed_sources=[SourceType(s) for s in allowed],  # type: ignore[arg-type]
        )
        results = retrieve(req)
    except Exception:
        results = []

    allowed_results = [r for r in results if is_source_allowed(r.source_type)]
    # Current-only: drop anything explicitly marked historical/stale.
    current = [
        r
        for r in allowed_results
        if "historical" not in str(r.chunk_id).lower()
        and "archive" not in str(r.document_id).lower()
    ]
    evidence = [
        {
            "source": str(r.source_type),
            "uri": r.document_id,
            "excerpt": r.snippet_redacted[:500],
            "evidence_level": "L2",
            "retrieved_at": now,
            "current_only": True,
        }
        for r in current
    ]
    snap = KnowledgeSnapshot(
        snapshot_id=snap_id,
        retrieved_at=now,
        as_of=now,
        chunk_ids=tuple(r.chunk_id for r in current),
        source_types=tuple(str(r.source_type) for r in current),
        provenance=tuple(allowed),
    )
    if not evidence:
        return snap, "ask", []
    return snap, "answer", evidence
