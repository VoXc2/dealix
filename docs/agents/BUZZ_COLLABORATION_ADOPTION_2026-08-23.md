# Buzz Collaboration Adoption — Dealix

Date: 2026-08-23
Issue: #1187
Source reviewed: `VoXc2/buzz` (fork of `block/buzz`)
License reviewed: Apache License 2.0

## Decision

Dealix adopts the high-value **collaboration patterns** demonstrated by Buzz, but does **not** vendor or operate Buzz as a second runtime, relay, authentication plane, tenant authority, workflow engine, or source of truth.

Dealix already owns canonical business state through Company Brain, Opportunities, Actions, Drafts, Approvals, Outcomes, Proof, Learning, durable PostgreSQL storage, and the existing approval-first Communication OS. Running a second collaboration source of truth would create conflicting tenancy, execution, audit, and governance semantics.

The adopted design therefore extends the existing Dealix Communication OS with a tenant-scoped collaboration event collection and a native Collaboration Hub.

## Verified Buzz concepts used as design inputs

The reviewed Buzz repository documents these useful concepts:

- people and agents participating in the same workspace;
- channels, DMs, messages, threads and reactions;
- shared canvases and media annotations;
- agent identities, jobs and an agent-first CLI surface;
- Git/branch/status events in the same collaboration history;
- workflow lifecycle events;
- presence, typing and huddle lifecycle events;
- unified search over collaboration history;
- append/event-log semantics with deterministic identity;
- tenant/community isolation established before tenant-observable operations;
- auditable provenance for human and agent activity.

These are adopted as product/architecture patterns, not as a second protocol requirement.

## Native Dealix mapping

| Buzz concept | Dealix canonical mapping |
|---|---|
| Community/workspace | `tenant_id` and existing tenant boundaries |
| Relay event log | `collaboration_events` collection in existing Communication OS storage |
| Channels / DMs | collaboration events with `channel_id` |
| Thread / reaction relations | `parent_event_id` + `root_event_id` |
| Agent membership | `agent_registered` event with capabilities and concurrency metadata |
| Agent inbox / job | `agent_job_requested` / `agent_job_status` + attention feed |
| Git events | internal `git_event` records; GitHub remains source of repository truth |
| Workflow events | internal `workflow_event` records; existing Dealix workflow/control plane remains authoritative |
| Search | tenant-scoped Collaboration Hub search |
| Attention / mentions | `attention_for` + agent/human attention feed |
| Presence / typing | transient-class collaboration events, never proof eligible |
| Huddles | lifecycle records only; no voice subsystem is introduced by this slice |
| Audit provenance | deterministic event IDs, semantic content hashes, actor/source metadata |

## Safety invariants

1. Dealix remains the source of truth.
2. Collaboration events never grant external execution authority.
3. External communication remains Draft -> Approval -> controlled execution.
4. Collaboration API is admin-gated until a narrower tenant-auth surface is proven.
5. Every read/search/relation is explicitly tenant-scoped.
6. Deterministic IDs make retries idempotent; conflicting reuse fails closed.
7. Cross-tenant parent, thread, job and event references fail closed.
8. Presence and typing records are transient-class and cannot become business proof.
9. Agent job records are coordination records only; they do not authorize tools, merge, deploy, payment, or production mutation.
10. Git and workflow events are evidence/coordination bridges, not alternate execution authorities.

## Storage decision

The existing PostgreSQL Communication OS table stores one JSON snapshot row per collection. The original migration also constrains the allowed collection names to `contact_log` and `sequences`, so the collaboration slice includes a narrow Alembic migration:

`db/migrations/versions/20260823_021_collaboration_events.py`

It expands that existing check constraint and seeds an empty `collaboration_events` snapshot row. It does **not** create a parallel table. The downgrade fails closed if durable collaboration data exists instead of deleting history silently.

Merging the migration definition is repository work. **Applying it to production remains a separate governed production mutation and is not performed by this PR.**

Local/tests continue to use the explicit file adapter. Staging/production continue to fail closed unless PostgreSQL is configured and the required migration is present.

## Implemented slice

- `dealix/company_intelligence/collaboration_contracts.py`
- `intelligence/collaboration_hub.py`
- `api/routers/ops_collaboration.py`
- extension of `intelligence/communication_storage.py`
- `db/migrations/versions/20260823_021_collaboration_events.py`
- registration in `api/routers/domains/ops.py`
- `tests/test_collaboration_hub.py`

Event kinds cover:

- channel and DM creation;
- messages and thread replies;
- reactions;
- attachments and media annotations;
- canvas updates;
- agent registration, job requests and job statuses;
- Git events;
- workflow events;
- presence and typing;
- huddle lifecycle records;
- Approval and Proof references.

## Explicitly not adopted in this slice

- Nostr as a new Dealix wire protocol;
- a second Rust relay runtime;
- a second authentication/identity authority;
- Redis pub/sub solely for collaboration;
- a second workflow engine;
- a second Git host;
- a second audit ledger;
- direct agent tool authority;
- automatic external sending;
- a new voice stack;
- production deployment, migration application, or DNS changes.

These exclusions preserve Dealix's existing architecture and reduce operational risk while still capturing the collaboration value.

## Attribution

Buzz is an Apache-2.0 project. This Dealix slice was implemented natively in Python against Dealix contracts and storage. Buzz documentation and architecture were used as design inspiration and capability reference. No separate Buzz runtime is bundled here. Any future direct source-code reuse must preserve the Apache-2.0 license notices and attribution required by that license.
