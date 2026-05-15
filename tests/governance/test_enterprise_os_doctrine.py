"""Doctrine — Enterprise AI OS spine (Knowledge, Agent Runtime, Evals, ROI).

Every new router must emit a ``governance_decision``, strip PII, abstain
without evidence, keep agents bounded, and never present unverified ROI
without evidence.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.knowledge_os.index import clear_default_index_for_test
from auto_client_acquisition.secure_agent_runtime_os.kill_switch import (
    reset_kill_switch_for_tests,
)


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_KNOWLEDGE_LEDGER_PATH", str(tmp_path / "knowledge.jsonl"))
    monkeypatch.setenv("DEALIX_AGENT_LOOP_LEDGER_PATH", str(tmp_path / "loop.jsonl"))
    monkeypatch.setenv("DEALIX_EVAL_LEDGER_PATH", str(tmp_path / "eval.jsonl"))
    monkeypatch.setenv("DEALIX_ROI_LEDGER_PATH", str(tmp_path / "roi.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    clear_default_index_for_test()
    reset_kill_switch_for_tests()
    yield
    clear_default_index_for_test()
    reset_kill_switch_for_tests()


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_knowledge_ingest_and_query_emit_governance_decision(client: TestClient) -> None:
    ingest = client.post(
        "/api/v1/knowledge/documents",
        json={
            "customer_id": "doctrine_kos",
            "source_type": "manually_entered_note",
            "title": "pricing",
            "text": "Dealix retainer pricing is fifteen thousand SAR per month.",
        },
    )
    assert ingest.status_code == 200, ingest.text
    assert ingest.json()["governance_decision"]

    query = client.post(
        "/api/v1/knowledge/query",
        json={"customer_id": "doctrine_kos", "query": "retainer pricing monthly"},
    )
    assert query.status_code == 200, query.text
    body = query.json()
    assert body["governance_decision"]
    assert body["insufficient_evidence"] is False
    assert body["citations"]


def test_knowledge_query_without_evidence_abstains(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/knowledge/query",
        json={"customer_id": "doctrine_empty_tenant", "query": "totally unknown subject"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["insufficient_evidence"] is True
    assert body["citations"] == []


def test_knowledge_query_strips_pii(client: TestClient) -> None:
    client.post(
        "/api/v1/knowledge/documents",
        json={
            "customer_id": "doctrine_pii",
            "source_type": "manually_entered_note",
            "title": "contact",
            "text": "Reach the owner at owner@example.com or 0501234567 about pricing.",
        },
    )
    resp = client.post(
        "/api/v1/knowledge/query",
        json={"customer_id": "doctrine_pii", "query": "reach owner pricing contact"},
    )
    assert resp.status_code == 200, resp.text
    assert "owner@example.com" not in repr(resp.json())
    assert "0501234567" not in repr(resp.json())


def test_knowledge_rejects_blocked_source(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/knowledge/documents",
        json={
            "customer_id": "doctrine_block",
            "source_type": "blocked_scraping_source",
            "title": "x",
            "text": "scraped content",
        },
    )
    assert resp.status_code == 422, resp.text


def test_agent_runtime_run_is_bounded(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/agent-runtime/run",
        json={"customer_id": "doctrine_agent", "goal": "summarize something useful"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["iteration_count"] <= 8
    assert body["terminated_reason"]
    assert body["governance_decision"]


def test_evals_run_emits_pass_rate_and_governance(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/evals/run",
        json={"customer_id": "doctrine_evals", "suite_id": "doctrine"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "pass_rate" in body
    assert body["governance_decision"]


def test_roi_snapshot_verified_lines_have_evidence(client: TestClient) -> None:
    resp = client.get("/api/v1/roi/doctrine_roi/snapshot")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["governance_decision"]
    cost_lines = [ln for ln in body["lines"] if ln["label"] == "llm_cost_sar"]
    assert cost_lines, "ROI snapshot must always show a cost line (no_hidden_pricing)"
    for line in body["lines"]:
        if line["confidence"] == "verified":
            assert line["evidence_ref"].strip(), (
                f"verified ROI line {line['label']} missing evidence (no_fake_proof)"
            )


def test_roi_executive_brief_states_limitations(client: TestClient) -> None:
    resp = client.get("/api/v1/roi/doctrine_roi/executive-brief?format=markdown")
    assert resp.status_code == 200, resp.text
    assert "Estimated value is not Verified value" in resp.text
