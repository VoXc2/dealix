"""Tool Guardrail Gateway (Phase 8 Wave 5).

OpenAI-Agents-SDK-style guardrails wrapping every tool call:
  input_guardrails  → prompt injection + PII overexposure check
  tool_guardrails   → per-tool permission (Moyasar live, WhatsApp, etc.)
  output_guardrails → forbidden tokens scrub + ROI-claim regex
  cost_budget       → per-call token + dollar cap
  audit             → every gate decision recorded
"""
from auto_client_acquisition.tool_guardrail_gateway.audit import audit_decision
from auto_client_acquisition.tool_guardrail_gateway.cost_budget import (
    check_cost_budget,
)
from auto_client_acquisition.tool_guardrail_gateway.input_guardrails import (
    check_input,
)
from auto_client_acquisition.tool_guardrail_gateway.output_guardrails import (
    check_output,
)
from auto_client_acquisition.tool_guardrail_gateway.tool_guardrails import (
    check_tool_permission,
)

__all__ = [
    "audit_decision",
    "check_cost_budget",
    "check_input",
    "check_output",
    "check_tool_permission",
]
