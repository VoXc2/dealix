"""
Background jobs API — submit and track async agent tasks.
واجهة برمجية للمهام الخلفية — تقديم ومتابعة المهام غير المتزامنة.

Endpoints:
  POST /jobs/lead-score             → enqueue lead scoring
  POST /jobs/proposal-draft         → enqueue proposal draft
  POST /jobs/outreach-batch         → enqueue outreach batch
  POST /jobs                        → generic enqueue
  GET  /jobs/{job_id}               → poll job status
  GET  /jobs/{job_id}/stream        → SSE real-time status stream
  GET  /jobs/                       → list recent jobs for tenant
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Annotated, Any, AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.utils import generate_id, utcnow
from db.models import BackgroundJobRecord
from db.session import get_db

router = APIRouter(prefix="/jobs", tags=["background-jobs"])
logger = get_logger(__name__)

# Lazy ARQ pool — initialised on first enqueue
_redis_pool: Any = None


async def _get_redis_pool() -> Any:
    """Get or create the ARQ Redis pool."""
    global _redis_pool
    if _redis_pool is None:
        from arq import create_pool  # noqa: PLC0415
        from arq.connections import RedisSettings  # noqa: PLC0415
        from core.config.settings import get_settings  # noqa: PLC0415
        settings = get_settings()
        _redis_pool = await create_pool(RedisSettings.from_dsn(settings.redis_url))
    return _redis_pool


# ── Pydantic schemas ───────────────────────────────────────────────

class JobStatusResponse(BaseModel):
    id: str
    job_type: str
    status: str
    tenant_id: str | None = None
    input_payload: dict[str, Any] = Field(default_factory=dict)
    output_payload: dict[str, Any] | None = None
    error: str | None = None
    retry_count: int = 0
    created_at: str
    started_at: str | None = None
    completed_at: str | None = None
    stream_url: str | None = None


class EnqueueJobRequest(BaseModel):
    job_type: str = Field(
        ...,
        description=(
            "Job type: lead_score | proposal_draft | outreach_batch | "
            "embedding_index | generic_llm"
        ),
        examples=["lead_score"],
    )
    payload: dict[str, Any] = Field(default_factory=dict)
    tenant_id: str | None = None


class LeadScoreRequest(BaseModel):
    lead_id: str
    tenant_id: str


class ProposalDraftRequest(BaseModel):
    deal_id: str
    tenant_id: str
    lang: str = "ar"


class OutreachBatchRequest(BaseModel):
    batch_id: str
    tenant_id: str


# ── Helpers ────────────────────────────────────────────────────────

async def _create_job_record(
    session: AsyncSession,
    job_type: str,
    tenant_id: str,
    input_payload: dict[str, Any],
) -> BackgroundJobRecord:
    job = BackgroundJobRecord(
        id=generate_id("job"),
        tenant_id=tenant_id,
        job_type=job_type,
        status="pending",
        input_payload=input_payload,
    )
    session.add(job)
    await session.commit()
    return job


def _job_to_response(job: BackgroundJobRecord, request: Request | None = None) -> JobStatusResponse:
    stream_url: str | None = None
    if request is not None:
        base = str(request.base_url).rstrip("/")
        stream_url = f"{base}/api/v1/jobs/{job.id}/stream"

    return JobStatusResponse(
        id=job.id,
        job_type=job.job_type,
        status=job.status,
        tenant_id=job.tenant_id,
        input_payload=job.input_payload or {},
        output_payload=job.output_payload,
        error=job.error,
        retry_count=job.retry_count or 0,
        created_at=job.created_at.isoformat(),
        started_at=job.started_at.isoformat() if job.started_at else None,
        completed_at=job.completed_at.isoformat() if job.completed_at else None,
        stream_url=stream_url,
    )


def _sse_event(data: dict[str, Any], event: str = "message") -> str:
    """Format a Server-Sent Event string."""
    payload = json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"


# ── Generic enqueue — POST /jobs ───────────────────────────────────

@router.post(
    "",
    response_model=JobStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Generic: enqueue a background agent job",
)
async def enqueue_job(
    body: EnqueueJobRequest,
    request: Request,
    session: AsyncSession = Depends(get_db),
) -> JobStatusResponse:
    """
    Enqueue any supported agent job via ARQ (Redis).
    أضف أي مهمة وكيل مدعومة إلى قائمة الانتظار عبر ARQ.

    Returns job_id with 202 Accepted. Poll GET /jobs/{job_id} or stream via SSE.
    """
    try:
        redis = await _get_redis_pool()
        job = await _create_job_record(
            session, body.job_type, body.tenant_id or "default", body.payload
        )
        await redis.enqueue_job(
            "run_agent_job",
            job_id=job.id,
            job_type=body.job_type,
            payload=body.payload,
            tenant_id=body.tenant_id,
            _job_id=job.id,
            _queue_name="dealix:arq:default",
        )
        logger.info("job_enqueued", job_id=job.id, job_type=body.job_type)
        return _job_to_response(job, request)
    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="ARQ not installed. Redis queue unavailable.",
        )
    except Exception as exc:
        logger.exception("enqueue_job_error", exc_info=exc)
        raise HTTPException(status_code=500, detail=str(exc))


# ── Typed endpoints ────────────────────────────────────────────────

@router.post(
    "/lead-score",
    response_model=JobStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enqueue lead scoring",
)
async def enqueue_lead_score(
    body: LeadScoreRequest,
    request: Request,
    session: AsyncSession = Depends(get_db),
) -> JobStatusResponse:
    """Enqueue async lead scoring. Returns job record immediately (202)."""
    try:
        redis = await _get_redis_pool()
        payload = {"lead_id": body.lead_id, "tenant_id": body.tenant_id}
        job = await _create_job_record(session, "lead_score", body.tenant_id, payload)
        await redis.enqueue_job(
            "run_agent_job",
            job_id=job.id,
            job_type="lead_score",
            payload=payload,
            tenant_id=body.tenant_id,
            _job_id=job.id,
            _queue_name="dealix:arq:default",
        )
        logger.info("job_enqueued", job_id=job.id, job_type="lead_score")
        return _job_to_response(job, request)
    except ImportError:
        raise HTTPException(status_code=503, detail="ARQ Redis queue unavailable.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post(
    "/proposal-draft",
    response_model=JobStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enqueue proposal draft",
)
async def enqueue_proposal_draft(
    body: ProposalDraftRequest,
    request: Request,
    session: AsyncSession = Depends(get_db),
) -> JobStatusResponse:
    """Enqueue LLM proposal drafting for a deal."""
    try:
        redis = await _get_redis_pool()
        payload = {"deal_id": body.deal_id, "tenant_id": body.tenant_id, "lang": body.lang}
        job = await _create_job_record(session, "proposal_draft", body.tenant_id, payload)
        await redis.enqueue_job(
            "run_agent_job",
            job_id=job.id,
            job_type="proposal_draft",
            payload=payload,
            tenant_id=body.tenant_id,
            _job_id=job.id,
            _queue_name="dealix:arq:default",
        )
        return _job_to_response(job, request)
    except ImportError:
        raise HTTPException(status_code=503, detail="ARQ Redis queue unavailable.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post(
    "/outreach-batch",
    response_model=JobStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enqueue outreach email batch",
)
async def enqueue_outreach_batch(
    body: OutreachBatchRequest,
    request: Request,
    session: AsyncSession = Depends(get_db),
) -> JobStatusResponse:
    """Enqueue a personalised outreach batch execution."""
    try:
        redis = await _get_redis_pool()
        payload = {"batch_id": body.batch_id, "tenant_id": body.tenant_id}
        job = await _create_job_record(session, "outreach_batch", body.tenant_id, payload)
        await redis.enqueue_job(
            "run_agent_job",
            job_id=job.id,
            job_type="outreach_batch",
            payload=payload,
            tenant_id=body.tenant_id,
            _job_id=job.id,
            _queue_name="dealix:arq:default",
        )
        return _job_to_response(job, request)
    except ImportError:
        raise HTTPException(status_code=503, detail="ARQ Redis queue unavailable.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── GET /jobs/{job_id} — poll status ──────────────────────────────

@router.get(
    "/{job_id}",
    response_model=JobStatusResponse,
    summary="Poll job status",
)
async def get_job_status(
    job_id: str,
    request: Request,
    session: AsyncSession = Depends(get_db),
) -> JobStatusResponse:
    """
    Poll the status of a background job.
    الاستعلام عن حالة مهمة خلفية.

    Lifecycle: pending → running → succeeded | failed | retrying
    """
    result = await session.execute(
        select(BackgroundJobRecord).where(BackgroundJobRecord.id == job_id)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")
    return _job_to_response(job, request)


# ── GET /jobs/{job_id}/stream — SSE ───────────────────────────────

@router.get(
    "/{job_id}/stream",
    summary="SSE stream for real-time job status",
)
async def stream_job_status(
    job_id: str,
    session: AsyncSession = Depends(get_db),
    poll_interval_ms: int = Query(default=1000, ge=200, le=10000),
    timeout_s: int = Query(default=300, ge=10, le=600),
) -> StreamingResponse:
    """
    Server-Sent Events stream for real-time job status updates.
    بث أحداث SSE لمتابعة حالة المهمة في الوقت الفعلي.

    Streams until job reaches a terminal state or timeout.

    Client example (JS):
        const es = new EventSource('/api/v1/jobs/{job_id}/stream');
        es.addEventListener('succeeded', e => console.log(JSON.parse(e.data)));
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        elapsed = 0.0
        interval = poll_interval_ms / 1000.0
        terminal_statuses = {"succeeded", "failed"}
        last_status: str | None = None

        yield _sse_event(
            {"job_id": job_id, "event": "connected", "message": "Watching job status"},
            event="connected",
        )

        while elapsed < timeout_s:
            await asyncio.sleep(interval)
            elapsed += interval

            try:
                # Expire cached state so next query fetches fresh data from DB
                session.expire_all()
                result = await session.execute(
                    select(BackgroundJobRecord).where(BackgroundJobRecord.id == job_id)
                )
                job: BackgroundJobRecord | None = result.scalar_one_or_none()

                if job is None:
                    yield _sse_event(
                        {"job_id": job_id, "event": "error", "message": "Job not found"},
                        event="error",
                    )
                    return

                if job.status != last_status:
                    last_status = job.status
                    payload: dict[str, Any] = {
                        "job_id": job.id,
                        "status": job.status,
                        "retry_count": job.retry_count or 0,
                    }
                    if job.error:
                        payload["error"] = job.error
                    if job.output_payload and job.status == "succeeded":
                        payload["output"] = job.output_payload
                    if job.started_at:
                        payload["started_at"] = job.started_at.isoformat()
                    if job.completed_at:
                        payload["completed_at"] = job.completed_at.isoformat()

                    yield _sse_event(payload, event=job.status)

                    if job.status in terminal_statuses:
                        yield _sse_event(
                            {"job_id": job_id, "event": "done"},
                            event="done",
                        )
                        return

            except Exception as exc:
                logger.warning("sse_poll_error", job_id=job_id, error=str(exc))
                yield _sse_event(
                    {"job_id": job_id, "event": "error", "message": str(exc)},
                    event="error",
                )
                return

        yield _sse_event(
            {
                "job_id": job_id,
                "event": "timeout",
                "message": f"Stream timeout after {timeout_s}s",
            },
            event="timeout",
        )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ── GET /jobs/ — list recent jobs ─────────────────────────────────

@router.get(
    "/",
    response_model=list[JobStatusResponse],
    summary="List recent jobs for tenant",
)
async def list_jobs(
    request: Request,
    tenant_id: Annotated[str, Query(description="Tenant ID to filter by")],
    limit: int = Query(default=20, le=100),
    session: AsyncSession = Depends(get_db),
) -> list[JobStatusResponse]:
    """
    List the most recent background jobs for a tenant.
    عرض أحدث المهام الخلفية لمستأجر محدد.
    """
    result = await session.execute(
        select(BackgroundJobRecord)
        .where(BackgroundJobRecord.tenant_id == tenant_id)
        .order_by(BackgroundJobRecord.created_at.desc())
        .limit(limit)
    )
    jobs = result.scalars().all()
    return [_job_to_response(j, request) for j in jobs]
