"""Eval suite runner.

``run_suite`` executes a suite, ledgers the result, emits an
``ai.eval_run`` event, and — if the pass rate dropped versus the previous
run of the same suite — emits ``ai.regression_detected`` plus a friction
event so the regression surfaces where operators look.

Suites (programmatic; ``evals/*.yaml`` packs are the data-driven upgrade):
  - ``knowledge_os``   — RAG grounding + honest abstention
  - ``agent_runtime``  — bounded, audited, grounded agent loop
  - ``doctrine``       — the 11 non-negotiables as runtime checks
  - ``all``            — every suite above
"""
from __future__ import annotations

from auto_client_acquisition.agent_loop_os.loop import AgentLoop
from auto_client_acquisition.agent_loop_os.tool_registry import default_tool_registry
from auto_client_acquisition.evals_os.agent_evals import eval_agent_loop
from auto_client_acquisition.evals_os.doctrine_evals import run_doctrine_evals
from auto_client_acquisition.evals_os.eval_ledger import emit_eval_run, last_run
from auto_client_acquisition.evals_os.rag_evals import eval_rag, rag_eval_to_result
from auto_client_acquisition.evals_os.schemas import EvalResult, EvalRunSummary
from auto_client_acquisition.knowledge_os.index import InMemoryKnowledgeIndex
from auto_client_acquisition.knowledge_os.ingest import ingest_document
from auto_client_acquisition.knowledge_os.retriever import retrieve
from auto_client_acquisition.knowledge_os.schemas import IngestRequest, RetrievalRequest, SourceType
from auto_client_acquisition.knowledge_os.synthesizer import answer_query
from auto_client_acquisition.revenue_memory.event_store import get_default_store
from auto_client_acquisition.revenue_memory.events import make_event

__all__ = ["run_suite", "SUITE_IDS"]

SUITE_IDS: tuple[str, ...] = ("knowledge_os", "agent_runtime", "doctrine", "all")

_NOTE = SourceType.MANUALLY_ENTERED_NOTE.value


def _run_knowledge_suite(customer_id: str) -> list[EvalResult]:
    index = InMemoryKnowledgeIndex()
    ingest_document(
        IngestRequest(
            customer_handle=customer_id,
            source_type=_NOTE,
            title="pricing",
            text="Dealix retainer pricing is fifteen thousand SAR per month for managed operations.",
        ),
        index=index,
    )
    # Case 1 — a query with grounding evidence.
    req = RetrievalRequest(query="retainer pricing monthly", customer_handle=customer_id)
    grounded = answer_query(req, index=index)
    grounded_rag = eval_rag(grounded, [r.chunk_id for r in retrieve(req, index=index)])
    case_1 = rag_eval_to_result("knowledge_os::grounded_query", "knowledge_os", grounded_rag)

    # Case 2 — a query with no evidence must abstain honestly.
    req2 = RetrievalRequest(query="completely unrelated subject matter", customer_handle=customer_id)
    abstain = answer_query(req2, index=index)
    abstain_rag = eval_rag(abstain, [r.chunk_id for r in retrieve(req2, index=index)])
    case_2 = rag_eval_to_result("knowledge_os::honest_abstention", "knowledge_os", abstain_rag)
    return [case_1, case_2]


def _run_agent_suite(customer_id: str) -> list[EvalResult]:
    index = InMemoryKnowledgeIndex()
    ingest_document(
        IngestRequest(
            customer_handle=customer_id,
            source_type=_NOTE,
            title="operations",
            text="Dealix managed operations covers lead handling, reporting, and weekly reviews.",
        ),
        index=index,
    )
    trace = AgentLoop(registry=default_tool_registry(index)).run(
        goal="summarize what managed operations covers",
        customer_id=customer_id,
    )
    return [eval_agent_loop(trace)]


def run_suite(suite_id: str, *, customer_id: str) -> EvalRunSummary:
    """Run ``suite_id`` for ``customer_id`` and ledger the outcome."""
    if suite_id not in SUITE_IDS:
        raise ValueError(f"unknown suite_id: {suite_id!r} (expected one of {SUITE_IDS})")
    if not customer_id.strip():
        raise ValueError("customer_id is required")

    results: list[EvalResult] = []
    if suite_id in ("knowledge_os", "all"):
        results += _run_knowledge_suite(customer_id)
    if suite_id in ("agent_runtime", "all"):
        results += _run_agent_suite(customer_id)
    if suite_id in ("doctrine", "all"):
        results += run_doctrine_evals(customer_id)

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    pass_rate = round(passed / total, 4) if total else 0.0

    prior = last_run(customer_id=customer_id, suite_id=suite_id)
    regression = bool(prior and pass_rate < float(prior.get("pass_rate", 0.0)))

    summary = EvalRunSummary(
        suite_id=suite_id,
        customer_id=customer_id,
        total=total,
        passed=passed,
        pass_rate=pass_rate,
        regression_detected=regression,
        results=tuple(results),
    )
    emit_eval_run(summary)
    _emit_events(summary, prior)
    return summary


def _emit_events(summary: EvalRunSummary, prior: dict | None) -> None:
    store = get_default_store()
    try:
        store.append(
            make_event(
                event_type="ai.eval_run",
                customer_id=summary.customer_id,
                subject_type="customer",
                subject_id=summary.customer_id,
                payload={
                    "run_id": summary.run_id,
                    "suite_id": summary.suite_id,
                    "pass_rate": summary.pass_rate,
                    "total": summary.total,
                    "passed": summary.passed,
                },
                actor="evals_os",
            )
        )
        if summary.regression_detected:
            store.append(
                make_event(
                    event_type="ai.regression_detected",
                    customer_id=summary.customer_id,
                    subject_type="customer",
                    subject_id=summary.customer_id,
                    payload={
                        "run_id": summary.run_id,
                        "suite_id": summary.suite_id,
                        "pass_rate": summary.pass_rate,
                        "previous_pass_rate": float((prior or {}).get("pass_rate", 0.0)),
                    },
                    actor="evals_os",
                )
            )
    except Exception:  # noqa: BLE001 — audit best-effort, never blocks the run
        pass

    if summary.regression_detected:
        try:
            from auto_client_acquisition.friction_log.schemas import (
                FrictionKind,
                FrictionSeverity,
            )
            from auto_client_acquisition.friction_log.store import emit as emit_friction

            emit_friction(
                customer_id=summary.customer_id,
                kind=FrictionKind.AI_REGRESSION,
                severity=FrictionSeverity.HIGH,
                evidence_ref=summary.run_id,
                notes=f"eval suite {summary.suite_id} pass_rate dropped to {summary.pass_rate}",
            )
        except Exception:  # noqa: BLE001
            pass
