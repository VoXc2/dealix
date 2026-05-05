"""AI Workforce v7 — orchestration layer over v5/v6 modules.

Pure local composition; no LLM, no external HTTP. Each agent is a
thin wrapper over an existing v5/v6 function with an explicit
autonomy level + ComplianceGuard veto at the end.

This package ships in two waves:
- ``cost_guard`` (P4) — budget + model-tier helpers, available now
- ``schemas`` / ``orchestrator`` / ``agent_registry`` / ``agent_contracts``
  / ``workforce_policy`` / ``risk_guard`` / ``evidence_writer``
  / ``language_router`` / ``task_router`` (P1+P2) — agent ships these

Public symbols re-exported below as they become available.
"""
from auto_client_acquisition.ai_workforce import cost_guard  # noqa: F401

__all__ = ["cost_guard"]
