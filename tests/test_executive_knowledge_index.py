"""Executive knowledge index."""

from __future__ import annotations

from dealix.execution.executive_knowledge_index import build_docs_index, search_docs


def test_build_docs_index_non_empty() -> None:
    rows = build_docs_index()
    assert len(rows) > 10


def test_search_docs_transformation() -> None:
    hits = search_docs("transformation")
    assert hits
