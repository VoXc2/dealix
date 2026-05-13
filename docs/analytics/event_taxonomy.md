---
title: Event Taxonomy — canonical event names, properties, categories, owners, retention
doc_id: W4.T12.event-taxonomy
owner: HoData
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T13.executive-kpi-spec, W4.T14.revenue-os-policy-rules, W4.T21.adr-0001, W4.T21.adr-0004, W4.T25.data-quality-gates, W4.T26.ab-framework]
kpi: { metric: events_with_required_properties_pct, target: 99.5, window: continuous }
rice: { reach: 0, impact: 3, confidence: 0.9, effort: 4pw, score: engineering }
---

# Event Taxonomy

## 1. Purpose

Define the canonical names, shapes, owners, and retention of every analytics event emitted by Dealix. This is the contract that powers product analytics (PostHog), executive KPIs (W4.T13), experimentation (W4.T26), data-quality reporting (W4.T25), and the audit trail (W4.T14). Cross-links the operational PostHog inventory in `docs/ops/POSTHOG_EVENTS.md`.

## 2. Naming Conventions

- **snake_case**, ASCII only, no spaces.
- Format: `<category>_<noun>_<verb_past_tense>`. Examples: `lead_record_created`, `passport_emission_completed`, `policy_rule_blocked`.
- Verbs are **past tense** ("created", "completed", "failed") because events describe things that already happened.
- One verb per event. Do not concatenate (`lead_created_and_enriched` is two events).
- Length cap: 64 characters.

Anti-patterns (rejected at code review):

- camelCase or PascalCase.
- Tense ambiguity (`lead_enrich`, `lead_enriches`).
- Adjective stuffing (`fast_high_quality_lead_created`).
- Vendor-specific names (`apollo_response_received`) — use generic class (`source_response_received`) with a `source_id` property.

## 3. Required Properties (every event)

Every event carries the following properties. No exceptions.

| Property | Type | Required | Notes |
|---|---|---|---|
| `event_id` | UUID | yes | client-generated; deduplication key |
| `event_name` | string | yes | from this taxonomy |
| `event_ts` | ISO-8601 timestamp (UTC) | yes | when it happened |
| `received_ts` | ISO-8601 timestamp (UTC) | yes | when the collector saw it |
| `tenant_id` | UUID | yes | except `system_*` events |
| `actor` | string enum | yes | `human:<user_id>` / `agent:<service>` / `system` |
| `service` | string | yes | emitting service name |
| `service_version` | string | yes | git SHA or semver |
| `trace_id` | hex | yes | OpenTelemetry trace ID for correlation |
| `region` | enum | yes | `ksa-central`, `ksa-east`, etc. |
| `environment` | enum | yes | `dev`, `stage`, `prod` |

## 4. Conditional Properties

Required when the event involves the named domain object.

| Property | When required | Type | Notes |
|---|---|---|---|
| `lead_id` | any `lead_*`, `passport_*`, `action_*` involving a lead | UUID | |
| `passport_id` | any `passport_*`, `action_*`, `policy_*` referencing a passport | UUID | |
| `evidence_level` | passport / action events | enum `low`/`medium`/`high` | |
| `vertical` | lead-scoped events | enum (banking, retail, ...) | from policy taxonomy |
| `region_kpi` | lead-scoped events | enum KSA regions or ISO 3166-2 | distinct from emitter `region` |
| `rule_id` | `policy_*` events | string `P-XXX` | matches policy rules doc |
| `experiment_id` | `experiment_*` events | string `EXP-YYYY-Q*-NNN` | matches experiment registry |
| `model_id` | LLM-call events | string | vendor-prefixed: `anthropic:sonnet-4.7` |
| `cost_sar` | LLM-call events | decimal | per-event cost attribution |

## 5. PII and Sensitive Fields

- Email, phone, name, ID number, IBAN, account number: **never** in event properties. If a workflow needs them, the event carries a reference (`lead_id`, `customer_id`) and the PII is fetched server-side at read time.
- Redaction is enforced at emit-time by `redact()` helper (see ADR-0004).
- For events that **must** carry PII for product analytics (rare; e.g. consented user identifier for funnel reporting), use the hashed form `sha256:<hex>` with a per-tenant salt.

## 6. Event Categories

Eight categories. Each category has an owner and a retention class.

### 6.1 `lead_*` (owner: Head of Data)

Lead lifecycle from ingest to disposition.

- `lead_record_created` — new lead enters Revenue OS.
- `lead_record_deduplicated` — incoming lead matched an existing canonical record.
- `lead_signal_received` — an external signal attached to the lead.
- `lead_enrichment_started`
- `lead_enrichment_completed`
- `lead_qualification_completed`
- `lead_disposition_set` — e.g. `qualified`, `disqualified`, `nurture`.
- `lead_duplicate_merged`
- `lead_record_archived`

### 6.2 `passport_*` (owner: CTO)

Decision passport lifecycle. Mirrors `DecisionPassportTracer` spans (ADR-0004).

- `passport_intent_created`
- `passport_evidence_collected`
- `passport_policy_checked`
- `passport_emission_completed`
- `passport_outcome_recorded`
- `passport_retrieved`
- `passport_disputed` — customer or regulator dispute.

### 6.3 `action_*` (owner: HoData)

Outbound side-effects gated by passport.

- `action_dispatch_requested`
- `action_dispatch_completed`
- `action_dispatch_failed`
- `action_dispatch_deduplicated` — idempotency hit (rule P-070).
- `action_outcome_observed` — reply, click, conversion.

### 6.4 `policy_*` (owner: CTO)

Policy module emissions; corresponds to `dealix/trust/policy.py`.

- `policy_rule_evaluated`
- `policy_rule_allowed`
- `policy_rule_blocked`
- `policy_rule_escalated`
- `policy_audit_emitted`
- `policy_version_changed` — rule catalogue version bumped.

### 6.5 `billing_*` (owner: CEO)

Revenue and billing — Moyasar callbacks, invoice events.

- `billing_checkout_started`
- `billing_checkout_completed`
- `billing_subscription_renewed`
- `billing_subscription_canceled`
- `billing_invoice_issued`
- `billing_invoice_paid`
- `billing_invoice_failed`
- `billing_refund_issued`

### 6.6 `system_*` (owner: CTO)

Operational events; `tenant_id` may be absent for global events.

- `system_service_started`
- `system_service_stopped`
- `system_health_check_failed`
- `system_quarantine_admitted` — record entered the quality-gate quarantine.
- `system_quarantine_repaired`
- `system_slo_burn_detected`

### 6.7 `experiment_*` (owner: HoData)

Experimentation framework events. Drive A/B analysis.

- `experiment_registered`
- `experiment_started`
- `experiment_exposure_assigned`
- `experiment_stopped`
- `experiment_shipped`
- `experiment_rolled_back`

### 6.8 `pdpl_*` (owner: CTO + Compliance)

PDPL-specific events. High-retention.

- `pdpl_dsr_received` — data subject rights request.
- `pdpl_dsr_acknowledged`
- `pdpl_dsr_fulfilled`
- `pdpl_dsr_rejected`
- `pdpl_cross_border_transfer_recorded`
- `pdpl_consent_recorded`
- `pdpl_consent_withdrawn`
- `pdpl_breach_recorded`

## 7. Owners and Retention

| Category | Owner | Retention (hot) | Retention (cold) | Total |
|---|---|---|---|---|
| `lead_*` | HoData | 13 months | 23 months | 36 months |
| `passport_*` | CTO | 24 months | 60 months | 84 months |
| `action_*` | HoData | 13 months | 23 months | 36 months |
| `policy_*` | CTO | 24 months | 60 months | 84 months |
| `billing_*` | CEO | 36 months | 84 months | 120 months (ZATCA) |
| `system_*` | CTO | 3 months | 9 months | 12 months |
| `experiment_*` | HoData | 12 months | 24 months | 36 months |
| `pdpl_*` | CTO + Compliance | 24 months | 60 months | 84 months |

Retention transitions are operationalized in `docs/ops/PDPL_RETENTION_POLICY.md`.

## 8. Schema Governance

- Schemas live as JSON Schema in `analytics/event_schemas/<event_name>.schema.json`.
- CI check: every event emitted by code must have a matching schema; PR adds the schema in the same commit.
- Breaking schema change (remove field, change type) requires a new event name (`lead_record_created_v2`); the old name is deprecated per ADR-0005 timing.
- Field additions are additive and never break consumers.

## 9. Cross-Link to PostHog Inventory

The operational PostHog inventory in `docs/ops/POSTHOG_EVENTS.md` lists events currently wired up in the SPA and backend. Reconciliation rule:

- Every event in this taxonomy with an `audience: product_analytics` annotation MUST appear in `POSTHOG_EVENTS.md`.
- Every event in `POSTHOG_EVENTS.md` MUST appear here.
- Quarterly reconciliation review; mismatches are blockers for the analytics owner.

## 10. Sample Event

```json
{
  "event_id": "9c2b...",
  "event_name": "passport_emission_completed",
  "event_ts": "2026-05-13T08:42:11.184Z",
  "received_ts": "2026-05-13T08:42:11.196Z",
  "tenant_id": "5b1f...",
  "actor": "agent:orchestrator",
  "service": "revenue-os",
  "service_version": "1.7.2+a3f9c1d",
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "region": "ksa-central",
  "environment": "prod",
  "lead_id": "7a31...",
  "passport_id": "PP-2026-05-1284",
  "evidence_level": "high",
  "vertical": "banking",
  "region_kpi": "SA-01",
  "cost_sar": "0.42",
  "model_id": "anthropic:sonnet-4.7"
}
```

## 11. References

- Operational inventory: `docs/ops/POSTHOG_EVENTS.md` (cross-linked, kept in sync).
- ADRs: ADR-0001 (event store), ADR-0004 (observability), ADR-0005 (API versioning).
- Related: `docs/policy/revenue_os_policy_rules.md`, `docs/data/data_quality_gates.md`, `docs/analytics/executive_kpi_spec.md`, `docs/experiments/ab_framework.md`.
- Compliance: `docs/PRIVACY_PDPL_READINESS.md`, `docs/ops/PDPL_RETENTION_POLICY.md`.

## 12. Review Cadence

Quarterly. Out-of-cycle change if a new product surface ships or a new regulator demand emerges.
