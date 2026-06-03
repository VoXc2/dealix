"""Backend router — picks retrieval strategy from the request shape."""
from __future__ import annotations

from auto_client_acquisition.knowledge_v10.schemas import (
    RetrievalRequest,
    SourceType,
)


def route_search(req: RetrievalRequest) -> dict:
    """Pick a backend.

    Heuristic:
      * No allowed_sources → ``"none"`` (will return empty)
      * Only INTERNAL_DOC  → ``"keyword_match"`` (cheap, local)
      * Mixed sources       → ``"vector_db_pending"`` (Qdrant ships in §S6)
    """
    allowed = list(req.allowed_sources)
    if not allowed:
        return {"backend": "none", "reason": "no_allowed_sources"}

    only_internal = all(
        (s.value if hasattr(s, "value") else str(s))
        == SourceType.INTERNAL_DOC.value
        for s in allowed
    )
    if only_internal:
        return {"backend": "keyword_match", "reason": "internal_doc_only"}

    return {
        "backend": "vector_db_pending",
        "reason": "mixed_sources_require_vector_db",
        "ships_in": "S6",
    }
