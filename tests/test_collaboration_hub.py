"""Regression tests for the tenant-scoped Dealix Collaboration OS."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from api.routers import ops_collaboration
from dealix.company_intelligence.collaboration_contracts import (
    CollaborationActorType,
    CollaborationEventKind,
)
from intelligence.collaboration_hub import (
    CollaborationConflictError,
    CollaborationHub,
    CollaborationRelationError,
)
from intelligence.communication_storage import (
    FileCommunicationStorage,
    PostgresCommunicationStorage,
)


def _hub(tmp_path: Path) -> CollaborationHub:
    return CollaborationHub(FileCommunicationStorage(tmp_path / "comms"))


def _channel(hub: CollaborationHub, tenant: str = "tenant-a", channel: str = "ops"):
    return hub.create_event(
        tenant_id=tenant,
        deduplication_key=f"channel:{channel}",
        kind=CollaborationEventKind.CHANNEL_CREATED,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        source_id="test",
        channel_id=channel,
        content=f"Channel {channel}",
        metadata={"visibility": "private"},
    )


def _register_agent(hub: CollaborationHub, tenant: str, agent_id: str = "agent-sales"):
    return hub.create_event(
        tenant_id=tenant,
        deduplication_key=f"agent:{agent_id}:v1",
        kind=CollaborationEventKind.AGENT_REGISTERED,
        actor_id="system",
        actor_type=CollaborationActorType.SYSTEM,
        target_actor_id=agent_id,
        source_id="test",
        content="Sales Agent",
        metadata={
            "agent_id": agent_id,
            "capabilities": ["research", "draft"],
            "max_concurrency": 2,
        },
        attention_for=(agent_id,),
    )


def test_append_is_idempotent_and_conflicts_fail_closed(tmp_path: Path) -> None:
    hub = _hub(tmp_path)
    first = _channel(hub)
    retry = _channel(hub)

    assert first.event_id == retry.event_id
    assert hub.stats(tenant_id="tenant-a")["event_count"] == 1

    with pytest.raises(CollaborationConflictError):
        hub.create_event(
            tenant_id="tenant-a",
            deduplication_key="channel:ops",
            kind=CollaborationEventKind.CHANNEL_CREATED,
            actor_id="founder",
            actor_type=CollaborationActorType.HUMAN,
            source_id="test",
            channel_id="ops",
            content="Different semantic content",
            metadata={"visibility": "private"},
        )


def test_tenant_isolation_and_cross_tenant_thread_reference_fail_closed(
    tmp_path: Path,
) -> None:
    hub = _hub(tmp_path)
    _channel(hub, "tenant-a", "ops")
    _channel(hub, "tenant-b", "ops")
    root = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="tenant-a:message:1",
        kind=CollaborationEventKind.MESSAGE,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        source_id="test",
        channel_id="ops",
        content="Tenant A only",
    )

    assert hub.search(tenant_id="tenant-a", query="Tenant A only")
    assert hub.search(tenant_id="tenant-b", query="Tenant A only") == []
    assert hub.get_event(tenant_id="tenant-b", event_id=root.event_id) is None

    with pytest.raises(CollaborationRelationError):
        hub.create_event(
            tenant_id="tenant-b",
            deduplication_key="tenant-b:reply:cross",
            kind=CollaborationEventKind.THREAD_REPLY,
            actor_id="other",
            actor_type=CollaborationActorType.HUMAN,
            source_id="test",
            channel_id="ops",
            parent_event_id=root.event_id,
            content="Must not cross tenants",
        )


def test_threads_reactions_attachments_canvas_and_media_relations(tmp_path: Path) -> None:
    hub = _hub(tmp_path)
    _channel(hub)
    root = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="message:root",
        kind=CollaborationEventKind.MESSAGE,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        source_id="test",
        channel_id="ops",
        content="Release plan",
        attention_for=("agent-eng",),
    )
    reply = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="message:reply",
        kind=CollaborationEventKind.THREAD_REPLY,
        actor_id="agent-eng",
        actor_type=CollaborationActorType.AGENT,
        source_id="test",
        parent_event_id=root.event_id,
        content="Patch prepared",
    )
    reaction = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="reaction:reply:+1",
        kind=CollaborationEventKind.REACTION,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        source_id="test",
        parent_event_id=reply.event_id,
        content="+1",
    )
    attachment = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="attachment:1",
        kind=CollaborationEventKind.ATTACHMENT,
        actor_id="agent-eng",
        actor_type=CollaborationActorType.AGENT,
        source_id="test",
        channel_id="ops",
        content="Build artifact metadata",
        metadata={"asset_id": "artifact-1", "media_type": "application/zip"},
    )
    annotation = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="annotation:1",
        kind=CollaborationEventKind.MEDIA_ANNOTATION,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        source_id="test",
        parent_event_id=attachment.event_id,
        content="Review this frame",
        metadata={"offset_ms": 1500},
    )
    canvas = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="canvas:plan:v1",
        kind=CollaborationEventKind.CANVAS_UPDATE,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        source_id="test",
        channel_id="ops",
        content="Plan updated",
        metadata={"canvas_id": "plan", "revision": 1},
    )

    thread_ids = [event.event_id for event in hub.thread(tenant_id="tenant-a", root_event_id=root.event_id)]
    assert root.event_id in thread_ids
    assert reply.event_id in thread_ids
    assert reaction.event_id in thread_ids
    assert annotation.root_event_id == attachment.event_id
    assert canvas.metadata["canvas_id"] == "plan"


def test_agent_registration_job_inbox_and_status_are_relation_safe(tmp_path: Path) -> None:
    hub = _hub(tmp_path)
    _register_agent(hub, "tenant-a", "agent-sales")

    job = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="job:qualified-account:1",
        kind=CollaborationEventKind.AGENT_JOB_REQUESTED,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        target_actor_id="agent-sales",
        source_id="test",
        content="Research the qualified account and prepare a draft only",
        metadata={"priority": "high", "execution_authorized": False},
        attention_for=("agent-sales",),
    )
    status = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="job:qualified-account:1:status:prepared",
        kind=CollaborationEventKind.AGENT_JOB_STATUS,
        actor_id="agent-sales",
        actor_type=CollaborationActorType.AGENT,
        target_actor_id="agent-sales",
        source_id="test",
        content="Draft prepared for approval",
        metadata={"job_event_id": job.event_id, "status": "prepared"},
    )

    inbox_ids = [event.event_id for event in hub.agent_inbox(tenant_id="tenant-a", agent_id="agent-sales")]
    assert job.event_id in inbox_ids
    assert status.event_id in inbox_ids
    assert all(not event.execution_allowed for event in hub.agent_inbox(tenant_id="tenant-a", agent_id="agent-sales"))

    with pytest.raises(CollaborationRelationError):
        hub.create_event(
            tenant_id="tenant-a",
            deduplication_key="job:unknown-agent",
            kind=CollaborationEventKind.AGENT_JOB_REQUESTED,
            actor_id="founder",
            actor_type=CollaborationActorType.HUMAN,
            target_actor_id="agent-unknown",
            source_id="test",
            content="Should fail closed",
        )


def test_git_workflow_presence_typing_and_huddle_events_are_internal_only(
    tmp_path: Path,
) -> None:
    hub = _hub(tmp_path)
    _channel(hub)
    git_event = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="git:dealix:sha1",
        kind=CollaborationEventKind.GIT_EVENT,
        actor_id="github",
        actor_type=CollaborationActorType.SYSTEM,
        source_id="github",
        content="CI completed",
        metadata={"repository": "Dealix-sa/dealix", "event_type": "status", "sha": "sha1"},
    )
    workflow = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="workflow:release:run1",
        kind=CollaborationEventKind.WORKFLOW_EVENT,
        actor_id="workflow-engine",
        actor_type=CollaborationActorType.WORKFLOW,
        source_id="dealix",
        content="Approval required",
        metadata={"workflow_id": "release", "event_type": "awaiting_approval"},
        attention_for=("founder",),
    )
    presence = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="presence:founder:1",
        kind=CollaborationEventKind.PRESENCE,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        source_id="test",
        channel_id="ops",
        content="online",
    )
    typing = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="typing:founder:1",
        kind=CollaborationEventKind.TYPING,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        source_id="test",
        channel_id="ops",
        content="typing",
    )
    huddle = hub.create_event(
        tenant_id="tenant-a",
        deduplication_key="huddle:ops:1",
        kind=CollaborationEventKind.HUDDLE_EVENT,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        source_id="test",
        channel_id="ops",
        content="started",
        metadata={"huddle_id": "ops-1", "state": "started"},
    )

    for event in (git_event, workflow, presence, typing, huddle):
        assert event.external_effect is False
        assert event.execution_allowed is False
    assert presence.retention_class.value == "transient"
    assert typing.proof_eligible is False
    assert hub.search(tenant_id="tenant-a", query="awaiting_approval")[0].event_id == workflow.event_id


def test_postgres_storage_persists_collaboration_collection() -> None:
    engine = create_engine("sqlite:///:memory:", future=True)
    first = CollaborationHub(PostgresCommunicationStorage(engine=engine, create_tables=True))
    created = first.create_event(
        tenant_id="tenant-a",
        deduplication_key="channel:finance",
        kind=CollaborationEventKind.CHANNEL_CREATED,
        actor_id="founder",
        actor_type=CollaborationActorType.HUMAN,
        source_id="test",
        channel_id="finance",
        content="Finance channel",
    )

    second = CollaborationHub(PostgresCommunicationStorage(engine=engine, create_tables=False))
    loaded = second.get_event(tenant_id="tenant-a", event_id=created.event_id)
    assert loaded is not None
    assert loaded.content == "Finance channel"


def test_api_is_admin_gated_tenant_scoped_and_rejects_execution_authority(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", "test-admin")
    monkeypatch.setattr(ops_collaboration, "_hub", _hub(tmp_path))
    app = FastAPI()
    app.include_router(ops_collaboration.router)
    client = TestClient(app, raise_server_exceptions=False)

    assert client.get("/api/v1/ops/collaboration/readiness").status_code == 401
    headers = {"X-Admin-API-Key": "test-admin"}

    create = client.post(
        "/api/v1/ops/collaboration/events",
        headers=headers,
        json={
            "tenant_id": "tenant-a",
            "deduplication_key": "channel:exec",
            "kind": "channel_created",
            "actor_id": "founder",
            "actor_type": "human",
            "source_id": "test",
            "channel_id": "exec",
            "content": "Executive room",
        },
    )
    assert create.status_code == 200
    event_id = create.json()["event"]["event_id"]
    assert create.json()["event"]["execution_allowed"] is False

    other_tenant = client.get(
        f"/api/v1/ops/collaboration/events/{event_id}?tenant_id=tenant-b",
        headers=headers,
    )
    assert other_tenant.status_code == 404

    authority_injection = client.post(
        "/api/v1/ops/collaboration/events",
        headers=headers,
        json={
            "tenant_id": "tenant-a",
            "deduplication_key": "bad:authority",
            "kind": "message",
            "actor_id": "founder",
            "actor_type": "human",
            "source_id": "test",
            "channel_id": "exec",
            "content": "Do not allow authority injection",
            "execution_allowed": True,
        },
    )
    assert authority_injection.status_code == 422


def test_api_agent_jobs_require_registration_and_surface_inbox(
    monkeypatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", "test-admin")
    monkeypatch.setattr(ops_collaboration, "_hub", _hub(tmp_path))
    app = FastAPI()
    app.include_router(ops_collaboration.router)
    client = TestClient(app, raise_server_exceptions=False)
    headers = {"X-Admin-API-Key": "test-admin"}

    registration = client.post(
        "/api/v1/ops/collaboration/agents/register",
        headers=headers,
        json={
            "tenant_id": "tenant-a",
            "agent_id": "agent-research",
            "name": "Research Agent",
            "capabilities": ["research"],
            "max_concurrency": 1,
        },
    )
    assert registration.status_code == 200

    job = client.post(
        "/api/v1/ops/collaboration/agents/jobs",
        headers=headers,
        json={
            "tenant_id": "tenant-a",
            "deduplication_key": "job:research:1",
            "requested_by": "founder",
            "target_agent_id": "agent-research",
            "objective": "Research with sources; no external action",
        },
    )
    assert job.status_code == 200
    assert job.json()["event"]["metadata"]["execution_authorized"] is False

    inbox = client.get(
        "/api/v1/ops/collaboration/agents/agent-research/inbox?tenant_id=tenant-a",
        headers=headers,
    )
    assert inbox.status_code == 200
    assert any(event["kind"] == "agent_job_requested" for event in inbox.json()["events"])
