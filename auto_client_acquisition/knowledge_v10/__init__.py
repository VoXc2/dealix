"""Knowledge v10 — Qdrant/Haystack-inspired RAG contract.

Pure contract layer: schemas + policies + a stub retrieval interface.
The real Qdrant adapter ships in §S6. No LLM, no external HTTP,
no scraping, no PII ingestion.

Public API:

    from auto_client_acquisition.knowledge_v10 import (
        Answer, AnswerRequest, DocumentManifest,
        RAGEvalResult, RetrievalRequest, RetrievalResult,
        SourceType, answer, evaluate_answer, extract_citations,
        is_source_allowed, retrieve, route_search, validate_manifest,
    )
"""
from auto_client_acquisition.knowledge_v10.answer_contract import answer
from auto_client_acquisition.knowledge_v10.citation_policy import extract_citations
from auto_client_acquisition.knowledge_v10.document_manifest import validate_manifest
from auto_client_acquisition.knowledge_v10.eval_contract import evaluate_answer
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

__all__ = [
    "Answer",
    "AnswerRequest",
    "DocumentManifest",
    "RAGEvalResult",
    "RetrievalRequest",
    "RetrievalResult",
    "SourceType",
    "answer",
    "evaluate_answer",
    "extract_citations",
    "is_source_allowed",
    "retrieve",
    "route_search",
    "validate_manifest",
]
