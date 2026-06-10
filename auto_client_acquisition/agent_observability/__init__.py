"""Agent Observability shim (Phase 11).

This is a thin re-export over auto_client_acquisition.observability_v10
which already does PII-redacted trace recording. Provides a stable
namespace for Wave 4 (`/api/v1/agent-observability/*`) while keeping
the production buffer + redaction logic intact.

Future Langfuse / OpenTelemetry adapters can plug in here without
modifying observability_v10.
"""
from auto_client_acquisition.agent_observability.schemas import AgentTrace
from auto_client_acquisition.agent_observability.trace import (
    list_recent_traces,
    record_trace,
)

__all__ = ["AgentTrace", "list_recent_traces", "record_trace"]
