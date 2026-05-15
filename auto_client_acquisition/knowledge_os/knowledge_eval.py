"""Lightweight eval helpers for knowledge policy + grounding."""

from __future__ import annotations

from auto_client_acquisition.knowledge_os.answer_with_citations import answer_with_citations


def eval_no_source_policy() -> bool:
    """Return True if empty sources always block."""
    out = answer_with_citations("test", sources=[])
    return bool(out.get("insufficient_evidence"))


def eval_retrieval_grounded() -> bool:
    """Return True iff a retrieved answer cites only indexed chunks.

    Builds an isolated in-memory index (no ledger side effects), indexes one
    chunk, queries it, and asserts every citation maps to an indexed chunk.
    """
    from auto_client_acquisition.knowledge_os.index import InMemoryKnowledgeIndex
    from auto_client_acquisition.knowledge_os.retriever import retrieve
    from auto_client_acquisition.knowledge_os.schemas import (
        KnowledgeChunk,
        RetrievalRequest,
        SourceType,
    )
    from auto_client_acquisition.knowledge_os.synthesizer import _deterministic_answer

    index = InMemoryKnowledgeIndex()
    index.add(
        KnowledgeChunk(
            chunk_id="eval_chunk_1",
            document_id="eval_doc_1",
            customer_handle="eval_tenant",
            source_type=SourceType.MANUALLY_ENTERED_NOTE.value,
            position=0,
            snippet_redacted="Dealix retainer pricing is fifteen thousand SAR per month.",
        )
    )
    request = RetrievalRequest(query="retainer pricing monthly", customer_handle="eval_tenant")
    results = retrieve(request, index=index)
    if not results:
        return False
    answer = _deterministic_answer(request, results)
    if answer.insufficient_evidence or not answer.citations:
        return False
    indexed_ids = {r.chunk_id for r in results}
    return all(cid in indexed_ids for cid in answer.citations)
