"""
Cost Tracker — append cost / latency / token records per agent run.

Pure write helpers + simple aggregation reads. Pricing per provider lives
in `_USD_PER_MTOK` (per-million-token rates). Numbers are rough but the
ledger lets us tighten them later by reprocessing rows.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auto_client_acquisition.agent_observability.trace_redactor import redact_dict
from db.models import AgentRunCostRecord


# USD per 1M tokens — rough public list prices, used for budget visibility
# only. Authoritative billing comes from each provider's invoice.
_USD_PER_MTOK: dict[str, dict[str, tuple[float, float]]] = {
    # provider: { model_substring: (input_usd, output_usd) }
    "anthropic": {
        "haiku":  (0.80,  4.00),
        "sonnet": (3.00, 15.00),
        "opus":  (15.00, 75.00),
    },
    "openai": {
        "gpt-4o-mini": (0.15, 0.60),
        "gpt-4o":      (5.00, 15.00),
    },
    "deepseek": {"":  (0.27, 1.10)},
    "groq":     {"":  (0.05, 0.10)},
    "google":   {
        "1.5-flash": (0.075, 0.30),
        "1.5-pro":   (1.25, 5.00),
    },
}

USD_TO_SAR = 3.75  # SAR is pegged ~3.75 to USD


def _new_id() -> str:
    return f"cost_{uuid.uuid4().hex[:14]}"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def estimate_cost_usd(*, provider: str | None, model: str | None,
                     input_tokens: int, output_tokens: int) -> float:
    """Rough USD estimate. Returns 0 if provider/model not catalogued."""
    if not provider:
        return 0.0
    p = provider.lower().strip()
    catalog = _USD_PER_MTOK.get(p, {})
    if not catalog:
        return 0.0
    m = (model or "").lower()
    rate = None
    for key, val in catalog.items():
        if not key or key in m:
            rate = val
            break
    if rate is None:
        return 0.0
    in_usd, out_usd = rate
    return round(
        (input_tokens / 1_000_000.0) * in_usd
        + (output_tokens / 1_000_000.0) * out_usd,
        6,
    )


async def record_run(
    session: AsyncSession,
    *,
    agent_name: str,
    agent_run_id: str | None = None,
    service_id: str | None = None,
    role: str | None = None,
    customer_id: str | None = None,
    partner_id: str | None = None,
    provider: str | None = None,
    model: str | None = None,
    input_tokens: int = 0,
    output_tokens: int = 0,
    latency_ms: int = 0,
    tool_calls_count: int = 0,
    error_type: str | None = None,
    meta: dict[str, Any] | None = None,
) -> AgentRunCostRecord:
    """Write one cost record. Caller commits. PII in meta is redacted first."""
    cost_usd = estimate_cost_usd(
        provider=provider, model=model,
        input_tokens=input_tokens, output_tokens=output_tokens,
    )
    row = AgentRunCostRecord(
        id=_new_id(),
        agent_run_id=agent_run_id,
        agent_name=agent_name,
        service_id=service_id,
        role=role,
        customer_id=customer_id,
        partner_id=partner_id,
        cost_estimate_usd=cost_usd,
        cost_estimate_sar=round(cost_usd * USD_TO_SAR, 4),
        latency_ms=int(latency_ms or 0),
        input_tokens=int(input_tokens or 0),
        output_tokens=int(output_tokens or 0),
        provider=provider,
        model=model,
        tool_calls_count=int(tool_calls_count or 0),
        error_type=error_type,
        occurred_at=_now(),
        meta_json=redact_dict(meta or {}),
    )
    session.add(row)
    return row


async def summarize(
    session: AsyncSession,
    *,
    days: int = 7,
    role: str | None = None,
    service_id: str | None = None,
) -> dict[str, Any]:
    """Aggregate cost / latency / token counts over the last N days."""
    since = _now() - timedelta(days=max(1, days))
    q = select(AgentRunCostRecord).where(AgentRunCostRecord.occurred_at >= since)
    if role:
        q = q.where(AgentRunCostRecord.role == role)
    if service_id:
        q = q.where(AgentRunCostRecord.service_id == service_id)
    rows = list((await session.execute(q)).scalars().all())

    total_usd = sum(r.cost_estimate_usd for r in rows)
    total_sar = sum(r.cost_estimate_sar for r in rows)
    total_in = sum(r.input_tokens for r in rows)
    total_out = sum(r.output_tokens for r in rows)
    errors = sum(1 for r in rows if r.error_type)

    by_provider: dict[str, float] = {}
    by_role: dict[str, float] = {}
    by_service: dict[str, float] = {}
    for r in rows:
        by_provider[r.provider or "unknown"] = round(by_provider.get(r.provider or "unknown", 0.0) + r.cost_estimate_sar, 4)
        if r.role:
            by_role[r.role] = round(by_role.get(r.role, 0.0) + r.cost_estimate_sar, 4)
        if r.service_id:
            by_service[r.service_id] = round(by_service.get(r.service_id, 0.0) + r.cost_estimate_sar, 4)

    avg_latency_ms = round(sum(r.latency_ms for r in rows) / max(len(rows), 1), 1)

    return {
        "since": since.isoformat(),
        "run_count": len(rows),
        "total_cost_usd": round(total_usd, 4),
        "total_cost_sar": round(total_sar, 4),
        "input_tokens": total_in,
        "output_tokens": total_out,
        "error_count": errors,
        "error_rate": round(errors / max(len(rows), 1), 4),
        "avg_latency_ms": avg_latency_ms,
        "cost_sar_by_provider": by_provider,
        "cost_sar_by_role": by_role,
        "cost_sar_by_service": by_service,
    }
