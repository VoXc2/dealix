"""Enterprise Foundation Core — one coherent governed enterprise loop.

This package is a thin facade. It does NOT rewrite the underlying systems —
it imports and re-exports the existing governance, identity, workflow,
agent-registry and audit primitives that already live under
``auto_client_acquisition/`` and wires them into a single runnable loop.

The loop proves the foundation works end to end:
    tenant -> users -> roles -> agent -> workflow -> approval
    -> CRM draft -> executive report -> eval report -> rollback drill
    -> audit verification

See ``platform_core.enterprise_loop`` for the orchestrator and
``api/routers/platform_foundation.py`` for the live proof endpoints.
"""

from __future__ import annotations

from platform_core import (
    agent_runtime,
    governance,
    identity,
    multi_tenant,
    observability,
    rbac,
    workflow_engine,
)
from platform_core.enterprise_loop import (
    LoopContext,
    LoopStepResult,
    run_enterprise_loop,
)

__all__ = [
    "LoopContext",
    "LoopStepResult",
    "agent_runtime",
    "governance",
    "identity",
    "multi_tenant",
    "observability",
    "rbac",
    "run_enterprise_loop",
    "workflow_engine",
]
