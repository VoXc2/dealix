"""Company Brain — TF-IDF retrieval, citations, and RBAC permissions."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.company_brain_mvp.memory import (
    ingest_chunk,
    query_workspace,
    reset_workspace,
    workspace_stats,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clean():
    for ws in ("rag_ws", "rag_ws2"):
        reset_workspace(ws)
    yield
    for ws in ("rag_ws", "rag_ws2"):
        reset_workspace(ws)


def test_no_source_no_answer() -> None:
    out = query_workspace(workspace_id="rag_ws", question="what is pricing?")
    assert out["answer_mode"] == "insufficient_evidence"
    assert out["citations"] == []


def test_query_returns_evidence_with_citations() -> None:
    ingest_chunk(
        workspace_id="rag_ws",
        text="Our refund policy gives a full refund within 14 days.",
        source_id="policy_refund",
        title="Refund Policy",
    )
    ingest_chunk(
        workspace_id="rag_ws",
        text="The office is open Sunday to Thursday, 9am to 5pm.",
        source_id="doc_hours",
    )
    out = query_workspace(workspace_id="rag_ws", question="refund within how many days")
    assert out["answer_mode"] == "evidence_backed"
    assert out["citations"][0]["source_id"] == "policy_refund"
    assert out["confidence"] > 0
    assert "relevance" in out["citations"][0]


def test_tfidf_ranks_most_relevant_chunk_first() -> None:
    ingest_chunk(
        workspace_id="rag_ws",
        text="Annual leave is 30 days per year for full-time staff.",
        source_id="hr_leave",
    )
    ingest_chunk(
        workspace_id="rag_ws",
        text="Parking is available in the basement for all staff.",
        source_id="facilities",
    )
    out = query_workspace(workspace_id="rag_ws", question="how many annual leave days")
    assert out["citations"][0]["source_id"] == "hr_leave"


def test_rbac_restricted_chunk_hidden_from_wrong_role() -> None:
    ingest_chunk(
        workspace_id="rag_ws",
        text="Executive compensation bands are confidential.",
        source_id="exec_comp",
        allowed_roles=("executive",),
    )
    # A staff-role viewer must not retrieve the executive-only chunk.
    staff = query_workspace(
        workspace_id="rag_ws", question="executive compensation bands",
        viewer_role="staff",
    )
    assert staff["answer_mode"] == "insufficient_evidence"
    # The executive role can.
    exec_view = query_workspace(
        workspace_id="rag_ws", question="executive compensation bands",
        viewer_role="executive",
    )
    assert exec_view["answer_mode"] == "evidence_backed"
    assert exec_view["citations"][0]["source_id"] == "exec_comp"


def test_public_chunk_visible_to_all_roles() -> None:
    ingest_chunk(
        workspace_id="rag_ws",
        text="The company mission is to serve Saudi businesses.",
        source_id="mission",
    )
    for role in ("", "staff", "executive"):
        out = query_workspace(
            workspace_id="rag_ws", question="company mission", viewer_role=role
        )
        assert out["answer_mode"] == "evidence_backed"


def test_workspace_isolation() -> None:
    ingest_chunk(
        workspace_id="rag_ws", text="Secret A belongs to workspace one.",
        source_id="a",
    )
    out = query_workspace(workspace_id="rag_ws2", question="secret")
    assert out["answer_mode"] == "insufficient_evidence"


def test_workspace_stats() -> None:
    ingest_chunk(workspace_id="rag_ws", text="doc one", source_id="s1")
    ingest_chunk(
        workspace_id="rag_ws", text="doc two", source_id="s2",
        allowed_roles=("executive",),
    )
    stats = workspace_stats("rag_ws")
    assert stats["chunk_count"] == 2
    assert stats["source_count"] == 2
    assert stats["restricted_chunk_count"] == 1


# ── API surface ──────────────────────────────────────────────────────


def test_company_brain_api_ingest_query_rbac() -> None:
    ingest = client.post(
        "/api/v1/company-brain/ingest",
        json={
            "workspace_id": "rag_ws",
            "text": "The board approval threshold is 100,000 SAR.",
            "source_id": "board_policy",
            "allowed_roles": ["executive"],
        },
    )
    assert ingest.status_code == 200, ingest.text

    staff_q = client.post(
        "/api/v1/company-brain/query",
        json={
            "workspace_id": "rag_ws",
            "question": "board approval threshold",
            "viewer_role": "staff",
        },
    )
    assert staff_q.json()["answer_mode"] == "insufficient_evidence"

    exec_q = client.post(
        "/api/v1/company-brain/query",
        json={
            "workspace_id": "rag_ws",
            "question": "board approval threshold",
            "viewer_role": "executive",
        },
    )
    assert exec_q.json()["answer_mode"] == "evidence_backed"

    stats = client.get("/api/v1/company-brain/rag_ws/stats")
    assert stats.status_code == 200
    assert stats.json()["chunk_count"] == 1
