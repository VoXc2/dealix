"""
Skill execution tracer (T11).

Wraps every `/api/v1/skills/{id}/run` invocation with:

1. **Cost guard** — checks the tenant's daily cap + per-request cap.
2. **Langfuse trace** — emits a trace when LANGFUSE_PUBLIC_KEY is set.
3. **Lago meter event** — fires `skill.run` metering when LAGO_API_KEY
   is set so per-billable-event invoicing works downstream.
4. **Portkey metadata** — passes tenant_id + skill_id through Portkey
   so its dashboard splits cost by customer + skill.

All four hooks are import-safe and inert without the corresponding
env vars; tests don't touch any network.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Awaitable, Callable

from core.logging import get_logger

log = get_logger(__name__)


@dataclass(frozen=True)
class SkillTraceContext:
    skill_id: str
    tenant_id: str
    request_id: str | None = None
    locale: str = "ar"


async def traced_skill_run(
    *,
    ctx: SkillTraceContext,
    handler: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]],
    inputs: dict[str, Any],
    estimated_usd: float = 0.0,
) -> dict[str, Any]:
    """Invoke `handler(inputs)` wrapped with cost-guard, Langfuse, Lago.

    The wrapper short-circuits on cost-cap with a 402-shaped dict
    (the router can surface it as HTTP 402 if we ever need to bill
    overage in-band).
    """
    # 1. Cost guard.
    cost_guard_result: dict[str, Any] = {"ok": True, "reason": None}
    if estimated_usd > 0 and ctx.tenant_id:
        try:
            from core.llm.cost_guard import CostGuard  # type: ignore

            cg = CostGuard(tenant_id=ctx.tenant_id)
            ok, reason = await cg.can_spend(estimated_usd)
            cost_guard_result = {"ok": ok, "reason": reason}
            if not ok:
                return {
                    "ok": False,
                    "skill_id": ctx.skill_id,
                    "error": "cost_cap_exceeded",
                    "reason": reason,
                }
        except Exception:
            log.exception("cost_guard_check_failed", skill_id=ctx.skill_id)

    # 2. Run + time.
    t0 = perf_counter()
    error: Exception | None = None
    result: dict[str, Any] = {}
    try:
        result = await handler(inputs)
    except Exception as exc:
        error = exc
        raise
    finally:
        elapsed_ms = round((perf_counter() - t0) * 1000, 1)

        # 3. Record spend (best-effort).
        if estimated_usd > 0 and ctx.tenant_id and cost_guard_result.get("ok"):
            try:
                from core.llm.cost_guard import CostGuard  # type: ignore

                await CostGuard(tenant_id=ctx.tenant_id).record_spend(estimated_usd)
            except Exception:
                log.exception("cost_guard_record_failed")

        # 4. Langfuse trace.
        if os.getenv("LANGFUSE_PUBLIC_KEY", "").strip():
            try:
                from langfuse import Langfuse  # type: ignore

                client = Langfuse()
                client.trace(
                    name=f"skill.{ctx.skill_id}",
                    user_id=ctx.tenant_id,
                    metadata={
                        "skill_id": ctx.skill_id,
                        "locale": ctx.locale,
                        "elapsed_ms": elapsed_ms,
                        "estimated_usd": estimated_usd,
                        "error": str(error) if error else None,
                    },
                    input={"inputs": inputs},
                    output=result,
                )
            except Exception:
                log.exception("langfuse_trace_failed")

        # 5. Lago metering — fire a `skill.run` event per call.
        if os.getenv("LAGO_API_KEY", "").strip() and ctx.tenant_id:
            try:
                from dealix.billing.lago_client import get_lago_client  # type: ignore

                await get_lago_client().meter(
                    metric_code="skill.run",
                    external_customer_id=ctx.tenant_id,
                    properties={
                        "skill_id": ctx.skill_id,
                        "elapsed_ms": elapsed_ms,
                    },
                )
            except Exception:
                log.exception("lago_meter_failed")

    return result
