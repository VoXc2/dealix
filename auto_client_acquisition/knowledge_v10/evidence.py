"""Build a governed EvidencePack from RAG retrieval results.

Closes the loop knowledge_v10.retrieve() → dealix.contracts.EvidencePack:
every retrieved chunk becomes an EvidenceSource with a SHA-256 content
hash, a retrievable URI and a verbatim excerpt — the basis the
Constitution (Article IV) requires for a high-stakes decision. The OTel
``trace_id`` is threaded through so the decision links to its evidence.
"""

from __future__ import annotations

import hashlib

from auto_client_acquisition.knowledge_v10.schemas import RetrievalResult
from dealix.contracts.evidence_pack import EvidencePack, EvidenceSource

_MAX_EXCERPT = 2000


def content_hash(text: str) -> str:
    """SHA-256 of the retrieved content (Evidence Pack spec §72)."""
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def evidence_source_from_result(result: RetrievalResult) -> EvidenceSource:
    """Map one retrieval result to a hashed, citable EvidenceSource."""
    excerpt = result.snippet_redacted[:_MAX_EXCERPT]
    return EvidenceSource(
        source=f"knowledge.{result.source_type}",
        uri=f"doc://{result.document_id}/{result.chunk_id}",
        excerpt=excerpt,
        content_hash=content_hash(excerpt),
    )


def evidence_pack_from_retrieval(
    *,
    decision_id: str,
    entity_id: str,
    results: list[RetrievalResult],
    agent_name: str = "knowledge_v10",
    tenant_id: str = "default",
    trace_id: str | None = None,
    model: str | None = None,
) -> EvidencePack:
    """Assemble a governed EvidencePack from retrieved knowledge chunks."""
    return EvidencePack(
        decision_id=decision_id,
        entity_id=entity_id,
        tenant_id=tenant_id,
        agent_name=agent_name,
        model=model,
        sources=[evidence_source_from_result(r) for r in results],
        trace_id=trace_id,
    )


__all__ = [
    "content_hash",
    "evidence_pack_from_retrieval",
    "evidence_source_from_result",
]
