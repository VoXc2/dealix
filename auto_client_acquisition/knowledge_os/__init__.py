"""Knowledge OS — citation-safe answers (facade over existing modules)."""

from auto_client_acquisition.knowledge_os.answer_with_citations import answer_with_citations
from auto_client_acquisition.knowledge_os.grounded_retrieval import (
    RBAC_ROLES,
    RetrievalSource,
    filter_by_rbac,
    grounded_answer,
)
from auto_client_acquisition.knowledge_os.knowledge_eval import eval_no_source_policy

__all__ = [
    "RBAC_ROLES",
    "RetrievalSource",
    "answer_with_citations",
    "eval_no_source_policy",
    "filter_by_rbac",
    "grounded_answer",
]
