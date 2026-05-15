"""Permission-aware grounded retrieval.

Wraps ``answer_with_citations`` with RBAC and tenant filtering: sources
above the caller's role, or belonging to another tenant, are dropped
before an answer is composed. If nothing survives the filter the answer
is ``insufficient_evidence`` — never a fabricated one (no_fake_proof).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from auto_client_acquisition.knowledge_os.answer_with_citations import (
    answer_with_citations,
)

# RBAC roles in ascending privilege (mirrors api/security/rbac.py).
RBAC_ROLES: tuple[str, ...] = (
    "viewer",
    "sales_rep",
    "sales_manager",
    "tenant_admin",
    "super_admin",
)
_ROLE_RANK: dict[str, int] = {role: i for i, role in enumerate(RBAC_ROLES)}


@dataclass(frozen=True, slots=True)
class RetrievalSource:
    """One retrievable knowledge source with access controls."""

    source_id: str
    excerpt: str
    min_role: str
    tenant_id: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.source_id, "excerpt": self.excerpt}


def _role_rank(role: str) -> int:
    if role not in _ROLE_RANK:
        raise ValueError(f"unknown RBAC role: {role}")
    return _ROLE_RANK[role]


def filter_by_rbac(
    sources: list[RetrievalSource],
    *,
    role: str,
    tenant_id: str,
) -> list[RetrievalSource]:
    """Keep only sources the caller may see: same tenant, role high enough."""
    caller_rank = _role_rank(role)
    kept: list[RetrievalSource] = []
    for s in sources:
        if s.tenant_id != tenant_id:
            continue
        if s.min_role not in _ROLE_RANK:
            continue
        if _ROLE_RANK[s.min_role] > caller_rank:
            continue
        kept.append(s)
    return kept


def grounded_answer(
    question: str,
    *,
    sources: list[RetrievalSource],
    role: str,
    tenant_id: str,
) -> dict[str, Any]:
    """Answer ``question`` using only RBAC- and tenant-permitted sources.

    Returns the ``answer_with_citations`` shape plus ``filtered_out``
    (count of sources dropped by the access filter).
    """
    if not question:
        raise ValueError("question is required")
    permitted = filter_by_rbac(sources, role=role, tenant_id=tenant_id)
    result = answer_with_citations(
        question, sources=[s.to_dict() for s in permitted]
    )
    result["filtered_out"] = len(sources) - len(permitted)
    result["caller_role"] = role
    return result
