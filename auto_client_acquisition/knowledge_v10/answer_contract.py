"""Answer synthesis — deterministic, NO LLM.

Concatenates retrieved snippets with citations. If no chunks are
provided, ``insufficient_evidence=True`` and confidence=0.0.
"""
from __future__ import annotations

from auto_client_acquisition.knowledge_v10.citation_policy import extract_citations
from auto_client_acquisition.knowledge_v10.schemas import (
    Answer,
    AnswerRequest,
    RetrievalResult,
)


def _join_snippets(chunks: list[RetrievalResult], language: str) -> str:
    """Defensive concat — limit each snippet to 240 chars."""
    parts: list[str] = []
    for c in chunks:
        snippet = (c.snippet_redacted or "").strip()
        if not snippet:
            continue
        parts.append(f"[{c.document_id}:{c.chunk_id}] {snippet[:240]}")
    return " | ".join(parts)


def answer(req: AnswerRequest) -> Answer:
    """Synthesize a deterministic answer from retrieved chunks."""
    if not req.retrieved_chunks:
        return Answer(
            answer_ar="",
            answer_en="",
            citations=[],
            confidence=0.0,
            insufficient_evidence=True,
        )

    citations = extract_citations(req.retrieved_chunks)
    body = _join_snippets(req.retrieved_chunks, req.language)
    confidence = min(0.95, 0.5 + 0.1 * len(req.retrieved_chunks))

    answer_ar = f"بناءً على المستندات: {body}" if body else ""
    answer_en = f"Based on the documents: {body}" if body else ""

    return Answer(
        answer_ar=answer_ar,
        answer_en=answer_en,
        citations=citations,
        confidence=float(confidence),
        insufficient_evidence=not bool(body),
    )
