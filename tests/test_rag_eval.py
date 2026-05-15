"""RAG evaluation metrics — precision/recall/MRR/hit-rate (Layer 5)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.knowledge_v10.ingestion import ingest_text
from auto_client_acquisition.knowledge_v10.rag_eval import (
    RagCase,
    evaluate_retrieval,
    retrieval_metrics,
)
from auto_client_acquisition.knowledge_v10.store import JsonlKnowledgeStore

_KEYWORDS = ("logistics", "retail", "finance", "riyadh")


def _fake_vec(text: str) -> list[float]:
    low = text.lower()
    vec = [float(low.count(k)) for k in _KEYWORDS]
    return vec if any(vec) else [1.0, 1.0, 1.0, 1.0]


async def _embed_batch(texts):
    return [_fake_vec(t) for t in texts]


async def _embed_one(text):
    return _fake_vec(text)


def test_retrieval_metrics_perfect_hit():
    m = retrieval_metrics(["d1", "d2", "d3"], {"d1"}, k=3)
    assert m.hit_rate == 1.0
    assert m.mrr == 1.0  # relevant doc is rank 1
    assert m.recall_at_k == 1.0


def test_retrieval_metrics_rank_two():
    m = retrieval_metrics(["d9", "d1"], {"d1"}, k=5)
    assert m.mrr == 0.5  # relevant doc at rank 2
    assert m.hit_rate == 1.0


def test_retrieval_metrics_miss():
    m = retrieval_metrics(["d9", "d8"], {"d1"}, k=5)
    assert m.hit_rate == 0.0
    assert m.mrr == 0.0
    assert m.recall_at_k == 0.0


@pytest.mark.asyncio
async def test_evaluate_retrieval_over_golden_corpus(tmp_path):
    store = JsonlKnowledgeStore(path=tmp_path / "k.jsonl")
    for doc_id, text in (
        ("doc_logistics", "Logistics fleet operations across Riyadh."),
        ("doc_retail", "Retail store expansion and retail merchandising."),
        ("doc_finance", "Finance reporting and finance controls."),
    ):
        await ingest_text(
            document_id=doc_id, text=text, customer_handle="acme",
            store=store, embed_fn=_embed_batch,
        )

    cases = [
        RagCase(query="logistics fleet riyadh", relevant_document_ids=["doc_logistics"],
                customer_handle="acme"),
        RagCase(query="retail merchandising store", relevant_document_ids=["doc_retail"],
                customer_handle="acme"),
        RagCase(query="finance controls reporting", relevant_document_ids=["doc_finance"],
                customer_handle="acme"),
    ]
    report = await evaluate_retrieval(cases, store=store, embed_fn=_embed_one, top_k=3)

    assert report["cases"] == 3
    # Distinct keyword vectors → every golden doc retrieved at rank 1.
    assert report["hit_rate"] == 1.0
    assert report["mean_mrr"] == 1.0
