"""Knowledge v10 RAG — ingestion + cosine retrieval over the JSONL store."""

from __future__ import annotations

import pytest

from auto_client_acquisition.knowledge_v10 import RetrievalRequest, SourceType
from auto_client_acquisition.knowledge_v10.ingestion import chunk_text, ingest_text
from auto_client_acquisition.knowledge_v10.retrieval_contract import retrieve
from auto_client_acquisition.knowledge_v10.store import JsonlKnowledgeStore

_KEYWORDS = ("logistics", "retail", "riyadh", "saudi")


def _fake_vec(text: str) -> list[float]:
    """Deterministic keyword-count embedding (non-zero fallback)."""
    low = text.lower()
    vec = [float(low.count(k)) for k in _KEYWORDS]
    return vec if any(vec) else [1.0, 1.0, 1.0, 1.0]


async def _fake_embed_batch(texts: list[str]) -> list[list[float]]:
    return [_fake_vec(t) for t in texts]


async def _fake_embed_one(text: str) -> list[float]:
    return _fake_vec(text)


@pytest.fixture()
def store(tmp_path):
    return JsonlKnowledgeStore(path=tmp_path / "knowledge-chunks.jsonl")


def test_chunk_text_splits_paragraphs():
    text = "\n\n".join(["para one " * 30, "para two " * 30, "para three " * 30])
    chunks = chunk_text(text, max_chars=300)
    assert len(chunks) >= 3
    assert all(len(c) <= 300 for c in chunks)


def test_chunk_text_keeps_short_text_as_one():
    assert chunk_text("short note") == ["short note"]


@pytest.mark.asyncio
async def test_ingest_and_retrieve_roundtrip(store):
    await ingest_text(
        document_id="doc_logistics",
        text="A logistics company in Riyadh moving freight across Saudi Arabia.",
        customer_handle="acme",
        store=store,
        embed_fn=_fake_embed_batch,
    )
    await ingest_text(
        document_id="doc_retail",
        text="A retail brand opening retail stores in malls.",
        customer_handle="acme",
        store=store,
        embed_fn=_fake_embed_batch,
    )

    req = RetrievalRequest(
        query="logistics freight in riyadh",
        customer_handle="acme",
        allowed_sources=[SourceType.INTERNAL_DOC],
        top_k=5,
    )
    results = await retrieve(req, store=store, embed_fn=_fake_embed_one)

    assert results, "retrieval must return chunks (not the old [] stub)"
    assert results[0].document_id == "doc_logistics"
    assert 0.0 <= results[0].score <= 1.0


@pytest.mark.asyncio
async def test_retrieval_is_tenant_scoped(store):
    await ingest_text(
        document_id="doc_a",
        text="Logistics intelligence for tenant A in Riyadh.",
        customer_handle="tenant_a",
        store=store,
        embed_fn=_fake_embed_batch,
    )
    req = RetrievalRequest(
        query="logistics riyadh",
        customer_handle="tenant_b",
        allowed_sources=[SourceType.INTERNAL_DOC],
    )
    results = await retrieve(req, store=store, embed_fn=_fake_embed_one)
    assert results == []


@pytest.mark.asyncio
async def test_no_allowed_sources_returns_empty(store):
    req = RetrievalRequest(query="anything here", allowed_sources=[])
    assert await retrieve(req, store=store, embed_fn=_fake_embed_one) == []


@pytest.mark.asyncio
async def test_blocked_source_rejected_on_ingest(store):
    with pytest.raises(ValueError, match="blocked"):
        await ingest_text(
            document_id="doc_bad",
            text="scraped content",
            source_type=SourceType.BLOCKED_SCRAPING_SOURCE,
            store=store,
            embed_fn=_fake_embed_batch,
        )


@pytest.mark.asyncio
async def test_snippet_is_pii_redacted(store):
    await ingest_text(
        document_id="doc_pii",
        text="Contact the Riyadh logistics lead at founder@example.com for details.",
        customer_handle="acme",
        store=store,
        embed_fn=_fake_embed_batch,
    )
    req = RetrievalRequest(
        query="logistics contact riyadh",
        customer_handle="acme",
        allowed_sources=[SourceType.INTERNAL_DOC],
    )
    results = await retrieve(req, store=store, embed_fn=_fake_embed_one)
    assert results
    assert "founder@example.com" not in results[0].snippet_redacted
