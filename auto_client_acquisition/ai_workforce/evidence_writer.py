"""Stable evidence-id minting for AgentTasks.

V7 phase 1 keeps this in-memory only — no I/O. Future versions wire
to ``proof_ledger.record_event`` so each agent task drops a redacted
ProofEvent automatically.
"""
from __future__ import annotations

from uuid import uuid4

from auto_client_acquisition.ai_workforce.schemas import AgentTask


def record_evidence(task: AgentTask) -> str:
    """Return a stable evidence_id anchored to the task.

    Pure function: no file write, no DB write. The id encodes the
    agent_id so a future wiring can route the event to the correct
    audit channel without changing the call site.
    """
    short = uuid4().hex[:10]
    return f"evidence_{task.agent_id}_{short}"
