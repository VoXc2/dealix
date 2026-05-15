"""Permission-aware retrieval.

Filters the allowed source set *before* touching the index — a blocked
source can never be a retrieval candidate. Results are tenant-scoped by
``customer_handle``.
"""
from __future__ import annotations

from auto_client_acquisition.knowledge_os.index import KnowledgeIndex
from auto_client_acquisition.knowledge_os.schemas import (
    RetrievalRequest,
    RetrievalResult,
    SourceType,
)
from auto_client_acquisition.knowledge_v10.source_policy import is_source_allowed

__all__ = ["retrieve", "default_allowed_sources"]


def default_allowed_sources() -> frozenset[str]:
    """Every source type that is *not* on the blocked list."""
    return frozenset(s.value for s in SourceType if is_source_allowed(s))


def retrieve(request: RetrievalRequest, *, index: KnowledgeIndex) -> list[RetrievalResult]:
    """Return ranked chunks for ``request``, honouring the source allow-list."""
    requested = request.allowed_sources or []
    if requested:
        allowed = frozenset(
            (s.value if isinstance(s, SourceType) else str(s))
            for s in requested
            if is_source_allowed(s)
        )
    else:
        allowed = default_allowed_sources()
    if not allowed:
        return []
    return index.search(
        request.query,
        customer_handle=request.customer_handle,
        top_k=request.top_k,
        allowed_sources=allowed,
    )
