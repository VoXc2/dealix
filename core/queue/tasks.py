"""
ARQ background task definitions — agent invocations off the request path.
تعريفات المهام الخلفية — تشغيل الوكلاء خارج مسار الطلب.

Each task function signature:
    async def task(ctx: dict, ...kwargs) -> dict

ARQ injects `ctx` with the Redis connection and any worker-startup state.
"""

from __future__ import annotations

import logging
from datetime import datetime, UTC
from typing import Any

from arq import ArqRedis

from core.config.settings import get_settings
from core.utils import generate_id, utcnow

logger = logging.getLogger(__name__)

# ── Cost hints (USD per 1k tokens) — used for budget enforcement ──
COST_PER_1K_INPUT: float = 0.003   # conservative Anthropic estimate
COST_PER_1K_OUTPUT: float = 0.015


# ═══════════════════════════════════════════════════════════════════
# Background task: run_agent_job
# ═══════════════════════════════════════════════════════════════════

async def run_agent_job(
    ctx: dict[str, Any],
    job_id: str,
    job_type: str,
    payload: dict[str, Any],
    tenant_id: str | None = None,
) -> dict[str, Any]:
    """
    Execute an agent invocation in the background.
    تشغيل وكيل في الخلفية وتتبع الحالة في BackgroundJobRecord.

    Args:
        ctx:       ARQ context (contains Redis connection).
        job_id:    Matches BackgroundJobRecord.id so callers can poll status.
        job_type:  e.g. "lead_score", "proposal_draft", "outreach_batch".
        payload:   Arbitrary input forwarded to the agent.
        tenant_id: Optional tenant for multi-tenancy filtering.

    Returns:
        Dict with status, output, and token usage.
    """
    started_at = utcnow()
    logger.info("job_started", job_id=job_id, job_type=job_type, tenant_id=tenant_id)

    # ── Persist: mark running ─────────────────────────────────────
    await _update_job_status(
        job_id=job_id,
        status="running",
        started_at=started_at,
    )

    try:
        result = await _dispatch(job_type=job_type, payload=payload, tenant_id=tenant_id)

        completed_at = utcnow()
        duration_ms = (completed_at - started_at).total_seconds() * 1000

        # ── Persist: mark succeeded ───────────────────────────────
        await _update_job_status(
            job_id=job_id,
            status="succeeded",
            output=result,
            completed_at=completed_at,
        )

        logger.info(
            "job_succeeded",
            job_id=job_id,
            job_type=job_type,
            duration_ms=round(duration_ms),
        )
        return {"job_id": job_id, "status": "succeeded", "output": result}

    except Exception as exc:  # noqa: BLE001
        completed_at = utcnow()
        logger.exception("job_failed", job_id=job_id, job_type=job_type, error=str(exc))

        retry_count = ctx.get("job_try", 1)
        is_final = retry_count >= 3  # WorkerSettings.max_tries

        await _update_job_status(
            job_id=job_id,
            status="failed" if is_final else "retrying",
            error=str(exc),
            completed_at=completed_at if is_final else None,
        )
        raise  # let ARQ handle retry logic


# ── Internal helpers ──────────────────────────────────────────────

async def _dispatch(job_type: str, payload: dict[str, Any], tenant_id: str | None) -> dict[str, Any]:
    """
    Route job_type to the correct agent or function.
    يوجّه نوع المهمة إلى الوكيل أو الوظيفة المناسبة.
    """
    if job_type == "lead_score":
        return await _run_lead_score(payload, tenant_id)
    if job_type == "proposal_draft":
        return await _run_proposal_draft(payload, tenant_id)
    if job_type == "outreach_batch":
        return await _run_outreach_batch(payload, tenant_id)
    if job_type == "embedding_index":
        return await _run_embedding_index(payload, tenant_id)
    # Generic LLM task
    return await _run_generic_llm(payload, tenant_id)


async def _run_lead_score(payload: dict[str, Any], tenant_id: str | None) -> dict[str, Any]:
    from core.llm import get_router
    from core.config.models import Task
    from core.llm.base import Message

    router = get_router()
    account_summary = payload.get("account_summary", "")
    resp = await router.run(
        Task.CLASSIFICATION,
        messages=[Message(role="user", content=f"Score this lead 0-100:\n{account_summary}")],
        system="You are a B2B lead scoring expert for the Saudi market. Return JSON: {{\"score\": <int>, \"reason\": \"<str>\"}}",
        max_tokens=512,
        temperature=0.2,
    )
    return {"lead_score_response": resp.content, "tokens": resp.total_tokens}


async def _run_proposal_draft(payload: dict[str, Any], tenant_id: str | None) -> dict[str, Any]:
    from core.llm import get_router
    from core.config.models import Task
    from core.llm.base import Message

    router = get_router()
    context = payload.get("context", "")
    resp = await router.run(
        Task.PROPOSAL,
        messages=[Message(role="user", content=context)],
        system="You are a senior Saudi B2B sales consultant. Draft a professional proposal in Arabic and English.",
        max_tokens=4096,
        temperature=0.4,
    )
    return {"proposal": resp.content, "tokens": resp.total_tokens}


async def _run_outreach_batch(payload: dict[str, Any], tenant_id: str | None) -> dict[str, Any]:
    results = []
    accounts = payload.get("accounts", [])
    for acc in accounts[:50]:  # cap at 50 per job
        results.append({"account_id": acc.get("id"), "status": "queued"})
    return {"queued": len(results), "accounts": results}


async def _run_embedding_index(payload: dict[str, Any], tenant_id: str | None) -> dict[str, Any]:
    from core.memory.revenue_memory import RevenueMemory
    memory = RevenueMemory()
    entity_type = payload.get("entity_type", "account")
    entity_id = payload.get("entity_id", "")
    text = payload.get("text", "")
    if entity_type == "account":
        await memory.index_account(account_id=entity_id, text=text, tenant_id=tenant_id)
    elif entity_type == "conversation":
        await memory.index_conversation(conversation_id=entity_id, text=text, tenant_id=tenant_id)
    return {"indexed": True, "entity_type": entity_type, "entity_id": entity_id}


async def _run_generic_llm(payload: dict[str, Any], tenant_id: str | None) -> dict[str, Any]:
    from core.llm import get_router
    from core.config.models import Task
    from core.llm.base import Message

    router = get_router()
    prompt = payload.get("prompt", "")
    task_str = payload.get("task", "reasoning")
    task = Task(task_str) if task_str in Task._value2member_map_ else Task.REASONING  # type: ignore[attr-defined]
    resp = await router.run(
        task,
        messages=[Message(role="user", content=prompt)],
        system=payload.get("system"),
        max_tokens=payload.get("max_tokens", 2048),
        temperature=payload.get("temperature", 0.7),
    )
    return {"content": resp.content, "tokens": resp.total_tokens, "provider": resp.provider}


# ── Job status DB helper ──────────────────────────────────────────

async def _update_job_status(
    job_id: str,
    status: str,
    *,
    output: dict[str, Any] | None = None,
    error: str | None = None,
    started_at: datetime | None = None,
    completed_at: datetime | None = None,
) -> None:
    """Upsert BackgroundJobRecord status."""
    try:
        from db.session import get_session
        from db.models import BackgroundJobRecord
        from sqlalchemy import select

        async with get_session() as session:
            result = await session.execute(
                select(BackgroundJobRecord).where(BackgroundJobRecord.id == job_id)
            )
            rec: BackgroundJobRecord | None = result.scalar_one_or_none()
            if rec:
                rec.status = status
                if output is not None:
                    rec.output_payload = output
                if error is not None:
                    rec.error = error
                if started_at is not None:
                    rec.started_at = started_at
                if completed_at is not None:
                    rec.completed_at = completed_at
                if status == "retrying":
                    rec.retry_count = (rec.retry_count or 0) + 1
    except Exception as exc:  # noqa: BLE001
        logger.warning("job_status_update_failed", job_id=job_id, error=str(exc))


# ═══════════════════════════════════════════════════════════════════
# Enqueue helper — called from FastAPI request handlers
# ═══════════════════════════════════════════════════════════════════

async def enqueue_agent_job(
    redis: ArqRedis,
    job_type: str,
    payload: dict[str, Any],
    *,
    tenant_id: str | None = None,
    job_id: str | None = None,
    _queue_name: str = "dealix:arq:default",
) -> str:
    """
    Persist a BackgroundJobRecord then enqueue the ARQ job.
    احفظ سجل المهمة في قاعدة البيانات ثم ضعها في الطابور.

    Returns the job_id callers can use to poll /api/v1/jobs/{job_id}.
    """
    job_id = job_id or generate_id("job")

    # ── Persist job record first ──────────────────────────────────
    try:
        from db.session import get_session
        from db.models import BackgroundJobRecord

        async with get_session() as session:
            rec = BackgroundJobRecord(
                id=job_id,
                tenant_id=tenant_id,
                job_type=job_type,
                status="pending",
                input_payload=payload,
            )
            session.add(rec)
    except Exception as exc:  # noqa: BLE001
        logger.warning("job_record_create_failed", job_id=job_id, error=str(exc))

    # ── Enqueue in ARQ (Redis) ────────────────────────────────────
    await redis.enqueue_job(
        "run_agent_job",
        job_id=job_id,
        job_type=job_type,
        payload=payload,
        tenant_id=tenant_id,
        _queue_name=_queue_name,
        _job_id=job_id,  # ARQ dedup key
    )

    logger.info("job_enqueued", job_id=job_id, job_type=job_type)
    return job_id
