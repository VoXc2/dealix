"""Evals OS — RAG, agent, and doctrine quality measurement."""
from __future__ import annotations

import pytest

from auto_client_acquisition.evals_os.agent_evals import eval_agent_loop
from auto_client_acquisition.evals_os.doctrine_evals import run_doctrine_evals
from auto_client_acquisition.evals_os.eval_ledger import list_eval_runs
from auto_client_acquisition.evals_os.rag_evals import eval_rag
from auto_client_acquisition.evals_os.runner import run_suite
from auto_client_acquisition.knowledge_os.schemas import Answer
from auto_client_acquisition.agent_loop_os.loop import AgentLoop
from auto_client_acquisition.agent_loop_os.tool_registry import default_tool_registry
from auto_client_acquisition.knowledge_os.index import InMemoryKnowledgeIndex
from auto_client_acquisition.secure_agent_runtime_os.kill_switch import (
    reset_kill_switch_for_tests,
)


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_KNOWLEDGE_LEDGER_PATH", str(tmp_path / "knowledge.jsonl"))
    monkeypatch.setenv("DEALIX_AGENT_LOOP_LEDGER_PATH", str(tmp_path / "loop.jsonl"))
    monkeypatch.setenv("DEALIX_EVAL_LEDGER_PATH", str(tmp_path / "eval.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    reset_kill_switch_for_tests()
    yield
    reset_kill_switch_for_tests()


def test_eval_rag_flags_hallucinated_citation() -> None:
    answer = Answer(
        answer_ar="some answer",
        citations=["chunk_not_retrieved"],
        confidence=0.9,
        insufficient_evidence=False,
    )
    result = eval_rag(answer, retrieved_chunk_ids=["chunk_a", "chunk_b"])
    assert result.hallucination_detected is True


def test_eval_rag_passes_grounded_answer() -> None:
    answer = Answer(
        answer_ar="grounded answer",
        citations=["chunk_a"],
        confidence=0.9,
        insufficient_evidence=False,
    )
    result = eval_rag(answer, retrieved_chunk_ids=["chunk_a", "chunk_b"])
    assert result.hallucination_detected is False
    assert result.faithfulness_score == 1.0


def test_eval_rag_treats_abstention_as_faithful() -> None:
    answer = Answer(insufficient_evidence=True)
    result = eval_rag(answer, retrieved_chunk_ids=[])
    assert result.hallucination_detected is False
    assert result.faithfulness_score == 1.0


def test_eval_agent_loop_scores_a_bounded_run() -> None:
    loop = AgentLoop(registry=default_tool_registry(InMemoryKnowledgeIndex()))
    trace = loop.run(goal="a goal with no evidence", customer_id="acme")
    result = eval_agent_loop(trace)
    assert result.passed is True


def test_run_suite_knowledge_os() -> None:
    summary = run_suite("knowledge_os", customer_id="acme")
    assert summary.total == 2
    assert summary.pass_rate == 1.0
    assert summary.regression_detected is False


def test_run_suite_agent_runtime() -> None:
    summary = run_suite("agent_runtime", customer_id="acme")
    assert summary.total == 1
    assert summary.passed == 1


def test_run_suite_doctrine_all_pass() -> None:
    summary = run_suite("doctrine", customer_id="acme")
    assert summary.total == 7
    assert summary.pass_rate == 1.0, [r.to_dict() for r in summary.results if not r.passed]


def test_run_suite_all_and_ledger() -> None:
    summary = run_suite("all", customer_id="acme")
    assert summary.total == 10
    assert summary.pass_rate == 1.0
    runs = list_eval_runs(customer_id="acme", suite_id="all")
    assert len(runs) == 1
    assert runs[-1]["run_id"] == summary.run_id


def test_run_suite_rejects_unknown_suite() -> None:
    with pytest.raises(ValueError):
        run_suite("does_not_exist", customer_id="acme")


def test_repeated_healthy_run_is_not_a_regression() -> None:
    run_suite("knowledge_os", customer_id="acme")
    second = run_suite("knowledge_os", customer_id="acme")
    assert second.regression_detected is False


def test_doctrine_evals_cover_all_checks() -> None:
    results = run_doctrine_evals("acme")
    names = {r.case_id for r in results}
    assert "doctrine::no_unbounded_agents" in names
    assert "doctrine::no_source_no_answer" in names
    assert "doctrine::no_live_send" in names
    assert all(r.passed for r in results)
