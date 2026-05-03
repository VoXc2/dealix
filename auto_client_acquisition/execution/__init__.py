"""
Execution — the "what happens after approval" layer.

When an approval-queue item gets `/approve`, the execution layer checks:
  1. Is the gate for this channel open?  (gate-open?)
  2. Is the channel in approved_channels for this customer?  (allowed?)
  3. Does the channel need a 24h-window or template?  (constraints?)

If all yes → execute the actual send via the right transport client.
If no → log "approved but not auto-executed; founder must send manually".

This makes Dealix Full Ops within the safety constraints we cannot legally cross
(LinkedIn auto-DM forbidden; cold WhatsApp forbidden; Moyasar live charge needs KYB).
"""

from auto_client_acquisition.execution.auto_executor import (
    AutoExecuteResult,
    auto_execute_approved,
)

__all__ = ["AutoExecuteResult", "auto_execute_approved"]
