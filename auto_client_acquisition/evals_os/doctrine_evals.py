"""Doctrine evals — the 11 non-negotiables as runnable eval checks.

The doctrine is already enforced by pytest guards. These evals run the
same invariants *programmatically at runtime* so they surface on the
executive dashboard, not only in CI.
"""
from __future__ import annotations

from auto_client_acquisition.agent_loop_os.loop import AgentLoop, PlanDecision
from auto_client_acquisition.agent_loop_os.loop_budget import LoopBudget
from auto_client_acquisition.agent_loop_os.tool_registry import default_tool_registry
from auto_client_acquisition.agent_loop_os.trace import TERMINATION_REASONS
from auto_client_acquisition.evals_os.schemas import EvalResult
from auto_client_acquisition.knowledge_os.index import InMemoryKnowledgeIndex
from auto_client_acquisition.knowledge_os.ingest import ingest_document
from auto_client_acquisition.knowledge_os.knowledge_eval import eval_no_source_policy
from auto_client_acquisition.knowledge_os.retriever import retrieve
from auto_client_acquisition.knowledge_os.schemas import IngestRequest, RetrievalRequest, SourceType
from auto_client_acquisition.knowledge_os.synthesizer import answer_query

__all__ = ["run_doctrine_evals"]

_SUITE = "doctrine"


def _result(case: str, passed: bool, detail: str = "") -> EvalResult:
    return EvalResult(
        case_id=f"doctrine::{case}",
        suite_id=_SUITE,
        passed=passed,
        score=1.0 if passed else 0.0,
        failures=() if passed else (detail or case,),
        metrics={},
    )


def _check_no_source_no_answer() -> EvalResult:
    index = InMemoryKnowledgeIndex()
    answer = answer_query(
        RetrievalRequest(query="anything at all", customer_handle="doctrine_eval"),
        index=index,
    )
    ok = eval_no_source_policy() and answer.insufficient_evidence and not answer.citations
    return _result("no_source_no_answer", ok, "empty index produced a non-abstaining answer")


def _check_no_scraping() -> EvalResult:
    index = InMemoryKnowledgeIndex()
    try:
        ingest_document(
            IngestRequest(
                customer_handle="doctrine_eval",
                source_type=SourceType.BLOCKED_SCRAPING_SOURCE.value,
                title="x",
                text="some scraped text",
            ),
            index=index,
        )
        return _result("no_scraping", False, "blocked scraping source was ingested")
    except ValueError:
        return _result("no_scraping", True)


def _check_no_pii_in_logs() -> EvalResult:
    index = InMemoryKnowledgeIndex()
    ingest_document(
        IngestRequest(
            customer_handle="doctrine_eval_pii",
            source_type=SourceType.MANUALLY_ENTERED_NOTE.value,
            title="contact",
            text="Reach the owner at owner@example.com or 0501234567 about the deal.",
        ),
        index=index,
    )
    results = retrieve(
        RetrievalRequest(query="reach owner deal contact", customer_handle="doctrine_eval_pii"),
        index=index,
    )
    blob = " ".join(r.snippet_redacted for r in results)
    ok = "owner@example.com" not in blob and "0501234567" not in blob
    return _result("no_pii_in_logs", ok, "raw PII survived ingestion redaction")


def _check_no_unbounded_agents() -> EvalResult:
    # A planner that never finalizes — proves the budget alone halts the loop.
    def never_finalize(goal, customer_id, context, steps) -> PlanDecision:
        return PlanDecision(
            thought="probe",
            tool_name="knowledge.retrieve",
            tool_args={"customer_id": customer_id, "query": goal},
        )

    loop = AgentLoop(
        registry=default_tool_registry(InMemoryKnowledgeIndex()),
        budget=LoopBudget(max_iterations=3, max_tool_calls=3),
        planner=never_finalize,
    )
    trace = loop.run(goal="probe the bound", customer_id="doctrine_eval")
    ok = trace.iteration_count <= 3 and trace.tool_call_count <= 3
    return _result(
        "no_unbounded_agents",
        ok,
        f"loop ran {trace.iteration_count} iterations / {trace.tool_call_count} tool calls",
    )


def _check_no_silent_failures() -> EvalResult:
    loop = AgentLoop(registry=default_tool_registry(InMemoryKnowledgeIndex()))
    trace = loop.run(goal="any goal at all", customer_id="doctrine_eval")
    ok = trace.terminated_reason in TERMINATION_REASONS
    return _result("no_silent_failures", ok, "loop terminated without a recorded reason")


def _check_no_unaudited_changes() -> EvalResult:
    loop = AgentLoop(registry=default_tool_registry(InMemoryKnowledgeIndex()))
    trace = loop.run(goal="any goal at all", customer_id="doctrine_eval")
    ok = bool(trace.loop_id) and bool(trace.steps) and trace.terminated_reason == "goal_met"
    return _result("no_unaudited_changes", ok, "loop produced no audit trail")


def _check_no_live_send() -> EvalResult:
    unguarded = default_tool_registry(InMemoryKnowledgeIndex()).unguarded_mutating_tools()
    ok = not unguarded
    return _result(
        "no_live_send", ok, f"unguarded mutating tools present: {list(unguarded)}"
    )


def run_doctrine_evals(customer_id: str) -> list[EvalResult]:
    """Run every in-process doctrine check. ``customer_id`` is informational."""
    return [
        _check_no_source_no_answer(),
        _check_no_scraping(),
        _check_no_pii_in_logs(),
        _check_no_unbounded_agents(),
        _check_no_silent_failures(),
        _check_no_unaudited_changes(),
        _check_no_live_send(),
    ]
