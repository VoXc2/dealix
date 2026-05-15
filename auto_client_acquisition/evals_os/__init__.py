"""Evals OS — quality measurement for Knowledge OS + the agent runtime.

RAG faithfulness, hallucination detection, agent-loop safety, and the 11
non-negotiables as runnable checks — all ledgered, with regression
detection against prior runs.
"""

from auto_client_acquisition.evals_os.agent_evals import eval_agent_loop
from auto_client_acquisition.evals_os.doctrine_evals import run_doctrine_evals
from auto_client_acquisition.evals_os.eval_ledger import (
    clear_for_test,
    emit_eval_run,
    last_run,
    list_eval_runs,
)
from auto_client_acquisition.evals_os.rag_evals import eval_rag, rag_eval_to_result
from auto_client_acquisition.evals_os.runner import SUITE_IDS, run_suite
from auto_client_acquisition.evals_os.schemas import (
    EvalCase,
    EvalResult,
    EvalRunSummary,
    RAGEvalResult,
)

__all__ = [
    "EvalCase",
    "EvalResult",
    "EvalRunSummary",
    "RAGEvalResult",
    "SUITE_IDS",
    "clear_for_test",
    "emit_eval_run",
    "eval_agent_loop",
    "eval_rag",
    "last_run",
    "list_eval_runs",
    "rag_eval_to_result",
    "run_doctrine_evals",
    "run_suite",
]
