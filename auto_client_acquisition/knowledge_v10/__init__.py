"""Knowledge v10 — RAG layer.

Schemas + policies + a real cosine-search retrieval backend behind one
``retrieve()`` interface. The store backend (JSONL or pgvector) is selected
by DEALIX_KNOWLEDGE_BACKEND. No LLM, no external HTTP, no scraping, no PII
ingestion (snippets are PII-redacted on the way out).

Public API:

    from auto_client_acquisition.knowledge_v10 import (
        Answer, AnswerRequest, DocumentManifest, KnowledgeChunk,
        RAGEvalResult, RetrievalRequest, RetrievalResult, SourceType,
        answer, chunk_text, evaluate_answer, extract_citations, get_store,
        ingest_text, is_source_allowed, retrieve, route_search,
        validate_manifest,
    )
"""
from auto_client_acquisition.knowledge_v10.answer_contract import answer
from auto_client_acquisition.knowledge_v10.citation_policy import extract_citations
from auto_client_acquisition.knowledge_v10.document_manifest import validate_manifest
from auto_client_acquisition.knowledge_v10.eval_contract import evaluate_answer
from auto_client_acquisition.knowledge_v10.ingestion import chunk_text, ingest_text
from auto_client_acquisition.knowledge_v10.retrieval_contract import retrieve
from auto_client_acquisition.knowledge_v10.schemas import (
    Answer,
    AnswerRequest,
    DocumentManifest,
    RAGEvalResult,
    RetrievalRequest,
    RetrievalResult,
    SourceType,
)
from auto_client_acquisition.knowledge_v10.search_router import route_search
from auto_client_acquisition.knowledge_v10.source_policy import is_source_allowed
from auto_client_acquisition.knowledge_v10.store import KnowledgeChunk, get_store

__all__ = [
    "Answer",
    "AnswerRequest",
    "DocumentManifest",
    "KnowledgeChunk",
    "RAGEvalResult",
    "RetrievalRequest",
    "RetrievalResult",
    "SourceType",
    "answer",
    "chunk_text",
    "evaluate_answer",
    "extract_citations",
    "get_store",
    "ingest_text",
    "is_source_allowed",
    "retrieve",
    "route_search",
    "validate_manifest",
]
