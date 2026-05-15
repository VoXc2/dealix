"""Answer synthesis — grounded, cited, hallucination-resistant.

Two entry points:
  - ``answer_query``      — synchronous, deterministic. Always available,
    even with no LLM keys. The agent runtime and tests use this.
  - ``answer_query_llm``  — async. Adds an LLM-written narrative grounded
    *only* in the retrieved snippets; falls back to the deterministic
    answer on any LLM failure. The HTTP router uses this.

Invariant (``no_source_no_answer``): zero retrieved chunks ⇒
``Answer(insufficient_evidence=True)`` with empty citations. An answer is
never produced from outside the retrieved evidence.
"""
from __future__ import annotations

from auto_client_acquisition.knowledge_os.index import KnowledgeIndex
from auto_client_acquisition.knowledge_os.knowledge_ledger import emit_knowledge_event
from auto_client_acquisition.knowledge_os.retriever import retrieve
from auto_client_acquisition.knowledge_os.schemas import (
    Answer,
    KnowledgeEvent,
    RetrievalRequest,
    RetrievalResult,
)

__all__ = ["answer_query", "answer_query_llm"]

_MAX_ANSWER_CHARS = 4000


def _record(request: RetrievalRequest, results: list[RetrievalResult]) -> None:
    emit_knowledge_event(
        KnowledgeEvent(
            customer_handle=request.customer_handle,
            kind="query_answered" if results else "retrieval_empty",
            query=request.query[:200],
            source_types=tuple(sorted({r.source_type for r in results})),
            chunk_count=len(results),
            citation_count=len(results),
            insufficient_evidence=not results,
        )
    )


def _deterministic_answer(request: RetrievalRequest, results: list[RetrievalResult]) -> Answer:
    if not results:
        return Answer(insufficient_evidence=True)
    extract = "\n---\n".join(r.snippet_redacted for r in results if r.snippet_redacted)
    extract = extract[:_MAX_ANSWER_CHARS]
    citations = [r.chunk_id for r in results]
    confidence = round(min(max(results[0].score, 0.0), 1.0), 4)
    lang = request.language
    return Answer(
        answer_ar=extract if lang in ("ar", "both") else "",
        answer_en=extract if lang == "en" else "",
        citations=citations,
        confidence=confidence,
        insufficient_evidence=False,
    )


def answer_query(request: RetrievalRequest, *, index: KnowledgeIndex) -> Answer:
    """Synchronous, deterministic grounded answer. Records to the ledger."""
    results = retrieve(request, index=index)
    _record(request, results)
    return _deterministic_answer(request, results)


async def answer_query_llm(request: RetrievalRequest, *, index: KnowledgeIndex) -> Answer:
    """Grounded answer with an LLM-written narrative; deterministic fallback."""
    results = retrieve(request, index=index)
    _record(request, results)
    base = _deterministic_answer(request, results)
    if not results:
        return base

    snippets = "\n\n".join(
        f"[{r.chunk_id}] {r.snippet_redacted}" for r in results if r.snippet_redacted
    )
    system = (
        "You are Dealix Knowledge OS. Answer ONLY from the provided snippets. "
        "If the snippets do not contain the answer, say so. Never invent facts. "
        "Cite the [chunk_id] tags you used. Reply in the user's language."
    )
    prompt = f"Question: {request.query}\n\nSnippets:\n{snippets}"
    try:
        from core.config.models import Task
        from core.llm.router import get_router

        response = await get_router().run(
            Task.SUMMARY, prompt, system=system, max_tokens=1024, temperature=0.2
        )
        narrative = (response.content or "").strip()
    except Exception:  # noqa: BLE001 — any LLM failure ⇒ deterministic answer
        return base
    if not narrative:
        return base

    narrative = narrative[:_MAX_ANSWER_CHARS]
    lang = request.language
    return Answer(
        answer_ar=narrative if lang in ("ar", "both") else "",
        answer_en=narrative if lang == "en" else "",
        citations=base.citations,
        confidence=base.confidence,
        insufficient_evidence=False,
    )
