# Event-Driven Operating Model — Compound Holding Model

**Layer:** Holding · Compound Holding Model
**Owner:** Head of Dealix Core (CTO)
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [EVENT_DRIVEN_OPERATING_MODEL_AR.md](./EVENT_DRIVEN_OPERATING_MODEL_AR.md)

## Context
Dealix runs as an **event-driven operating model**: every meaningful state change inside Core OS emits a structured domain event. Events are the spinal cord that connects the Application, AI Control, Governance, Data, Integration, and Learning layers without coupling them. This is what allows the holding to be modular today and to split into microservices tomorrow without rewriting business logic. The architecture is described in `docs/BEAST_LEVEL_ARCHITECTURE.md`, the reliability posture in `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`, and the runtime provenance in `docs/ledgers/AI_RUN_LEDGER.md`.

## What events enable

- **Audit** — every business action is reconstructable.
- **Analytics** — board and BU dashboards subscribe instead of polling.
- **Proof Ledger** — proof events accumulate as the legal record of value.
- **Automation** — workflows trigger off events, not timers.
- **Notifications** — clients and operators receive context-aware updates.
- **AI Control Tower** — Gateway events drive cost, eval, and drift telemetry.
- **Product telemetry** — feature candidate events feed the Productization Ledger.

## Common event envelope

Every event uses this envelope (fields in addition to type-specific payload):

```json
{
  "event_type": "<string>",
  "event_id": "<uuid>",
  "project_id": "<string>",
  "tenant_id": "<string>",
  "actor": { "type": "<user|agent|system>", "id": "<string>" },
  "created_at": "<ISO-8601 UTC>",
  "schema_version": "1"
}
```

Type-specific fields are documented per event below.

## Domain events taxonomy

| Event type | When emitted | Primary consumer |
|---|---|---|
| `dataset_uploaded` | A dataset is ingested into Data OS | Data OS, Data BU |
| `data_quality_scored` | DRS computed for a source | Data OS, BU dashboards |
| `pii_detected` | PII tagging finds new PII | Governance Runtime |
| `governance_check_passed` | Policy check approves a workflow step | Audit Log |
| `account_scored` | An account is scored by Revenue Workspace | Revenue BU |
| `draft_generated` | A draft outreach / reply is produced | Revenue / Support BUs |
| `approval_required` | A step needs human approval | Approval Matrix |
| `approval_granted` | Human approves a step | Audit Log |
| `proof_event_created` | ROI / outcome evidence captured | Proof Ledger |
| `report_delivered` | A report is generated and delivered to client | BU + Brand |
| `capital_asset_created` | A reusable asset enters Capital Ledger | Head of Core |
| `feature_candidate_created` | A repeated step is flagged for productization | Product Council |
| `retainer_recommended` | CSM heuristic recommends retainer offer | CSM workspace |

## Example events

### 1. `account_scored`

```json
{
  "event_type": "account_scored",
  "event_id": "evt_01HV2K8Z9X",
  "project_id": "PRJ-001",
  "tenant_id": "TEN-acme",
  "actor": { "type": "agent", "id": "revenue.scoring-v3" },
  "created_at": "2026-05-13T10:00:00Z",
  "schema_version": "1",
  "account_id": "ACC-443",
  "score": 87,
  "governance_status": "approved_with_review",
  "policy_id": "pol_rev_scoring_v2",
  "model_id": "claude-opus-4-7",
  "input_hash": "sha256:9a8b…"
}
```

### 2. `proof_event_created`

```json
{
  "event_type": "proof_event_created",
  "event_id": "evt_01HV3R1QPM",
  "project_id": "PRJ-001",
  "tenant_id": "TEN-acme",
  "actor": { "type": "user", "id": "user_dlx_jane" },
  "created_at": "2026-05-13T12:30:00Z",
  "schema_version": "1",
  "proof_type": "roi_measured",
  "metric": "hours_saved_per_week",
  "baseline": 32,
  "current": 6,
  "value_sar": 18000,
  "evidence_ref": "proof_pack/PRJ-001/v1.pdf"
}
```

### 3. `governance_check_passed`

```json
{
  "event_type": "governance_check_passed",
  "event_id": "evt_01HV3T9NB8",
  "project_id": "PRJ-001",
  "tenant_id": "TEN-acme",
  "actor": { "type": "system", "id": "governance-runtime" },
  "created_at": "2026-05-13T12:31:00Z",
  "schema_version": "1",
  "policy_id": "pol_pdpl_export_v1",
  "subject": "model_call:mcl_01HV3T9N",
  "decision": "allow",
  "redactions_applied": ["email", "phone"]
}
```

### 4. `capital_asset_created`

```json
{
  "event_type": "capital_asset_created",
  "event_id": "evt_01HV41ZK6Q",
  "project_id": "PRJ-001",
  "tenant_id": "TEN-acme",
  "actor": { "type": "user", "id": "user_dlx_ops_lead" },
  "created_at": "2026-05-13T14:10:00Z",
  "schema_version": "1",
  "asset_type": "prompt_template",
  "asset_id": "asset_rev_account_score_v3",
  "asset_ref": "capital_ledger/prompt_templates/rev_account_score_v3.md",
  "reusability_tags": ["revenue", "saudi", "b2b"]
}
```

### 5. `retainer_recommended`

```json
{
  "event_type": "retainer_recommended",
  "event_id": "evt_01HV4G7RPC",
  "project_id": "PRJ-001",
  "tenant_id": "TEN-acme",
  "actor": { "type": "agent", "id": "csm.retainer-radar-v1" },
  "created_at": "2026-05-13T15:45:00Z",
  "schema_version": "1",
  "retainer_readiness_score": 78,
  "recommended_tier": "monthly_revops_os",
  "rationale": "qa_score=92 proof_pack=present value_realization=4.6x"
}
```

## Delivery guarantees

- **At-least-once** delivery on the bus; consumers are idempotent on `event_id`.
- **Schema-versioned**; consumers honor `schema_version` and accept additive fields.
- **PDPL-aware**; events never carry raw PII — only references and redacted forms.
- **Replayable** from the bus for at least 30 days for incident recovery.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| State changes across Core OS | Domain events on bus | Each layer's emitters | Realtime |
| Subscribed consumers | Reactions (audit, automation, telemetry) | Consuming modules | Realtime |
| Event schema changes | Versioned schema bump | Head of Core | Quarterly |

## Metrics
- **Event emission rate** — events / hour per type.
- **Consumer lag p95** — seconds behind head.
- **Schema-version drift** — count of consumers still on N-1 after window.
- **PII leakage events** — must be 0.
- **Replayability** — % events replayable for the last 30 days.

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architectural foundation.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — reliability posture.
- `docs/ledgers/AI_RUN_LEDGER.md` — sibling run-ledger.
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability framework.
- `docs/product/AI_RUN_PROVENANCE.md` — provenance design.
- `docs/holding/CORE_OS_ARCHITECTURE.md` — Core OS layered architecture.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
