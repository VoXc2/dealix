"""Knowledge OS engine — ingestion, retrieval, grounded synthesis."""
from __future__ import annotations

import pytest

from auto_client_acquisition.knowledge_os.chunker import chunk_text
from auto_client_acquisition.knowledge_os.index import InMemoryKnowledgeIndex
from auto_client_acquisition.knowledge_os.ingest import ingest_document
from auto_client_acquisition.knowledge_os.knowledge_eval import eval_retrieval_grounded
from auto_client_acquisition.knowledge_os.knowledge_ledger import list_knowledge_events
from auto_client_acquisition.knowledge_os.retriever import retrieve
from auto_client_acquisition.knowledge_os.schemas import (
    IngestRequest,
    RetrievalRequest,
    SourceType,
)
from auto_client_acquisition.knowledge_os.synthesizer import answer_query


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_KNOWLEDGE_LEDGER_PATH", str(tmp_path / "knowledge.jsonl"))
    yield


def test_chunk_text_is_deterministic() -> None:
    text = "paragraph one here.\n\nparagraph two here.\n\nparagraph three here."
    assert chunk_text(text) == chunk_text(text)
    assert all(len(c) <= 900 for c in chunk_text(text))


def test_chunk_text_empty_returns_empty() -> None:
    assert chunk_text("   ") == []


def test_ingest_rejects_blocked_source() -> None:
    index = InMemoryKnowledgeIndex()
    with pytest.raises(ValueError):
        ingest_document(
            IngestRequest(
                customer_handle="acme",
                source_type=SourceType.BLOCKED_SCRAPING_SOURCE.value,
                title="x",
                text="scraped text",
            ),
            index=index,
        )


def test_ingest_retrieve_answer_round_trip() -> None:
    index = InMemoryKnowledgeIndex()
    manifest = ingest_document(
        IngestRequest(
            customer_handle="acme",
            source_type=SourceType.MANUALLY_ENTERED_NOTE.value,
            title="pricing",
            text="Dealix retainer pricing is fifteen thousand SAR per month.",
        ),
        index=index,
    )
    assert manifest.chunk_count >= 1

    request = RetrievalRequest(query="retainer pricing monthly", customer_handle="acme")
    results = retrieve(request, index=index)
    assert results, "expected at least one retrieved chunk"

    answer = answer_query(request, index=index)
    assert answer.insufficient_evidence is False
    assert answer.citations
    # Every citation must map to a retrieved chunk — no hallucinated sources.
    retrieved_ids = {r.chunk_id for r in results}
    assert all(cid in retrieved_ids for cid in answer.citations)


def test_empty_index_yields_insufficient_evidence() -> None:
    index = InMemoryKnowledgeIndex()
    answer = answer_query(
        RetrievalRequest(query="anything goes here", customer_handle="acme"),
        index=index,
    )
    assert answer.insufficient_evidence is True
    assert answer.citations == []


def test_pii_is_redacted_before_indexing() -> None:
    index = InMemoryKnowledgeIndex()
    ingest_document(
        IngestRequest(
            customer_handle="acme",
            source_type=SourceType.MANUALLY_ENTERED_NOTE.value,
            title="contact",
            text="Email the owner at owner@example.com or call 0501234567 today.",
        ),
        index=index,
    )
    results = retrieve(
        RetrievalRequest(query="email owner call today", customer_handle="acme"),
        index=index,
    )
    blob = " ".join(r.snippet_redacted for r in results)
    assert "owner@example.com" not in blob
    assert "0501234567" not in blob


def test_tenant_isolation() -> None:
    index = InMemoryKnowledgeIndex()
    ingest_document(
        IngestRequest(
            customer_handle="tenant_a",
            source_type=SourceType.MANUALLY_ENTERED_NOTE.value,
            title="secret",
            text="Tenant A confidential roadmap detail about pricing.",
        ),
        index=index,
    )
    results = retrieve(
        RetrievalRequest(query="confidential roadmap pricing", customer_handle="tenant_b"),
        index=index,
    )
    assert results == []


def test_knowledge_ledger_records_activity() -> None:
    index = InMemoryKnowledgeIndex()
    ingest_document(
        IngestRequest(
            customer_handle="ledger_co",
            source_type=SourceType.MANUALLY_ENTERED_NOTE.value,
            title="note",
            text="Dealix managed operations covers reporting and reviews.",
        ),
        index=index,
    )
    answer_query(
        RetrievalRequest(query="managed operations reporting", customer_handle="ledger_co"),
        index=index,
    )
    events = list_knowledge_events(customer_handle="ledger_co")
    kinds = {e.kind for e in events}
    assert "document_ingested" in kinds
    assert "query_answered" in kinds


def test_eval_retrieval_grounded_helper() -> None:
    assert eval_retrieval_grounded() is True
