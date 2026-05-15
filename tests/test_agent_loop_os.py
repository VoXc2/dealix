"""Agent Runtime — bounded, audited, kill-switchable agentic loop."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_loop_os.agent_loop_ledger import list_loops
from auto_client_acquisition.agent_loop_os.loop import AgentLoop, PlanDecision
from auto_client_acquisition.agent_loop_os.loop_budget import LoopBudget
from auto_client_acquisition.agent_loop_os.orchestrator_bridge import agentic_resolve_executor
from auto_client_acquisition.agent_loop_os.tool_registry import default_tool_registry
from auto_client_acquisition.knowledge_os.index import InMemoryKnowledgeIndex
from auto_client_acquisition.knowledge_os.ingest import ingest_document
from auto_client_acquisition.knowledge_os.schemas import IngestRequest, SourceType
from auto_client_acquisition.orchestrator.queue import AgentTask
from auto_client_acquisition.secure_agent_runtime_os.kill_switch import (
    activate_kill_switch,
    reset_kill_switch_for_tests,
)


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_LOOP_LEDGER_PATH", str(tmp_path / "loop.jsonl"))
    monkeypatch.setenv("DEALIX_KNOWLEDGE_LEDGER_PATH", str(tmp_path / "knowledge.jsonl"))
    reset_kill_switch_for_tests()
    yield
    reset_kill_switch_for_tests()


def _index_with_doc(customer_id: str = "acme") -> InMemoryKnowledgeIndex:
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
    return index


def test_loop_is_bounded_by_iteration_budget() -> None:
    def never_finalize(goal, customer_id, context, steps) -> PlanDecision:
        return PlanDecision(
            thought="probe",
            tool_name="knowledge.retrieve",
            tool_args={"customer_id": customer_id, "query": goal},
        )

    loop = AgentLoop(
        registry=default_tool_registry(_index_with_doc()),
        budget=LoopBudget(max_iterations=3, max_tool_calls=10),
        planner=never_finalize,
    )
    trace = loop.run(goal="probe the iteration bound", customer_id="acme")
    assert trace.iteration_count <= 3
    assert trace.terminated_reason == "max_iterations"


def test_loop_is_bounded_by_tool_call_budget() -> None:
    def never_finalize(goal, customer_id, context, steps) -> PlanDecision:
        return PlanDecision(
            thought="probe",
            tool_name="knowledge.retrieve",
            tool_args={"customer_id": customer_id, "query": goal},
        )

    loop = AgentLoop(
        registry=default_tool_registry(_index_with_doc()),
        budget=LoopBudget(max_iterations=20, max_tool_calls=2),
        planner=never_finalize,
    )
    trace = loop.run(goal="probe the tool-call bound", customer_id="acme")
    assert trace.tool_call_count <= 2
    assert trace.terminated_reason == "budget_exhausted"


def test_loop_produces_audit_trace_and_ledger_entry() -> None:
    loop = AgentLoop(registry=default_tool_registry(_index_with_doc()))
    trace = loop.run(goal="summarize managed operations", customer_id="acme")
    assert trace.loop_id
    assert trace.steps, "loop must record at least one audited step"
    assert trace.terminated_reason in ("goal_met", "max_iterations")

    ledgered = list_loops(customer_id="acme")
    assert any(t["loop_id"] == trace.loop_id for t in ledgered)


def test_kill_switch_halts_the_loop() -> None:
    activate_kill_switch()
    loop = AgentLoop(registry=default_tool_registry(_index_with_doc()))
    trace = loop.run(goal="this should not run", customer_id="acme")
    assert trace.terminated_reason == "kill_switch"


def test_deterministic_planner_grounds_the_answer() -> None:
    loop = AgentLoop(registry=default_tool_registry(_index_with_doc()))
    trace = loop.run(goal="managed operations lead handling reporting", customer_id="acme")
    assert trace.terminated_reason == "goal_met"
    assert trace.insufficient_evidence is False
    assert trace.final_answer.strip()


def test_loop_abstains_when_no_evidence() -> None:
    loop = AgentLoop(registry=default_tool_registry(InMemoryKnowledgeIndex()))
    trace = loop.run(goal="a goal with no indexed knowledge", customer_id="acme")
    assert trace.terminated_reason == "goal_met"
    assert trace.insufficient_evidence is True


def test_tool_registry_has_no_unguarded_mutating_tools() -> None:
    registry = default_tool_registry(InMemoryKnowledgeIndex())
    assert registry.unguarded_mutating_tools() == ()


def test_orchestrator_bridge_runs_a_loop() -> None:
    task = AgentTask(
        task_id="tsk_test",
        customer_id="acme",
        agent_id="agent_loop_os",
        action_type="agentic_resolve",
        payload={"goal": "summarize anything", "inputs": {}},
    )
    result = agentic_resolve_executor(task)
    assert result["customer_id"] == "acme"
    assert result["terminated_reason"] in ("goal_met", "max_iterations")
