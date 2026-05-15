"""RAG-quality evals — faithfulness, grounding, hallucination.

The core hallucination test is structural and deterministic: every
citation an answer makes MUST be a chunk that was actually retrieved. A
citation outside the retrieved set is, by definition, a hallucinated
source.
"""
from __future__ import annotations

from collections.abc import Sequence

from auto_client_acquisition.evals_os.schemas import EvalResult, RAGEvalResult
from auto_client_acquisition.knowledge_os.schemas import Answer

__all__ = ["eval_rag", "rag_eval_to_result"]


def eval_rag(answer: Answer, retrieved_chunk_ids: Sequence[str]) -> RAGEvalResult:
    """Score one grounded answer against the chunks that were retrieved."""
    retrieved = set(retrieved_chunk_ids)
    citations = list(answer.citations)

    if answer.insufficient_evidence:
        # An honest "no evidence" answer is faithful by construction.
        return RAGEvalResult(
            faithfulness_score=1.0,
            context_relevance=1.0 if not retrieved else 0.0,
            answer_relevance=1.0,
            hallucination_detected=False,
            notes="insufficient_evidence — honest abstention",
        )

    cited_outside = [c for c in citations if c not in retrieved]
    hallucinated = bool(cited_outside)
    faithfulness = 0.0 if not citations else len([c for c in citations if c in retrieved]) / len(citations)
    context_relevance = 1.0 if retrieved else 0.0
    answer_relevance = 1.0 if (answer.answer_ar or answer.answer_en).strip() else 0.0

    return RAGEvalResult(
        faithfulness_score=round(faithfulness, 4),
        context_relevance=context_relevance,
        answer_relevance=answer_relevance,
        hallucination_detected=hallucinated,
        notes=("cited un-retrieved chunks: " + ", ".join(cited_outside)) if hallucinated else "",
    )


def rag_eval_to_result(
    case_id: str,
    suite_id: str,
    rag: RAGEvalResult,
) -> EvalResult:
    """Convert a ``RAGEvalResult`` into a pass/fail ``EvalResult``."""
    failures: list[str] = []
    if rag.hallucination_detected:
        failures.append(f"hallucination_detected: {rag.notes}")
    if rag.faithfulness_score < 1.0:
        failures.append(f"faithfulness below 1.0: {rag.faithfulness_score}")
    if rag.answer_relevance < 1.0:
        failures.append("answer not relevant / empty")
    score = round(
        (rag.faithfulness_score + rag.context_relevance + rag.answer_relevance) / 3.0, 4
    )
    return EvalResult(
        case_id=case_id,
        suite_id=suite_id,
        passed=not failures,
        score=score,
        failures=tuple(failures),
        metrics={
            "faithfulness": rag.faithfulness_score,
            "context_relevance": rag.context_relevance,
            "answer_relevance": rag.answer_relevance,
            "hallucination": 1.0 if rag.hallucination_detected else 0.0,
        },
    )
