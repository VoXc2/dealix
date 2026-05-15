"""Knowledge OS — permission-aware grounded retrieval."""

from __future__ import annotations

import pytest

from auto_client_acquisition.knowledge_os import (
    RetrievalSource,
    filter_by_rbac,
    grounded_answer,
)


def _source(sid: str, min_role: str, tenant: str = "t1") -> RetrievalSource:
    return RetrievalSource(
        source_id=sid,
        excerpt=f"excerpt for {sid}",
        min_role=min_role,
        tenant_id=tenant,
    )


def test_rbac_filter_drops_higher_role_sources() -> None:
    sources = [_source("s1", "viewer"), _source("s2", "tenant_admin")]
    kept = filter_by_rbac(sources, role="sales_rep", tenant_id="t1")
    assert {s.source_id for s in kept} == {"s1"}


def test_rbac_filter_drops_cross_tenant_sources() -> None:
    sources = [_source("s1", "viewer", tenant="t1"), _source("s2", "viewer", tenant="t2")]
    kept = filter_by_rbac(sources, role="tenant_admin", tenant_id="t1")
    assert {s.source_id for s in kept} == {"s1"}


def test_rbac_filter_unknown_role_raises() -> None:
    with pytest.raises(ValueError):
        filter_by_rbac([], role="not_a_role", tenant_id="t1")


def test_grounded_answer_returns_citations_for_permitted_sources() -> None:
    sources = [_source("s1", "viewer"), _source("s2", "viewer")]
    result = grounded_answer(
        "what is the plan?", sources=sources, role="sales_rep", tenant_id="t1"
    )
    assert result["insufficient_evidence"] is False
    assert len(result["citations"]) == 2
    assert result["filtered_out"] == 0


def test_grounded_answer_insufficient_when_all_filtered_out() -> None:
    sources = [_source("s1", "super_admin"), _source("s2", "tenant_admin")]
    result = grounded_answer(
        "what is the plan?", sources=sources, role="viewer", tenant_id="t1"
    )
    assert result["insufficient_evidence"] is True
    assert result["citations"] == []
    assert result["filtered_out"] == 2


def test_grounded_answer_requires_question() -> None:
    with pytest.raises(ValueError):
        grounded_answer("", sources=[], role="viewer", tenant_id="t1")
