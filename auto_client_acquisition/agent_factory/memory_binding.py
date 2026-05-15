"""Agent memory binding — connects an agent to the Knowledge OS retrieval layer.
ربط ذاكرة الوكيل — يربط الوكيل بطبقة الاسترجاع في Knowledge OS.

Scaffold: the binding is a permission-aware contract over ``knowledge_v10``.
An agent declares the maximum source set and customer scope it may retrieve
within; the adapter intersects that with the source allow-list so blocked
(scraping / personal-data) sources can never reach a query.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.agent_factory.knowledge_engine import SemanticChunkIndex
from auto_client_acquisition.knowledge_v10.retrieval_contract import retrieve
from auto_client_acquisition.knowledge_v10.schemas import (
    RetrievalRequest,
    RetrievalResult,
    SourceType,
)
from auto_client_acquisition.knowledge_v10.source_policy import is_source_allowed


class AgentMemoryBinding(BaseModel):
    """Declares an agent's retrieval capability and its hard scope limits.
    يعرّف قدرة الاسترجاع لدى الوكيل وحدوده الصارمة."""

    model_config = ConfigDict(extra="forbid", use_enum_values=True)

    enabled: bool = False
    customer_handle: str = ""
    allowed_sources: list[SourceType] = Field(default_factory=list)
    top_k: int = Field(default=5, ge=1, le=50)
    retrieval_mode: Literal["contract_stub", "semantic_pending"] = "contract_stub"


def binding_valid(binding: AgentMemoryBinding) -> tuple[bool, tuple[str, ...]]:
    """Return ``(ok, errors)``. A disabled binding is always valid."""
    if not binding.enabled:
        return True, ()
    errors: list[str] = []
    if not binding.customer_handle.strip():
        errors.append("customer_handle_required")
    if not [s for s in binding.allowed_sources if is_source_allowed(s)]:
        errors.append("at_least_one_allowed_source_required")
    return not errors, tuple(errors)


def build_retrieval_request(binding: AgentMemoryBinding, query: str) -> RetrievalRequest:
    """Build a permission-scoped ``RetrievalRequest``.

    The agent CANNOT widen its own scope: ``customer_handle`` is forced from
    the binding and blocked sources are dropped before the request exists.
    """
    safe_sources = [s for s in binding.allowed_sources if is_source_allowed(s)]
    return RetrievalRequest(
        query=query,
        customer_handle=binding.customer_handle,
        top_k=binding.top_k,
        allowed_sources=safe_sources,
    )


def retrieve_for_agent(
    binding: AgentMemoryBinding,
    query: str,
    *,
    index: SemanticChunkIndex | None = None,
) -> list[RetrievalResult]:
    """Retrieval path for an agent's memory.

    Validates the binding, builds a customer-scoped request, then:

      * ``retrieval_mode == "semantic_pending"`` + an ``index`` → semantic
        search through the permission-aware ``SemanticChunkIndex``.
      * otherwise → ``knowledge_v10.retrieve`` (the contract stub → ``[]``).

    The agent cannot widen its own scope: ``customer_handle`` and
    ``allowed_sources`` always come from the binding via
    ``build_retrieval_request``.
    """
    ok, _errors = binding_valid(binding)
    if not binding.enabled or not ok:
        return []
    request = build_retrieval_request(binding, query)
    if binding.retrieval_mode == "semantic_pending" and index is not None:
        return index.search(
            query,
            customer_handle=request.customer_handle,
            allowed_sources=request.allowed_sources,
            top_k=request.top_k,
        )
    return retrieve(request)


__all__ = [
    "AgentMemoryBinding",
    "binding_valid",
    "build_retrieval_request",
    "retrieve_for_agent",
]
