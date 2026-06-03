"""Citation extraction — deterministic."""
from __future__ import annotations

from auto_client_acquisition.knowledge_v10.schemas import RetrievalResult


def extract_citations(chunks: list[RetrievalResult]) -> list[str]:
    """Return ``document_id:chunk_id`` for every chunk, in order."""
    out: list[str] = []
    seen: set[str] = set()
    for c in chunks:
        cid = f"{c.document_id}:{c.chunk_id}"
        if cid in seen:
            continue
        seen.add(cid)
        out.append(cid)
    return out
