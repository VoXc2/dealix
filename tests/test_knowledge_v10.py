"""Tests for knowledge_v10 — RAG contract."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from auto_client_acquisition.knowledge_v10 import (
    Answer,
    AnswerRequest,
    DocumentManifest,
    RetrievalRequest,
    RetrievalResult,
    SourceType,
    answer,
    evaluate_answer,
    extract_citations,
    is_source_allowed,
    retrieve,
    route_search,
    validate_manifest,
)


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


def test_source_type_has_nine_values():
    assert len(list(SourceType)) == 9
    expected = {
        "customer_provided_url", "customer_uploaded_file",
        "official_public_site", "search_api_result", "crm_record",
        "internal_doc", "manually_entered_note",
        "blocked_scraping_source", "blocked_personal_data_source",
    }
    assert {s.value for s in SourceType} == expected


def test_blocked_scraping_source_is_denied():
    assert is_source_allowed(SourceType.BLOCKED_SCRAPING_SOURCE) is False


def test_blocked_personal_data_source_is_denied():
    assert is_source_allowed(SourceType.BLOCKED_PERSONAL_DATA_SOURCE) is False


def test_internal_doc_is_allowed():
    assert is_source_allowed(SourceType.INTERNAL_DOC) is True


def test_official_public_site_is_allowed():
    assert is_source_allowed(SourceType.OFFICIAL_PUBLIC_SITE) is True


@pytest.mark.asyncio
async def test_retrieve_with_no_allowed_sources_returns_empty():
    req = RetrievalRequest(query="how do we onboard", allowed_sources=[])
    assert await retrieve(req) == []


@pytest.mark.asyncio
async def test_retrieve_with_only_blocked_sources_returns_empty():
    req = RetrievalRequest(
        query="anything goes",
        allowed_sources=[SourceType.BLOCKED_SCRAPING_SOURCE],
    )
    assert await retrieve(req) == []


def test_answer_with_empty_chunks_returns_insufficient_evidence():
    req = AnswerRequest(query="what is our pricing", retrieved_chunks=[])
    out = answer(req)
    assert isinstance(out, Answer)
    assert out.insufficient_evidence is True
    assert out.confidence == 0.0
    assert out.citations == []


def test_answer_with_chunks_returns_positive_confidence():
    chunks = [
        RetrievalResult(
            chunk_id="c1", document_id="d1",
            snippet_redacted="Pilot is 499 SAR for 7 days",
            score=0.8, source_type=SourceType.INTERNAL_DOC,
        ),
        RetrievalResult(
            chunk_id="c2", document_id="d1",
            snippet_redacted="No live send by default",
            score=0.6, source_type=SourceType.INTERNAL_DOC,
        ),
    ]
    out = answer(AnswerRequest(query="how much pilot cost", retrieved_chunks=chunks))
    assert out.insufficient_evidence is False
    assert out.confidence > 0.0
    assert "d1:c1" in out.citations
    assert "d1:c2" in out.citations
    assert "499" in out.answer_en


def test_extract_citations_dedupes():
    chunks = [
        RetrievalResult(chunk_id="c1", document_id="d1", source_type=SourceType.INTERNAL_DOC),
        RetrievalResult(chunk_id="c1", document_id="d1", source_type=SourceType.INTERNAL_DOC),
    ]
    assert extract_citations(chunks) == ["d1:c1"]


def test_evaluate_answer_faithfulness_one_when_citations_present():
    chunks = [
        RetrievalResult(
            chunk_id="c1", document_id="d1",
            snippet_redacted="pricing details here",
            score=0.9, source_type=SourceType.INTERNAL_DOC,
        ),
    ]
    a = answer(AnswerRequest(query="pricing", retrieved_chunks=chunks))
    result = evaluate_answer(a, chunks)
    assert result.faithfulness_score == 1.0
    assert result.hallucination_detected is False


def test_evaluate_detects_fabricated_citation():
    chunks = [
        RetrievalResult(
            chunk_id="c1", document_id="d1",
            snippet_redacted="real chunk", score=0.5,
            source_type=SourceType.INTERNAL_DOC,
        ),
    ]
    forged = Answer(
        answer_ar="ج",
        answer_en="answer without any citation tokens in body",
        citations=["dFAKE:cFAKE"],
        confidence=0.5,
        insufficient_evidence=False,
    )
    res = evaluate_answer(forged, chunks)
    assert res.faithfulness_score < 1.0
    assert res.hallucination_detected is True


def test_validate_manifest_accepts_dict():
    raw = {
        "id": "doc_1",
        "customer_handle": "ACME-SAUDI",
        "source_type": SourceType.INTERNAL_DOC.value,
        "title": "Pricing",
        "language": "ar",
        "chunk_count": 4,
    }
    m = validate_manifest(raw)
    assert isinstance(m, DocumentManifest)
    assert m.chunk_count == 4


def test_route_search_returns_keyword_match_for_internal_only():
    req = RetrievalRequest(
        query="pricing", allowed_sources=[SourceType.INTERNAL_DOC],
    )
    decision = route_search(req)
    assert decision["backend"] == "keyword_match"


def test_route_search_falls_back_to_pending_for_mixed():
    req = RetrievalRequest(
        query="pricing",
        allowed_sources=[
            SourceType.INTERNAL_DOC,
            SourceType.OFFICIAL_PUBLIC_SITE,
        ],
    )
    decision = route_search(req)
    assert decision["backend"] == "vector_db_pending"


def test_status_endpoint_advertises_no_default_scraping(client: TestClient):
    resp = client.get("/api/v1/knowledge-v10/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "knowledge_v10"
    assert body["guardrails"]["no_default_scraping"] is True
    assert body["guardrails"]["no_pii_ingestion"] is True
    assert body["guardrails"]["no_external_http"] is True


def test_search_endpoint_returns_empty_list(client: TestClient):
    resp = client.post(
        "/api/v1/knowledge-v10/search",
        json={"query": "anything", "allowed_sources": []},
    )
    assert resp.status_code == 200
    assert resp.json() == []


def test_answer_endpoint_with_no_chunks_returns_insufficient(client: TestClient):
    resp = client.post(
        "/api/v1/knowledge-v10/answer",
        json={"query": "pricing question", "retrieved_chunks": [], "language": "both"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["insufficient_evidence"] is True
    assert body["confidence"] == 0.0


def test_sources_endpoint_lists_all_nine(client: TestClient):
    resp = client.get("/api/v1/knowledge-v10/sources")
    assert resp.status_code == 200
    assert len(resp.json()["sources"]) == 9
