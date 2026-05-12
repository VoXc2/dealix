"""
LLM cost guardrails — per-request hard cap + per-tenant daily cap.

Why: a runaway prompt with a 32k-token context can cost > $1 in one call.
At our pricing tiers, that's profit gone if it happens on the wrong
customer. The guardrail enforces a deterministic ceiling and prefers
*degrading to a cheaper model* over surfacing a 5xx.

Public surface:
    @cost_guarded(estimated_tokens=lambda req: ...)
    async def call_anthropic(...): ...

Or imperatively:
    guard = CostGuard(tenant_id=...)
    if not guard.can_spend(estimated_usd):
        ... # switch to cheaper model or fail
    await call_llm(...)
    guard.record_spend(actual_usd)

Limits are env-driven:
    LLM_MAX_USD_PER_REQUEST            (default 0.50)
    LLM_MAX_USD_PER_TENANT_DAY         (default 25.00)
    LLM_DEGRADE_MODEL                  (e.g. claude-haiku) — when set,
                                       degraded calls swap to this model.

Storage: short-window per-tenant spend lives in Redis under
`dealix:llm:spend:{tenant_id}:{YYYYMMDD}`. Falls back to an in-process
dict when Redis is unavailable so tests don't need Redis up.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar

from core.logging import get_logger

log = get_logger(__name__)

T = TypeVar("T")


class CostCapExceeded(RuntimeError):
    """Raised when the request would breach the per-request cap."""


# Best-effort in-process counter; Redis adapter swaps it out below.
_local_counters: dict[str, float] = {}


def _today_key(tenant_id: str) -> str:
    return f"dealix:llm:spend:{tenant_id}:{datetime.now(timezone.utc).strftime('%Y%m%d')}"


def _max_per_request() -> float:
    try:
        return float(os.getenv("LLM_MAX_USD_PER_REQUEST", "0.50"))
    except ValueError:
        return 0.50


def _max_per_tenant_day() -> float:
    try:
        return float(os.getenv("LLM_MAX_USD_PER_TENANT_DAY", "25.00"))
    except ValueError:
        return 25.00


def degrade_model() -> str | None:
    val = os.getenv("LLM_DEGRADE_MODEL", "").strip()
    return val or None


@dataclass
class CostGuard:
    tenant_id: str
    request_cap_usd: float = field(default_factory=_max_per_request)
    tenant_day_cap_usd: float = field(default_factory=_max_per_tenant_day)

    async def current_day_spend_usd(self) -> float:
        """Return today's cumulative spend for this tenant."""
        key = _today_key(self.tenant_id)
        try:
            import redis.asyncio as redis  # type: ignore
        except Exception:
            return float(_local_counters.get(key, 0.0))
        url = os.getenv("REDIS_URL", "").strip()
        if not url:
            return float(_local_counters.get(key, 0.0))
        try:
            client = redis.from_url(url, decode_responses=True)
            raw = await client.get(key)
            await client.aclose()
            return float(raw or 0.0)
        except Exception:
            return float(_local_counters.get(key, 0.0))

    def can_spend_sync(self, estimated_usd: float) -> tuple[bool, str | None]:
        """Synchronous cap check ignoring per-tenant accumulation.

        Suitable for boot-time / hot-path checks. The per-tenant rolling
        check uses `await CostGuard.can_spend(...)` instead.
        """
        if estimated_usd > self.request_cap_usd:
            return False, "per_request_cap_exceeded"
        return True, None

    async def can_spend(self, estimated_usd: float) -> tuple[bool, str | None]:
        ok, reason = self.can_spend_sync(estimated_usd)
        if not ok:
            return False, reason
        spent = await self.current_day_spend_usd()
        if spent + estimated_usd > self.tenant_day_cap_usd:
            return False, "tenant_day_cap_exceeded"
        return True, None

    async def record_spend(self, actual_usd: float) -> None:
        key = _today_key(self.tenant_id)
        # Update local counter first so even if Redis is down we still
        # enforce within the process lifetime.
        _local_counters[key] = float(_local_counters.get(key, 0.0)) + float(actual_usd)
        try:
            import redis.asyncio as redis  # type: ignore
        except Exception:
            return
        url = os.getenv("REDIS_URL", "").strip()
        if not url:
            return
        try:
            client = redis.from_url(url, decode_responses=True)
            pipe = client.pipeline()
            pipe.incrbyfloat(key, float(actual_usd))
            pipe.expire(key, 60 * 60 * 30)  # 30 hours, covers TZ edges
            await pipe.execute()
            await client.aclose()
        except Exception:
            log.warning("cost_guard_redis_record_failed", tenant=self.tenant_id)


def cost_guarded(
    estimate_usd: Callable[..., float],
    *,
    actual_usd: Callable[[Any], float] | None = None,
    tenant_id_arg: str = "tenant_id",
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """Decorator wiring a single LLM call to CostGuard checks.

    `estimate_usd` is called with the same args/kwargs as the wrapped
    function. If `actual_usd` is provided, it's invoked on the return
    value to record the real cost; otherwise the estimate is recorded.
    """

    def decorator(fn: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            tenant_id = kwargs.get(tenant_id_arg) or "unknown"
            est = float(estimate_usd(*args, **kwargs))
            guard = CostGuard(tenant_id=str(tenant_id))
            ok, reason = await guard.can_spend(est)
            if not ok:
                degrade = degrade_model()
                log.warning(
                    "llm_cost_cap_hit",
                    tenant_id=tenant_id,
                    estimate_usd=est,
                    reason=reason,
                    degrade_to=degrade,
                )
                if degrade and "model" in kwargs:
                    kwargs["model"] = degrade
                else:
                    raise CostCapExceeded(reason or "cost_cap_exceeded")
            t0 = time.perf_counter()
            result = await fn(*args, **kwargs)
            elapsed = time.perf_counter() - t0
            actual = float(actual_usd(result)) if actual_usd else est
            await guard.record_spend(actual)
            log.info(
                "llm_cost_recorded",
                tenant_id=tenant_id,
                actual_usd=actual,
                elapsed_s=round(elapsed, 3),
            )
            return result

        return wrapper

    return decorator
