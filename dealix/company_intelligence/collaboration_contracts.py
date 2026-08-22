"""Canonical collaboration-event contracts for Dealix Company Intelligence.

This module adapts high-value collaboration/event-log ideas from the Apache-2.0
Buzz project into Dealix's existing tenant, approval, proof, and communication
architecture. Dealix remains the source of truth; no external relay or second
execution authority is introduced here.

The contracts are persistence-neutral and have no database, network, or LLM I/O.
Collaboration records may reference canonical Approval/Proof records, but they
never become business proof themselves and never authorize external execution.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

NonEmptyString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

_SENSITIVE_METADATA_KEYS = {
    "authorization",
    "api_key",
    "access_token",
    "refresh_token",
    "password",
    "private_key",
    "secret",
    "token",
}
_SENSITIVE_METADATA_SUFFIXES = (
    "_api_key",
    "_access_token",
    "_refresh_token",
    "_password",
    "_private_key",
    "_secret",
    "_token",
)


class CollaborationActorType(StrEnum):
    """Actor classes that can participate in the Dealix collaboration plane."""

    HUMAN = "human"
    AGENT = "agent"
    SYSTEM = "system"
    WORKFLOW = "workflow"


class CollaborationEventKind(StrEnum):
    """Canonical event kinds supported by the collaboration plane."""

    CHANNEL_CREATED = "channel_created"
    DM_CREATED = "dm_created"
    MESSAGE = "message"
    THREAD_REPLY = "thread_reply"
    REACTION = "reaction"
    ATTACHMENT = "attachment"
    MEDIA_ANNOTATION = "media_annotation"
    CANVAS_UPDATE = "canvas_update"
    AGENT_REGISTERED = "agent_registered"
    AGENT_JOB_REQUESTED = "agent_job_requested"
    AGENT_JOB_STATUS = "agent_job_status"
    GIT_EVENT = "git_event"
    WORKFLOW_EVENT = "workflow_event"
    PRESENCE = "presence"
    TYPING = "typing"
    HUDDLE_EVENT = "huddle_event"
    APPROVAL_REFERENCE = "approval_reference"
    PROOF_REFERENCE = "proof_reference"


class CollaborationRetentionClass(StrEnum):
    """Retention intent; transient records are never valid business proof."""

    AUDIT = "audit"
    TRANSIENT = "transient"


def _canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        default=str,
    )


def _metadata_has_sensitive_keys(value: Any) -> bool:
    """Reject obvious credential-bearing metadata fields before persistence."""

    if isinstance(value, dict):
        for raw_key, nested in value.items():
            key = str(raw_key).strip().lower()
            if key in _SENSITIVE_METADATA_KEYS or key.endswith(_SENSITIVE_METADATA_SUFFIXES):
                return True
            if _metadata_has_sensitive_keys(nested):
                return True
    elif isinstance(value, (list, tuple)):
        return any(_metadata_has_sensitive_keys(item) for item in value)
    return False


def stable_collaboration_event_id(*, tenant_id: str, deduplication_key: str) -> str:
    canonical = _canonical_json(
        {
            "deduplication_key": deduplication_key.strip(),
            "tenant_id": tenant_id.strip(),
        }
    )
    return f"collab_{sha256(canonical.encode('utf-8')).hexdigest()[:20]}"


def collaboration_content_hash(payload: dict[str, Any]) -> str:
    return sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


class CanonicalCollaborationEvent(BaseModel):
    """One immutable-in-storage tenant-scoped collaboration event.

    IDs are deterministic from tenant + deduplication key. ``content_hash``
    fingerprints the semantic payload so retrying the same event is idempotent,
    while reusing a deduplication key for different content fails closed.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    tenant_id: NonEmptyString
    event_id: NonEmptyString
    deduplication_key: NonEmptyString
    kind: CollaborationEventKind

    actor_id: NonEmptyString
    actor_type: CollaborationActorType
    target_actor_id: str = ""

    channel_id: str = ""
    conversation_id: str = ""
    parent_event_id: str = ""
    root_event_id: str = ""

    content: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    attention_for: tuple[str, ...] = ()

    retention_class: CollaborationRetentionClass = CollaborationRetentionClass.AUDIT
    proof_eligible: bool = False

    source_id: NonEmptyString
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    content_hash: NonEmptyString

    external_effect: bool = False
    execution_allowed: bool = False

    @model_validator(mode="after")
    def enforce_collaboration_invariants(self) -> CanonicalCollaborationEvent:
        expected_id = stable_collaboration_event_id(
            tenant_id=self.tenant_id,
            deduplication_key=self.deduplication_key,
        )
        if self.event_id != expected_id:
            raise ValueError("event_id does not match tenant + deduplication key")

        if self.external_effect or self.execution_allowed:
            raise ValueError("collaboration events never authorize external execution")
        if self.proof_eligible:
            raise ValueError("collaboration records cannot become business proof")
        if _metadata_has_sensitive_keys(self.metadata):
            raise ValueError("credential-bearing metadata keys are not allowed")

        transient_kinds = {
            CollaborationEventKind.PRESENCE,
            CollaborationEventKind.TYPING,
        }
        if self.kind in transient_kinds:
            if self.retention_class != CollaborationRetentionClass.TRANSIENT:
                raise ValueError("presence and typing events must be transient")
        elif self.retention_class == CollaborationRetentionClass.TRANSIENT:
            raise ValueError("only presence and typing events may be transient")

        if self.kind == CollaborationEventKind.THREAD_REPLY and not self.parent_event_id:
            raise ValueError("thread replies require parent_event_id")
        if self.kind == CollaborationEventKind.REACTION and not self.parent_event_id:
            raise ValueError("reactions require parent_event_id")
        if self.kind == CollaborationEventKind.MEDIA_ANNOTATION and not self.parent_event_id:
            raise ValueError("media annotations require parent_event_id")

        channel_kinds = {
            CollaborationEventKind.CHANNEL_CREATED,
            CollaborationEventKind.DM_CREATED,
            CollaborationEventKind.MESSAGE,
            CollaborationEventKind.THREAD_REPLY,
            CollaborationEventKind.REACTION,
            CollaborationEventKind.ATTACHMENT,
            CollaborationEventKind.MEDIA_ANNOTATION,
            CollaborationEventKind.CANVAS_UPDATE,
            CollaborationEventKind.PRESENCE,
            CollaborationEventKind.TYPING,
            CollaborationEventKind.HUDDLE_EVENT,
        }
        if self.kind in channel_kinds and not self.channel_id:
            raise ValueError(f"{self.kind.value} requires channel_id")

        if self.kind == CollaborationEventKind.DM_CREATED:
            participants = self.metadata.get("participants")
            if not isinstance(participants, list) or len(participants) < 2:
                raise ValueError("DM creation requires at least two participants")

        if self.kind == CollaborationEventKind.AGENT_REGISTERED:
            capabilities = self.metadata.get("capabilities")
            max_concurrency = self.metadata.get("max_concurrency")
            if not isinstance(capabilities, list):
                raise ValueError("agent registration requires capabilities list")
            if not isinstance(max_concurrency, int) or max_concurrency < 1:
                raise ValueError("agent registration requires max_concurrency >= 1")

        if self.kind == CollaborationEventKind.AGENT_JOB_REQUESTED:
            if not self.target_actor_id:
                raise ValueError("agent job requests require target_actor_id")
            if not self.content.strip():
                raise ValueError("agent job requests require an objective")

        if self.kind == CollaborationEventKind.AGENT_JOB_STATUS:
            if not self.target_actor_id:
                raise ValueError("agent job status requires target_actor_id")
            if not self.metadata.get("job_event_id"):
                raise ValueError("agent job status requires job_event_id metadata")

        if self.kind == CollaborationEventKind.ATTACHMENT:
            if not self.metadata.get("asset_id") or not self.metadata.get("media_type"):
                raise ValueError("attachments require asset_id and media_type metadata")

        if self.kind == CollaborationEventKind.CANVAS_UPDATE and not self.metadata.get("canvas_id"):
            raise ValueError("canvas updates require canvas_id metadata")

        if self.kind == CollaborationEventKind.GIT_EVENT:
            if not self.metadata.get("repository") or not self.metadata.get("event_type"):
                raise ValueError("git events require repository and event_type metadata")

        if self.kind == CollaborationEventKind.WORKFLOW_EVENT:
            if not self.metadata.get("workflow_id") or not self.metadata.get("event_type"):
                raise ValueError("workflow events require workflow_id and event_type metadata")

        if self.kind == CollaborationEventKind.APPROVAL_REFERENCE and not self.metadata.get(
            "approval_id"
        ):
            raise ValueError("approval references require approval_id metadata")

        if self.kind == CollaborationEventKind.PROOF_REFERENCE and not self.metadata.get(
            "proof_event_id"
        ):
            raise ValueError("proof references require proof_event_id metadata")

        expected_hash = collaboration_content_hash(self.semantic_payload())
        if self.content_hash != expected_hash:
            raise ValueError("content_hash does not match semantic collaboration payload")
        return self

    def semantic_payload(self) -> dict[str, Any]:
        """Return fields whose meaning must remain stable across retries."""
        return {
            "actor_id": self.actor_id,
            "actor_type": self.actor_type.value,
            "attention_for": list(self.attention_for),
            "channel_id": self.channel_id,
            "content": self.content,
            "conversation_id": self.conversation_id,
            "kind": self.kind.value,
            "metadata": self.metadata,
            "parent_event_id": self.parent_event_id,
            "proof_eligible": self.proof_eligible,
            "retention_class": self.retention_class.value,
            "root_event_id": self.root_event_id,
            "source_id": self.source_id,
            "target_actor_id": self.target_actor_id,
            "tenant_id": self.tenant_id,
        }


def build_collaboration_event(
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
    root_event_id: str = "",
    content: str = "",
    metadata: dict[str, Any] | None = None,
    attention_for: tuple[str, ...] = (),
    retention_class: CollaborationRetentionClass | None = None,
    proof_eligible: bool = False,
) -> CanonicalCollaborationEvent:
    """Build a deterministic collaboration event with a semantic hash."""

    resolved_retention = retention_class
    if resolved_retention is None:
        if kind in {CollaborationEventKind.PRESENCE, CollaborationEventKind.TYPING}:
            resolved_retention = CollaborationRetentionClass.TRANSIENT
        else:
            resolved_retention = CollaborationRetentionClass.AUDIT

    normalized_metadata = metadata or {}
    semantic = {
        "actor_id": actor_id.strip(),
        "actor_type": actor_type.value,
        "attention_for": list(attention_for),
        "channel_id": channel_id.strip(),
        "content": content,
        "conversation_id": conversation_id.strip(),
        "kind": kind.value,
        "metadata": normalized_metadata,
        "parent_event_id": parent_event_id.strip(),
        "proof_eligible": proof_eligible,
        "retention_class": resolved_retention.value,
        "root_event_id": root_event_id.strip(),
        "source_id": source_id.strip(),
        "target_actor_id": target_actor_id.strip(),
        "tenant_id": tenant_id.strip(),
    }

    return CanonicalCollaborationEvent(
        tenant_id=tenant_id,
        event_id=stable_collaboration_event_id(
            tenant_id=tenant_id,
            deduplication_key=deduplication_key,
        ),
        deduplication_key=deduplication_key,
        kind=kind,
        actor_id=actor_id,
        actor_type=actor_type,
        target_actor_id=target_actor_id,
        channel_id=channel_id,
        conversation_id=conversation_id,
        parent_event_id=parent_event_id,
        root_event_id=root_event_id,
        content=content,
        metadata=normalized_metadata,
        attention_for=attention_for,
        retention_class=resolved_retention,
        proof_eligible=proof_eligible,
        source_id=source_id,
        content_hash=collaboration_content_hash(semantic),
        external_effect=False,
        execution_allowed=False,
    )


__all__ = [
    "CanonicalCollaborationEvent",
    "CollaborationActorType",
    "CollaborationEventKind",
    "CollaborationRetentionClass",
    "build_collaboration_event",
    "collaboration_content_hash",
    "stable_collaboration_event_id",
]
