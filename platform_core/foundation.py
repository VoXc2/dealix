"""Foundation — single aggregate import surface for the Enterprise Foundation Core.

Prefer importing from here when a caller needs more than one facade:

    from platform_core.foundation import multi_tenant, governance, run_enterprise_loop
"""

from __future__ import annotations

from platform_core import (
    agent_runtime,
    governance,
    identity,
    multi_tenant,
    observability,
    rbac,
    stores,
    workflow_engine,
)
from platform_core.enterprise_loop import (
    RUN_STORE,
    LoopContext,
    LoopStepResult,
    get_run,
    new_run,
    run_enterprise_loop,
)

__all__ = [
    "RUN_STORE",
    "LoopContext",
    "LoopStepResult",
    "agent_runtime",
    "get_run",
    "governance",
    "identity",
    "multi_tenant",
    "new_run",
    "observability",
    "rbac",
    "run_enterprise_loop",
    "stores",
    "workflow_engine",
]
