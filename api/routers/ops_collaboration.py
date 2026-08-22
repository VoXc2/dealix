"""Internal Collaboration OS API.

Admin-gated, tenant-scoped collaboration among people, agents, workflows, Git,
and Dealix operational surfaces. This API records internal events only. It does
not send externally and does not authorize merge, deploy, payment, or production
mutation.
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field

from api.security.api_key import require_admin_key
from dealix.company_intelligence.collaboration_contracts import (
    CollaborationActorType,
    CollaborationEventKind,
)
from intelligence.collaboration_hub import (
    CollaborationConflictError,
    CollaborationHub,
    CollaborationRelationError,
)
from intelligence.communication_storage import CommunicationStorageUnavailable

router = APIRouter(
    prefix="/api/v1/ops/collaboration",
    tags=["Collaboration OS"],
    dependencies=[Depends(require_admin_key)],
)
_hub = CollaborationHub()
logger = logging.getLogger(__name__)


class CollaborationEventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    deduplication_key: str = Field(..., min_length=1)
    kind: CollaborationEventKind
    actor_id: str = Field(..., min_length=1)
    actor_type: CollaborationActorType
    source_id: str = Field(..., min_length=1)
    target_actor_id: str = ""
    channel_id: str = ""
    conversation_id: str = ""
    parent_event_id: str = ""
    content: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    attention_for: list[str] = Field(default_factory=list)


class AgentRegistrationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    agent_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    capabilities: list[str] = Field(default_factory=list)
    max_concurrency: int = Field(default=1, ge=1, le=128)
    channel_ids: list[str] = Field(default_factory=list)
    version: str = "1"
    actor_id: str = Field(default="system", min_length=1)
    source_id: str = Field(default="collaboration_api", min_length=1)


class AgentJobRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    deduplication_key: str = Field(..., min_length=1)
    requested_by: str = Field(..., min_length=1)
    target_agent_id: str = Field(..., min_length=1)
    objective: str = Field(..., min_length=1)
    channel_id: str = ""
    priority: str = "normal"
    capability: str = ""
    source_id: str = Field(default="collaboration_api", min_length=1)


class AgentJobStatusRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., min_length=1)
    deduplication_key: str = Field(..., min_length=1)
    agent_id: str = Field(..., min_length=1)
    job_event_id: str = Field(..., min_length=1)
    status: str = Field(..., min_length=1)
    summary: str = ""
    channel_id: str = ""
    source_id: str = Field(default="collaboration_api", min_length=1)


def _raise_storage_unavailable(exc: CommunicationStorageUnavailable) -> None:
    raise HTTPException(
        status_code=503,
        detail={
            "code": "collaboration_storage_unavailable",
            "message": "Collaboration OS durable storage is unavailable; writes fail closed.",
        },
    ) from exc


def _raise_safe_rejection(exc: Exception, operation: str) -> None:
    logger.warning(
        "collaboration_operation_rejected operation=%s error_type=%s",
        operation,
        type(exc).__name__,
    )
    raise HTTPException(
        status_code=400,
        detail={
            "code": "collaboration_operation_rejected",
            "message": "The collaboration operation could not be completed safely.",
        },
    ) from exc


def _event_dict(event: Any) -> dict[str, Any]:
    return event.model_dump(mode="json")


@router.get("/readiness")
async def collaboration_readiness() -> dict[str, Any]:
    return {
        **_hub.storage_readiness(),
        "external_execution_allowed": False,
        "source_of_truth": "dealix",
    }


@router.post("/events")
async def create_collaboration_event(payload: CollaborationEventRequest) -> dict[str, Any]:
    try:
        event = _hub.create_event(
            tenant_id=payload.tenant_id,
            deduplication_key=payload.deduplication_key,
            kind=payload.kind,
            actor_id=payload.actor_id,
            actor_type=payload.actor_type,
            source_id=payload.source_id,
            target_actor_id=payload.target_actor_id,
            channel_id=payload.channel_id,
            conversation_id=payload.conversation_id,
            parent_event_id=payload.parent_event_id,
            content=payload.content,
            metadata=payload.metadata,
            attention_for=tuple(payload.attention_for),
            proof_eligible=False,
        )
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    except (CollaborationConflictError, CollaborationRelationError, ValueError) as exc:
        _raise_safe_rejection(exc, "create_event")
    return {"event": _event_dict(event)}


@router.post("/agents/register")
async def register_agent(payload: AgentRegistrationRequest) -> dict[str, Any]:
    try:
        event = _hub.create_event(
            tenant_id=payload.tenant_id,
            deduplication_key=f"agent:{payload.agent_id}:registration:{payload.version}",
            kind=CollaborationEventKind.AGENT_REGISTERED,
            actor_id=payload.actor_id,
            actor_type=CollaborationActorType.SYSTEM,
            source_id=payload.source_id,
            target_actor_id=payload.agent_id,
            content=payload.name,
            metadata={
                "agent_id": payload.agent_id,
                "name": payload.name,
                "capabilities": payload.capabilities,
                "max_concurrency": payload.max_concurrency,
                "channel_ids": payload.channel_ids,
                "version": payload.version,
            },
            attention_for=(payload.agent_id,),
        )
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    except (CollaborationConflictError, CollaborationRelationError, ValueError) as exc:
        _raise_safe_rejection(exc, "register_agent")
    return {"event": _event_dict(event)}


@router.post("/agents/jobs")
async def request_agent_job(payload: AgentJobRequest) -> dict[str, Any]:
    try:
        event = _hub.create_event(
            tenant_id=payload.tenant_id,
            deduplication_key=payload.deduplication_key,
            kind=CollaborationEventKind.AGENT_JOB_REQUESTED,
            actor_id=payload.requested_by,
            actor_type=CollaborationActorType.HUMAN,
            source_id=payload.source_id,
            target_actor_id=payload.target_agent_id,
            channel_id=payload.channel_id,
            content=payload.objective,
            metadata={
                "priority": payload.priority,
                "capability": payload.capability,
                "execution_authorized": False,
            },
            attention_for=(payload.target_agent_id,),
        )
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    except (CollaborationConflictError, CollaborationRelationError, ValueError) as exc:
        _raise_safe_rejection(exc, "request_agent_job")
    return {"event": _event_dict(event)}


@router.post("/agents/jobs/status")
async def update_agent_job_status(payload: AgentJobStatusRequest) -> dict[str, Any]:
    try:
        event = _hub.create_event(
            tenant_id=payload.tenant_id,
            deduplication_key=payload.deduplication_key,
            kind=CollaborationEventKind.AGENT_JOB_STATUS,
            actor_id=payload.agent_id,
            actor_type=CollaborationActorType.AGENT,
            source_id=payload.source_id,
            target_actor_id=payload.agent_id,
            channel_id=payload.channel_id,
            content=payload.summary or payload.status,
            metadata={
                "job_event_id": payload.job_event_id,
                "status": payload.status,
                "execution_authorized": False,
            },
        )
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    except (CollaborationConflictError, CollaborationRelationError, ValueError) as exc:
        _raise_safe_rejection(exc, "update_agent_job_status")
    return {"event": _event_dict(event)}


@router.get("/events/{event_id}")
async def get_collaboration_event(
    event_id: str,
    tenant_id: str = Query(..., min_length=1),
) -> dict[str, Any]:
    try:
        event = _hub.get_event(tenant_id=tenant_id, event_id=event_id)
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    if event is None:
        raise HTTPException(status_code=404, detail="Collaboration event not found")
    return {"event": _event_dict(event)}


@router.get("/channels")
async def list_collaboration_channels(
    tenant_id: str = Query(..., min_length=1),
) -> dict[str, Any]:
    try:
        channels = _hub.list_channels(tenant_id=tenant_id)
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {"tenant_id": tenant_id, "count": len(channels), "channels": channels}


@router.get("/channels/{channel_id}")
async def channel_timeline(
    channel_id: str,
    tenant_id: str = Query(..., min_length=1),
    limit: int = Query(default=100, ge=1, le=500),
) -> dict[str, Any]:
    try:
        events = _hub.list_channel(
            tenant_id=tenant_id,
            channel_id=channel_id,
            limit=limit,
        )
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {"tenant_id": tenant_id, "channel_id": channel_id, "events": [_event_dict(e) for e in events]}


@router.get("/threads/{root_event_id}")
async def collaboration_thread(
    root_event_id: str,
    tenant_id: str = Query(..., min_length=1),
    limit: int = Query(default=500, ge=1, le=500),
) -> dict[str, Any]:
    try:
        events = _hub.thread(
            tenant_id=tenant_id,
            root_event_id=root_event_id,
            limit=limit,
        )
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {"tenant_id": tenant_id, "root_event_id": root_event_id, "events": [_event_dict(e) for e in events]}


@router.get("/search")
async def search_collaboration(
    tenant_id: str = Query(..., min_length=1),
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
) -> dict[str, Any]:
    try:
        events = _hub.search(tenant_id=tenant_id, query=q, limit=limit)
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {"tenant_id": tenant_id, "query": q, "events": [_event_dict(e) for e in events]}


@router.get("/attention/{actor_id}")
async def collaboration_attention_feed(
    actor_id: str,
    tenant_id: str = Query(..., min_length=1),
    limit: int = Query(default=50, ge=1, le=100),
) -> dict[str, Any]:
    try:
        events = _hub.attention_feed(
            tenant_id=tenant_id,
            actor_id=actor_id,
            limit=limit,
        )
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {"tenant_id": tenant_id, "actor_id": actor_id, "events": [_event_dict(e) for e in events]}


@router.get("/agents/{agent_id}/inbox")
async def agent_inbox(
    agent_id: str,
    tenant_id: str = Query(..., min_length=1),
    limit: int = Query(default=50, ge=1, le=100),
) -> dict[str, Any]:
    try:
        events = _hub.agent_inbox(
            tenant_id=tenant_id,
            agent_id=agent_id,
            limit=limit,
        )
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
    return {"tenant_id": tenant_id, "agent_id": agent_id, "events": [_event_dict(e) for e in events]}


@router.get("/stats")
async def collaboration_stats(
    tenant_id: str = Query(..., min_length=1),
) -> dict[str, Any]:
    try:
        return _hub.stats(tenant_id=tenant_id)
    except CommunicationStorageUnavailable as exc:
        _raise_storage_unavailable(exc)
