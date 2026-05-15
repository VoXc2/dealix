"""Agent Factory — build-time composition layer for governed agents.
مصنع الوكلاء — طبقة تركيب وقت البناء للوكلاء المحكومين.

Scaffold scope: clean contracts + base structure + a reference path.
Layering rule — ``agent_factory`` NEVER reimplements risk scoring, tool
permissions, governance, lifecycle, or retrieval. It only composes them:

  * ``agent_os``             — primitive identity + registry + tool vocabulary.
  * ``agentic_operations_os`` — policy runtime: risk, ToolClass, lifecycle, governance.
  * ``agent_factory``        — takes an ``AgentBlueprint`` → runs the policy gates
                               → registers an ``AgentCard``; owns the eval-harness
                               and observability contracts and the memory binding.
"""

from auto_client_acquisition.agent_factory.blueprint import (
    AgentBlueprint,
    EscalationRule,
    EscalationTrigger,
    EvaluationRule,
    blueprint_structurally_valid,
)
from auto_client_acquisition.agent_factory.builder import (
    BuildOutcome,
    BuildResult,
    build_agent,
)
from auto_client_acquisition.agent_factory.eval_harness import (
    AgentEvalCase,
    AgentEvalResult,
    AgentEvalSuite,
    AgentEvalSuiteResult,
    run_eval_case,
    run_eval_suite,
)
from auto_client_acquisition.agent_factory.memory_binding import (
    AgentMemoryBinding,
    binding_valid,
    build_retrieval_request,
    retrieve_for_agent,
)
from auto_client_acquisition.agent_factory.trace import (
    AgentRunTrace,
    AgentStepRecord,
    TraceStatus,
    append_step,
    new_trace,
    summarize_trace,
)

__all__ = [
    "AgentBlueprint",
    "AgentEvalCase",
    "AgentEvalResult",
    "AgentEvalSuite",
    "AgentEvalSuiteResult",
    "AgentMemoryBinding",
    "AgentRunTrace",
    "AgentStepRecord",
    "BuildOutcome",
    "BuildResult",
    "EscalationRule",
    "EscalationTrigger",
    "EvaluationRule",
    "TraceStatus",
    "append_step",
    "binding_valid",
    "blueprint_structurally_valid",
    "build_agent",
    "build_retrieval_request",
    "new_trace",
    "retrieve_for_agent",
    "run_eval_case",
    "run_eval_suite",
    "summarize_trace",
]
