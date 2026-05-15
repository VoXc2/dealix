"""Knowledge OS — ingestion, permission-aware retrieval, grounded answers.

The engine: source-gated ingestion → deterministic chunking → PII
redaction → tenant-scoped index → grounded, cited synthesis. Every step
records to an append-only knowledge ledger.
"""

from auto_client_acquisition.knowledge_os.answer_with_citations import answer_with_citations
from auto_client_acquisition.knowledge_os.index import (
    InMemoryKnowledgeIndex,
    KnowledgeIndex,
    clear_default_index_for_test,
    get_default_index,
)
from auto_client_acquisition.knowledge_os.ingest import ingest_document
from auto_client_acquisition.knowledge_os.knowledge_eval import (
    eval_no_source_policy,
    eval_retrieval_grounded,
)
from auto_client_acquisition.knowledge_os.knowledge_ledger import (
    clear_for_test,
    emit_knowledge_event,
    list_knowledge_events,
)
from auto_client_acquisition.knowledge_os.retriever import retrieve
from auto_client_acquisition.knowledge_os.schemas import (
    Answer,
    DocumentManifest,
    IngestRequest,
    KnowledgeChunk,
    KnowledgeEvent,
    RetrievalRequest,
    RetrievalResult,
    SourceType,
)
from auto_client_acquisition.knowledge_os.synthesizer import answer_query, answer_query_llm

__all__ = [
    "Answer",
    "DocumentManifest",
    "InMemoryKnowledgeIndex",
    "IngestRequest",
    "KnowledgeChunk",
    "KnowledgeEvent",
    "KnowledgeIndex",
    "RetrievalRequest",
    "RetrievalResult",
    "SourceType",
    "answer_query",
    "answer_query_llm",
    "answer_with_citations",
    "clear_default_index_for_test",
    "clear_for_test",
    "emit_knowledge_event",
    "eval_no_source_policy",
    "eval_retrieval_grounded",
    "get_default_index",
    "ingest_document",
    "list_knowledge_events",
    "retrieve",
]
