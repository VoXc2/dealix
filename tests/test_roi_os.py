"""ROI OS — executive intelligence + ROI snapshots."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_loop_os.loop import AgentLoop
from auto_client_acquisition.agent_loop_os.tool_registry import default_tool_registry
from auto_client_acquisition.evals_os.runner import run_suite
from auto_client_acquisition.knowledge_os.index import InMemoryKnowledgeIndex
from auto_client_acquisition.knowledge_os.ingest import ingest_document
from auto_client_acquisition.knowledge_os.schemas import (
    IngestRequest,
    RetrievalRequest,
    SourceType,
)
from auto_client_acquisition.knowledge_os.synthesizer import answer_query
from auto_client_acquisition.roi_os.cost_model import estimated_value_from_activity
from auto_client_acquisition.roi_os.executive_brief import build_brief
from auto_client_acquisition.roi_os.roi_aggregator import compute_roi
from auto_client_acquisition.roi_os.schemas import roi_snapshot_valid
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
    reset_kill_switch_for_tests()
    yield
    reset_kill_switch_for_tests()


def _seed_activity(customer_id: str = "acme") -> None:
    index = InMemoryKnowledgeIndex()
    ingest_document(
        IngestRequest(
            customer_handle=customer_id,
            source_type=SourceType.MANUALLY_ENTERED_NOTE.value,
            title="ops",
            text="Dealix managed operations covers lead handling and weekly reporting.",
        ),
        index=index,
    )
    answer_query(
        RetrievalRequest(query="managed operations reporting", customer_handle=customer_id),
        index=index,
    )
    AgentLoop(registry=default_tool_registry(index)).run(
        goal="summarize managed operations reporting",
        customer_id=customer_id,
    )
    run_suite("knowledge_os", customer_id=customer_id)


def test_compute_roi_returns_a_valid_snapshot() -> None:
    _seed_activity("acme")
    snapshot = compute_roi("acme", window_days=30)
    assert snapshot.customer_id == "acme"
    assert snapshot.agent_runs >= 1
    assert snapshot.grounded_answers >= 1
    assert roi_snapshot_valid(snapshot) is True


def test_verified_roi_lines_carry_evidence() -> None:
    _seed_activity("acme")
    snapshot = compute_roi("acme")
    verified = [line for line in snapshot.lines if line.confidence == "verified"]
    assert verified, "expected at least one verified ROI line"
    for line in verified:
        assert line.evidence_ref.strip(), f"verified line {line.label} missing evidence"


def test_roi_snapshot_always_shows_a_cost_line() -> None:
    _seed_activity("acme")
    snapshot = compute_roi("acme")
    labels = {line.label for line in snapshot.lines}
    assert "llm_cost_sar" in labels  # no_hidden_pricing


def test_estimated_value_is_labelled_estimated() -> None:
    _seed_activity("acme")
    snapshot = compute_roi("acme")
    estimated = [line for line in snapshot.lines if line.confidence == "estimated"]
    assert estimated, "estimated operational value must be present and labelled"


def test_executive_brief_has_limitations_disclaimer() -> None:
    _seed_activity("acme")
    brief = build_brief("acme", window_days=30)
    assert "## Limitations" in brief.markdown
    assert "Estimated value is not Verified value" in brief.markdown
    assert brief.headline


def test_cost_model_estimate_is_a_tuple() -> None:
    hours, value = estimated_value_from_activity(grounded_answers=3, successful_agent_runs=2)
    assert hours > 0
    assert value > 0


def test_compute_roi_rejects_blank_customer() -> None:
    with pytest.raises(ValueError):
        compute_roi("   ")
