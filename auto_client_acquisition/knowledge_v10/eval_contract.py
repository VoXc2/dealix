"""RAG evaluator — deterministic checks only.

Inspired by RAGAS faithfulness / context_relevance / answer_relevance,
but with NO LLM-as-judge. Pure heuristic checks so the bundle stays
deterministic and offline-safe.
"""
from __future__ import annotations

from auto_client_acquisition.knowledge_v10.schemas import (
    Answer,
    RAGEvalResult,
    RetrievalResult,
)


def _faithfulness(answer: Answer) -> float:
    """1.0 when every cited id is referenced in the rendered text.

    A trivial proxy for hallucination: if any citation listed in
    ``answer.citations`` does NOT appear in the answer body, drop the
    score. This catches the common failure mode of a model fabricating
    a citation that was never retrieved.
    """
    if not answer.citations:
        return 1.0 if answer.insufficient_evidence else 0.0
    body = f"{answer.answer_ar}\n{answer.answer_en}"
    found = sum(1 for c in answer.citations if c in body)
    return float(found) / float(len(answer.citations))


def _context_relevance(query: str, chunks: list[RetrievalResult]) -> float:
    """Crude token-overlap relevance score in [0, 1]."""
    if not chunks:
        return 0.0
    q_tokens = {t.lower() for t in query.split() if len(t) > 2}
    if not q_tokens:
        return 0.5
    scored = 0.0
    for c in chunks:
        text = (c.snippet_redacted or "").lower()
        overlap = sum(1 for t in q_tokens if t in text)
        scored += min(1.0, overlap / max(1, len(q_tokens)))
    return float(scored / len(chunks))


def _answer_relevance(query: str, answer: Answer) -> float:
    if answer.insufficient_evidence:
        return 0.0
    body = (answer.answer_ar + " " + answer.answer_en).lower()
    q_tokens = {t.lower() for t in query.split() if len(t) > 2}
    if not q_tokens:
        return 0.5
    overlap = sum(1 for t in q_tokens if t in body)
    return float(min(1.0, overlap / max(1, len(q_tokens))))


def evaluate_answer(
    answer: Answer,
    retrieved_chunks: list[RetrievalResult],
    golden_answer: str = "",
) -> RAGEvalResult:
    """Return deterministic faithfulness / context / answer relevance."""
    faith = _faithfulness(answer)
    notes = []
    if golden_answer:
        notes.append("golden_answer_provided")

    # Context relevance proxy: do retrieved chunks share tokens with
    # the rendered answer body?
    body = (answer.answer_ar + " " + answer.answer_en).strip()
    ctx = _context_relevance(body or "n/a", retrieved_chunks)
    ans_rel = _answer_relevance(body or "n/a", answer)

    hallucination = faith < 1.0 and not answer.insufficient_evidence
    return RAGEvalResult(
        faithfulness_score=faith,
        context_relevance=ctx,
        answer_relevance=ans_rel,
        hallucination_detected=hallucination,
        notes="; ".join(notes),
    )
