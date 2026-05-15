"""RAG evaluation — real retrieval-quality metrics over golden cases.

Replaces deterministic shape-only checks for the knowledge layer with
precision@k / recall@k / MRR / hit-rate measured against a golden set
(query → the document_ids that should be retrieved).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from auto_client_acquisition.knowledge_v10.retrieval_contract import retrieve
from auto_client_acquisition.knowledge_v10.schemas import RetrievalRequest, SourceType
from auto_client_acquisition.knowledge_v10.store import KnowledgeStore

QueryEmbedFn = Callable[[str], Awaitable[list[float]]]


@dataclass(frozen=True)
class RetrievalMetrics:
    precision_at_k: float
    recall_at_k: float
    mrr: float
    hit_rate: float
    k: int


def retrieval_metrics(
    retrieved_ids: list[str], relevant_ids: list[str] | set[str], k: int
) -> RetrievalMetrics:
    """Precision@k, recall@k, MRR and hit-rate for a single query."""
    retrieved = retrieved_ids[:k]
    relevant = set(relevant_ids)
    hits = [d for d in retrieved if d in relevant]

    precision = len(hits) / len(retrieved) if retrieved else 0.0
    recall = len(set(hits)) / len(relevant) if relevant else 0.0

    mrr = 0.0
    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant:
            mrr = 1.0 / rank
            break

    return RetrievalMetrics(
        precision_at_k=round(precision, 4),
        recall_at_k=round(recall, 4),
        mrr=round(mrr, 4),
        hit_rate=1.0 if hits else 0.0,
        k=k,
    )


@dataclass(frozen=True)
class RagCase:
    """One golden retrieval case."""

    query: str
    relevant_document_ids: list[str]
    customer_handle: str = ""


async def evaluate_retrieval(
    cases: list[RagCase],
    *,
    store: KnowledgeStore,
    embed_fn: QueryEmbedFn,
    top_k: int = 5,
) -> dict[str, float | int]:
    """Aggregate retrieval metrics across all golden cases."""
    per_case: list[RetrievalMetrics] = []
    for case in cases:
        req = RetrievalRequest(
            query=case.query,
            customer_handle=case.customer_handle,
            allowed_sources=[SourceType.INTERNAL_DOC],
            top_k=top_k,
        )
        results = await retrieve(req, store=store, embed_fn=embed_fn)
        per_case.append(
            retrieval_metrics(
                [r.document_id for r in results], case.relevant_document_ids, top_k
            )
        )

    n = len(per_case) or 1
    return {
        "cases": len(per_case),
        "k": top_k,
        "mean_precision": round(sum(m.precision_at_k for m in per_case) / n, 4),
        "mean_recall": round(sum(m.recall_at_k for m in per_case) / n, 4),
        "mean_mrr": round(sum(m.mrr for m in per_case) / n, 4),
        "hit_rate": round(sum(m.hit_rate for m in per_case) / n, 4),
    }


__all__ = [
    "RagCase",
    "RetrievalMetrics",
    "evaluate_retrieval",
    "retrieval_metrics",
]
