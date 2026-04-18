"""
Lead Intelligence Engine V2 — FastAPI Router
============================================
Endpoints:
  POST /api/v2/intelligence/discover       — start discovery job
  GET  /api/v2/intelligence/jobs/{job_id}  — job status + progress
  GET  /api/v2/intelligence/jobs/{job_id}/leads — paginated leads
  POST /api/v2/intelligence/jobs/{job_id}/export?format=csv|json — download
  WS   /api/v2/intelligence/jobs/{job_id}/stream — stream leads

Jobs stored in memory (dict keyed by UUID). Each job runs as a background task.
"""

from __future__ import annotations

import asyncio
import csv
import io
import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from app.intelligence.v2.models import (
    DepthLevel,
    DiscoveryJob,
    DiscoveryQuery,
    GeoFilter,
    ICP,
    JobStatus,
    ScoredLead,
)
from app.intelligence.v2.orchestrator import run_full_pipeline

logger = logging.getLogger(__name__)

# ─────────────────────────── In-Memory Job Store ─────────────────────────────

_JOBS: Dict[str, DiscoveryJob] = {}

# ─────────────────────────── Router ──────────────────────────────────────────

router = APIRouter(prefix="/api/v2/intelligence", tags=["Intelligence V2"])

# ─────────────────────────── Request/Response Models ─────────────────────────


class DiscoverRequest(BaseModel):
    """Request body for POST /discover."""

    icp: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Ideal Customer Profile — industries, geo, size, signals",
        example={
            "industries": ["restaurants"],
            "geo": {"countries": ["SA"], "cities": ["Riyadh"]},
            "signals": ["hiring"],
        }
    )
    depth: DepthLevel = DepthLevel.STANDARD
    limit: int = Field(50, ge=1, le=500)
    sources: Optional[List[str]] = None
    language: str = "ar"


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: float
    leads_found: int
    leads_scored: int
    sources_completed: List[str]
    sources_total: int
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    error: Optional[str]


class LeadSummary(BaseModel):
    """Compact lead representation for list responses."""

    id: str
    company_name: str
    company_name_ar: Optional[str]
    domain: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    city: Optional[str]
    country: str
    industry: Optional[str]
    total_score: float
    tier: Optional[str]
    is_hiring: bool
    hiring_roles: List[str]
    has_website: bool
    linkedin_url: Optional[str]
    talking_points_ar: List[str]
    sources: List[str]
    is_mock: bool


def _job_to_status(job: DiscoveryJob) -> JobStatusResponse:
    return JobStatusResponse(
        job_id=job.id,
        status=job.status.value,
        progress=job.progress,
        leads_found=job.leads_found,
        leads_scored=job.leads_scored,
        sources_completed=job.sources_completed,
        sources_total=job.sources_total,
        created_at=job.created_at.isoformat(),
        started_at=job.started_at.isoformat() if job.started_at else None,
        completed_at=job.completed_at.isoformat() if job.completed_at else None,
        error=job.error,
    )


def _scored_to_summary(lead: ScoredLead) -> LeadSummary:
    el = lead.enriched_lead
    nl = el.normalized_lead
    sources = [p.source_name for p in nl.provenances]
    is_mock = any(p.is_mock for p in nl.provenances)

    return LeadSummary(
        id=lead.id,
        company_name=nl.company_name,
        company_name_ar=nl.company_name_ar,
        domain=nl.domain,
        phone=nl.phone_e164,
        email=nl.email or (el.discovered_emails[0] if el.discovered_emails else None),
        city=nl.city,
        country=nl.country,
        industry=nl.industry,
        total_score=lead.total_score,
        tier=lead.tier.value if lead.tier else None,
        is_hiring=nl.is_hiring,
        hiring_roles=nl.hiring_roles,
        has_website=el.has_website,
        linkedin_url=el.linkedin_url or nl.linkedin_url,
        talking_points_ar=lead.talking_points_ar[:3],
        sources=list(set(sources)),
        is_mock=is_mock,
    )


def _parse_icp(raw: Dict[str, Any]) -> ICP:
    """Parse raw ICP dict into ICP model."""
    geo_raw = raw.get("geo", {})
    geo = GeoFilter(
        countries=geo_raw.get("countries", ["SA"]),
        cities=geo_raw.get("cities", []),
    )
    return ICP(
        industries=raw.get("industries", []),
        geo=geo,
        company_size=raw.get("company_size"),
        min_employees=raw.get("min_employees"),
        max_employees=raw.get("max_employees"),
        roles=raw.get("roles", []),
        signals=raw.get("signals", []),
        keywords=raw.get("keywords", []),
        keywords_ar=raw.get("keywords_ar", []),
    )


# ─────────────────────────── Background Task ─────────────────────────────────

async def _run_job(job: DiscoveryJob):
    """Background task: run the full pipeline and update job state."""
    try:
        await run_full_pipeline(job.query, job)
    except Exception as e:
        logger.error(f"[api] Job {job.id} background task failed: {e}", exc_info=True)
        job.status = JobStatus.FAILED
        job.error = str(e)
        job.completed_at = datetime.utcnow()


# ─────────────────────────── Endpoints ───────────────────────────────────────

@router.post("/discover", summary="Start a lead discovery job")
async def start_discovery(
    request: DiscoverRequest,
    background_tasks: BackgroundTasks,
):
    """
    Start a new lead discovery job.
    Returns a job_id to poll for status and results.

    Example:
    ```bash
    curl -X POST localhost:8001/api/v2/intelligence/discover \\
      -H "Content-Type: application/json" \\
      -d '{"icp":{"industries":["restaurants"],"geo":{"countries":["SA"],"cities":["Riyadh"]}},"depth":"quick","limit":5}'
    ```
    """
    icp = _parse_icp(request.icp or {})

    query = DiscoveryQuery(
        icp=icp,
        depth=request.depth,
        limit=request.limit,
        sources=request.sources,
        language=request.language,
    )

    job = DiscoveryJob(query=query)
    _JOBS[job.id] = job

    # Start background task
    background_tasks.add_task(_run_job, job)

    logger.info(f"[api] Started discovery job {job.id} — depth={request.depth.value} limit={request.limit}")

    return {
        "job_id": job.id,
        "status": job.status.value,
        "message": "Discovery job started",
        "poll_url": f"/api/v2/intelligence/jobs/{job.id}",
        "leads_url": f"/api/v2/intelligence/jobs/{job.id}/leads",
        "stream_url": f"/api/v2/intelligence/jobs/{job.id}/stream",
    }


@router.get("/jobs/{job_id}", response_model=JobStatusResponse, summary="Get job status")
async def get_job_status(job_id: str):
    """Get the current status and progress of a discovery job."""
    job = _JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return _job_to_status(job)


@router.get("/jobs/{job_id}/leads", summary="Get discovered leads (paginated)")
async def get_job_leads(
    job_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    min_score: float = Query(0.0, ge=0, le=100),
    tier: Optional[str] = Query(None, description="hot|warm|cool|cold"),
):
    """
    Get leads from a completed or in-progress job.
    Results are paginated and filterable by score/tier.
    """
    job = _JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    leads = job.scored_leads

    # Filter
    if min_score > 0:
        leads = [l for l in leads if l.total_score >= min_score]
    if tier:
        leads = [l for l in leads if l.tier and l.tier.value == tier]

    # Paginate
    total = len(leads)
    start = (page - 1) * page_size
    end = start + page_size
    page_leads = leads[start:end]

    return {
        "job_id": job_id,
        "status": job.status.value,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size if total > 0 else 0,
        "leads": [_scored_to_summary(l).model_dump() for l in page_leads],
    }


@router.post("/jobs/{job_id}/export", summary="Export leads as CSV or JSON")
async def export_leads(
    job_id: str,
    format: str = Query("csv", description="csv or json"),
):
    """Export all leads from a completed job."""
    job = _JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    if job.status not in (JobStatus.COMPLETED, JobStatus.RUNNING):
        raise HTTPException(
            status_code=400,
            detail=f"Job is {job.status.value} — leads not yet available"
        )

    leads = [_scored_to_summary(l) for l in job.scored_leads]

    if format == "json":
        content = json.dumps([l.model_dump() for l in leads], ensure_ascii=False, indent=2)
        return StreamingResponse(
            io.StringIO(content),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=leads_{job_id}.json"},
        )
    else:
        # CSV
        output = io.StringIO()
        if leads:
            fieldnames = list(leads[0].model_dump().keys())
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for lead in leads:
                row = lead.model_dump()
                # Flatten lists to strings for CSV
                for k, v in row.items():
                    if isinstance(v, list):
                        row[k] = "; ".join(str(i) for i in v)
                writer.writerow(row)

        output.seek(0)
        return StreamingResponse(
            output,
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename=leads_{job_id}.csv"},
        )


@router.websocket("/jobs/{job_id}/stream")
async def stream_leads(websocket: WebSocket, job_id: str):
    """
    WebSocket: stream leads in real-time as they're discovered.
    Sends JSON messages: {"type": "lead", "data": {...}} or {"type": "done"}
    """
    await websocket.accept()

    job = _JOBS.get(job_id)
    if not job:
        await websocket.send_json({"type": "error", "message": f"Job {job_id} not found"})
        await websocket.close()
        return

    try:
        sent_lead_ids: set[str] = set()
        poll_interval = 0.5  # seconds

        while True:
            # Send any new leads
            for lead in job.scored_leads:
                if lead.id not in sent_lead_ids:
                    sent_lead_ids.add(lead.id)
                    await websocket.send_json({
                        "type": "lead",
                        "data": _scored_to_summary(lead).model_dump(),
                    })

            # Send status update
            await websocket.send_json({
                "type": "status",
                "status": job.status.value,
                "progress": job.progress,
                "leads_found": job.leads_found,
            })

            if job.status in (JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED):
                await websocket.send_json({"type": "done", "status": job.status.value})
                break

            await asyncio.sleep(poll_interval)

    except WebSocketDisconnect:
        logger.info(f"[api] WebSocket disconnected for job {job_id}")
    except Exception as e:
        logger.error(f"[api] WebSocket error for job {job_id}: {e}")
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass


@router.get("/sources", summary="List available source adapters")
async def list_sources():
    """List all available source adapters with their status."""
    from app.intelligence.v2.orchestrator import SOURCE_REGISTRY
    import os

    source_status = []
    for name, cls in SOURCE_REGISTRY.items():
        instance = cls()
        source_status.append({
            "name": name,
            "requires_key": cls.REQUIRES_KEY,
            "available": instance.is_available,
            "rate_limit_cps": cls.RATE_LIMIT_CPS,
        })

    return {"sources": source_status}


@router.get("/jobs", summary="List all active jobs")
async def list_jobs():
    """List all jobs (for debugging)."""
    return {
        "jobs": [
            {
                "job_id": job.id,
                "status": job.status.value,
                "progress": job.progress,
                "leads_scored": job.leads_scored,
                "created_at": job.created_at.isoformat(),
            }
            for job in _JOBS.values()
        ]
    }
