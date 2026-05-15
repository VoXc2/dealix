"""Knowledge → governed EvidencePack builder (Layer 11)."""

from __future__ import annotations

from auto_client_acquisition.knowledge_v10.evidence import (
    content_hash,
    evidence_pack_from_retrieval,
    evidence_source_from_result,
)
from auto_client_acquisition.knowledge_v10.schemas import RetrievalResult, SourceType


def _result(doc: str = "doc1", chunk: str = "chk1") -> RetrievalResult:
    return RetrievalResult(
        chunk_id=chunk,
        document_id=doc,
        snippet_redacted="Riyadh logistics operations summary.",
        score=0.82,
        source_type=SourceType.INTERNAL_DOC,
    )


def test_content_hash_is_deterministic_sha256():
    h1 = content_hash("evidence text")
    h2 = content_hash("evidence text")
    assert h1 == h2
    assert h1.startswith("sha256:")
    assert content_hash("other") != h1


def test_evidence_source_has_required_fields():
    src = evidence_source_from_result(_result())
    assert src.source == "knowledge.internal_doc"
    assert src.uri == "doc://doc1/chk1"
    assert src.excerpt
    assert src.content_hash and src.content_hash.startswith("sha256:")
    assert src.retrieved_at  # spec §73 — retrieval timestamp


def test_evidence_pack_from_retrieval_threads_trace_id():
    pack = evidence_pack_from_retrieval(
        decision_id="dec_1",
        entity_id="lead_1",
        results=[_result("dA", "cA"), _result("dB", "cB")],
        tenant_id="acme",
        trace_id="trace-abc-123",
    )
    assert pack.decision_id == "dec_1"
    assert pack.tenant_id == "acme"
    assert pack.trace_id == "trace-abc-123"
    assert len(pack.sources) == 2
    assert all(s.content_hash for s in pack.sources)


def test_empty_retrieval_yields_pack_with_no_sources():
    pack = evidence_pack_from_retrieval(
        decision_id="dec_2", entity_id="lead_2", results=[],
    )
    assert pack.sources == []
    assert pack.is_complete is False
