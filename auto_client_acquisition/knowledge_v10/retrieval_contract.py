"""Retrieval interface — stub.

The real Qdrant adapter ships in §S6. Until then this enforces the
source allow-list and returns an empty list. Filtering blocked
sources is done up-front so a later wired-in adapter can NEVER
accidentally surface a denied source type.
"""
from __future__ import annotations

from auto_client_acquisition.knowledge_v10.schemas import (
    RetrievalRequest,
    RetrievalResult,
)
from auto_client_acquisition.knowledge_v10.source_policy import is_source_allowed


def retrieve(req: RetrievalRequest) -> list[RetrievalResult]:
    """Return retrieval results for ``req``.

    Stub interface — returns ``[]``. Real Qdrant adapter ships in §S6.
    Even when wired, this function MUST drop any result whose
    ``source_type`` fails ``is_source_allowed``.
    """
    # Filter the request itself first — never query a denied source.
    allowed = [s for s in req.allowed_sources if is_source_allowed(s)]
    if not allowed:
        return []
    # No backend wired yet → empty.
    return []
