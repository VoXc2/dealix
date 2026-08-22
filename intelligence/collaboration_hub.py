"""Tenant-scoped internal collaboration hub for Dealix.

The hub extends the existing Communication OS durable storage rather than
introducing a second relay, workflow engine, approval system, or source of truth.
It records collaboration among humans, agents, systems, workflows, repositories,
and canvases as immutable events.

No method sends externally or grants execution authority. External communication
continues to flow through Dealix Draft -> Approval -> controlled execution.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any

from dealix.company_intelligence.collaboration_contracts import (
    CanonicalCollaborationEvent,
    CollaborationActorType,
    CollaborationEventKind,
    build_collaboration_event,
)
from intelligence.communication_storage import (
    CommunicationStorage,
    get_communication_storage,
)


class CollaborationConflictError(ValueError):
    """A deterministic event ID was reused with different semantic content."""


class CollaborationRelationError(ValueError):
    """A relation is missing, invalid, or crosses the tenant boundary."""


class CollaborationHub:
    """Append-only collaboration service backed by Communication OS storage."""

    def __init__(self, storage: CommunicationStorage | None = None) -> None:
        self._storage = storage or get_communication_storage()

    def storage_readiness(self) -> dict[str, Any]:
        return self._storage.readiness()

    @staticmethod
    def _event_to_dict(event: CanonicalCollaborationEvent) -> dict[str, Any]:
        return event.model_dump(mode="json")

    @staticmethod
    def _event_from_dict(raw: dict[str, Any]) -> CanonicalCollaborationEvent:
        return CanonicalCollaborationEvent.model_validate(raw)

    @staticmethod
    def _tenant_events(
        rows: Iterable[dict[str, Any]],
        tenant_id: str,
    ) -> list[CanonicalCollaborationEvent]:
        return [
            CanonicalCollaborationEvent.model_validate(raw)
            for raw in rows
            if raw.get("tenant_id") == tenant_id
        ]

    @staticmethod
    def _find_raw(
        rows: list[dict[str, Any]],
        *,
        tenant_id: str,
        event_id: str,
    ) -> dict[str, Any] | None:
        for raw in rows:
            if raw.get("tenant_id") == tenant_id and raw.get("event_id") == event_id:
                return raw
        return None

    @staticmethod
    def _registered_agent_exists(
        rows: list[dict[str, Any]],
        *,
        tenant_id: str,
        agent_id: str,
    ) -> bool:
        for raw in rows:
            if raw.get("tenant_id") != tenant_id:
                continue
            if raw.get("kind") != CollaborationEventKind.AGENT_REGISTERED.value:
                continue
            metadata = raw.get("metadata") or {}
            if raw.get("target_actor_id") == agent_id or metadata.get("agent_id") == agent_id:
                return True
        return False

    @staticmethod
    def _validate_relation(
        rows: list[dict[str, Any]],
        event: CanonicalCollaborationEvent,
    ) -> None:
        if event.parent_event_id:
            parent_raw = CollaborationHub._find_raw(
                rows,
                tenant_id=event.tenant_id,
                event_id=event.parent_event_id,
            )
            if parent_raw is None:
                # Do not reveal whether a similarly named event exists in another tenant.
                raise CollaborationRelationError("parent event is unavailable in this tenant")
            parent = CollaborationHub._event_from_dict(parent_raw)
            if event.channel_id and parent.channel_id and event.channel_id != parent.channel_id:
                raise CollaborationRelationError("parent event belongs to a different channel")

        if event.kind == CollaborationEventKind.AGENT_JOB_REQUESTED:
            if not CollaborationHub._registered_agent_exists(
                rows,
                tenant_id=event.tenant_id,
                agent_id=event.target_actor_id,
            ):
                raise CollaborationRelationError("target agent is not registered in this tenant")

        if event.kind == CollaborationEventKind.AGENT_JOB_STATUS:
            job_event_id = str(event.metadata.get("job_event_id", ""))
            job_raw = CollaborationHub._find_raw(
                rows,
                tenant_id=event.tenant_id,
                event_id=job_event_id,
            )
            if job_raw is None:
                raise CollaborationRelationError("job event is unavailable in this tenant")
            job = CollaborationHub._event_from_dict(job_raw)
            if job.kind != CollaborationEventKind.AGENT_JOB_REQUESTED:
                raise CollaborationRelationError("job_event_id does not reference a job request")
            if job.target_actor_id != event.target_actor_id:
                raise CollaborationRelationError("job status actor does not own the referenced job")

    def append_event(
        self,
        event: CanonicalCollaborationEvent,
    ) -> CanonicalCollaborationEvent:
        """Append one event atomically and idempotently.

        A retry with the same deterministic ID and semantic payload returns the
        existing event. Reusing the deduplication key for different content fails
        closed, preventing silent event mutation.
        """

        if event.external_effect or event.execution_allowed:
            raise ValueError("collaboration events cannot authorize execution")

        def _append(rows: list[dict[str, Any]]) -> CanonicalCollaborationEvent:
            existing_raw = self._find_raw(
                rows,
                tenant_id=event.tenant_id,
                event_id=event.event_id,
            )
            if existing_raw is not None:
                existing = self._event_from_dict(existing_raw)
                if existing.content_hash != event.content_hash:
                    raise CollaborationConflictError(
                        "deduplication key already belongs to different content"
                    )
                return existing

            self._validate_relation(rows, event)
            rows.append(self._event_to_dict(event))
            return event

        return self._storage.mutate("collaboration_events", _append)

    def create_event(
        self,
        *,
        tenant_id: str,
        deduplication_key: str,
        kind: CollaborationEventKind,
        actor_id: str,
        actor_type: CollaborationActorType,
        source_id: str,
        target_actor_id: str = "",
        channel_id: str = "",
        conversation_id: str = "",
        parent_event_id: str = "",
        content: str = "",
        metadata: dict[str, Any] | None = None,
        attention_for: tuple[str, ...] = (),
        proof_eligible: bool = False,
    ) -> CanonicalCollaborationEvent:
        """Build and append an event, resolving thread roots safely."""

        root_event_id = ""
        resolved_channel_id = channel_id
        if parent_event_id:
            parent = self.get_event(tenant_id=tenant_id, event_id=parent_event_id)
            if parent is None:
                raise CollaborationRelationError("parent event is unavailable in this tenant")
            root_event_id = parent.root_event_id or parent.event_id
            if not resolved_channel_id:
                resolved_channel_id = parent.channel_id
            elif parent.channel_id and parent.channel_id != resolved_channel_id:
                raise CollaborationRelationError("parent event belongs to a different channel")

        event = build_collaboration_event(
            tenant_id=tenant_id,
            deduplication_key=deduplication_key,
            kind=kind,
            actor_id=actor_id,
            actor_type=actor_type,
            source_id=source_id,
            target_actor_id=target_actor_id,
            channel_id=resolved_channel_id,
            conversation_id=conversation_id,
            parent_event_id=parent_event_id,
            root_event_id=root_event_id,
            content=content,
            metadata=metadata,
            attention_for=attention_for,
            proof_eligible=proof_eligible,
        )
        return self.append_event(event)

    def get_event(
        self,
        *,
        tenant_id: str,
        event_id: str,
    ) -> CanonicalCollaborationEvent | None:
        rows = self._storage.read("collaboration_events")
        raw = self._find_raw(rows, tenant_id=tenant_id, event_id=event_id)
        return None if raw is None else self._event_from_dict(raw)

    def list_channel(
        self,
        *,
        tenant_id: str,
        channel_id: str,
        limit: int = 100,
    ) -> list[CanonicalCollaborationEvent]:
        limit = max(1, min(limit, 500))
        events = [
            event
            for event in self._tenant_events(
                self._storage.read("collaboration_events"), tenant_id
            )
            if event.channel_id == channel_id
        ]
        events.sort(key=lambda event: event.created_at)
        return events[-limit:]

    def list_channels(self, *, tenant_id: str) -> list[dict[str, Any]]:
        """Return channel/DM creation records with simple activity counts."""

        events = self._tenant_events(
            self._storage.read("collaboration_events"), tenant_id
        )
        activity: dict[str, int] = {}
        creation: dict[str, CanonicalCollaborationEvent] = {}
        for event in events:
            if event.channel_id:
                activity[event.channel_id] = activity.get(event.channel_id, 0) + 1
            if event.kind in {
                CollaborationEventKind.CHANNEL_CREATED,
                CollaborationEventKind.DM_CREATED,
            }:
                creation.setdefault(event.channel_id, event)

        result: list[dict[str, Any]] = []
        for channel_id, event in creation.items():
            result.append(
                {
                    "channel_id": channel_id,
                    "kind": event.kind.value,
                    "content": event.content,
                    "metadata": event.metadata,
                    "created_at": event.created_at.isoformat(),
                    "event_count": activity.get(channel_id, 0),
                }
            )
        result.sort(key=lambda item: item["created_at"])
        return result

    def thread(
        self,
        *,
        tenant_id: str,
        root_event_id: str,
        limit: int = 500,
    ) -> list[CanonicalCollaborationEvent]:
        root = self.get_event(tenant_id=tenant_id, event_id=root_event_id)
        if root is None:
            return []
        resolved_root = root.root_event_id or root.event_id
        events = self._tenant_events(
            self._storage.read("collaboration_events"), tenant_id
        )
        matches = [
            event
            for event in events
            if event.event_id == resolved_root or event.root_event_id == resolved_root
        ]
        matches.sort(key=lambda event: event.created_at)
        return matches[: max(1, min(limit, 500))]

    def search(
        self,
        *,
        tenant_id: str,
        query: str,
        limit: int = 20,
    ) -> list[CanonicalCollaborationEvent]:
        """Tenant-scoped text search over event content and non-secret metadata."""

        needle = query.strip().casefold()
        if not needle:
            return []
        matches: list[CanonicalCollaborationEvent] = []
        for event in self._tenant_events(
            self._storage.read("collaboration_events"), tenant_id
        ):
            searchable = " ".join(
                [
                    event.kind.value,
                    event.actor_id,
                    event.target_actor_id,
                    event.channel_id,
                    event.content,
                    json.dumps(event.metadata, ensure_ascii=False, sort_keys=True),
                ]
            ).casefold()
            if needle in searchable:
                matches.append(event)
        matches.sort(key=lambda event: event.created_at, reverse=True)
        return matches[: max(1, min(limit, 100))]

    def attention_feed(
        self,
        *,
        tenant_id: str,
        actor_id: str,
        limit: int = 50,
    ) -> list[CanonicalCollaborationEvent]:
        """Return mentions, assignments, and jobs that need one actor's attention."""

        matches = [
            event
            for event in self._tenant_events(
                self._storage.read("collaboration_events"), tenant_id
            )
            if actor_id in event.attention_for or event.target_actor_id == actor_id
        ]
        matches.sort(key=lambda event: event.created_at, reverse=True)
        return matches[: max(1, min(limit, 100))]

    def agent_inbox(
        self,
        *,
        tenant_id: str,
        agent_id: str,
        limit: int = 50,
    ) -> list[CanonicalCollaborationEvent]:
        """Return job and attention events targeted at a specific agent."""

        allowed = {
            CollaborationEventKind.AGENT_JOB_REQUESTED,
            CollaborationEventKind.AGENT_JOB_STATUS,
            CollaborationEventKind.MESSAGE,
            CollaborationEventKind.THREAD_REPLY,
            CollaborationEventKind.WORKFLOW_EVENT,
        }
        return [
            event
            for event in self.attention_feed(
                tenant_id=tenant_id, actor_id=agent_id, limit=limit
            )
            if event.kind in allowed
        ]

    def stats(self, *, tenant_id: str) -> dict[str, Any]:
        events = self._tenant_events(
            self._storage.read("collaboration_events"), tenant_id
        )
        by_kind: dict[str, int] = {}
        actors: set[str] = set()
        channels: set[str] = set()
        for event in events:
            by_kind[event.kind.value] = by_kind.get(event.kind.value, 0) + 1
            actors.add(event.actor_id)
            if event.channel_id:
                channels.add(event.channel_id)
        return {
            "tenant_id": tenant_id,
            "event_count": len(events),
            "actor_count": len(actors),
            "channel_count": len(channels),
            "by_kind": dict(sorted(by_kind.items())),
            "external_execution_allowed": False,
        }


__all__ = [
    "CollaborationConflictError",
    "CollaborationHub",
    "CollaborationRelationError",
]
