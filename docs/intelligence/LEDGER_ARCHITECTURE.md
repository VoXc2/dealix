# Ledger Architecture — Intelligence · Operating Brain

**Layer:** Intelligence · Operating Brain
**Owner:** Chief of Staff
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [LEDGER_ARCHITECTURE_AR.md](./LEDGER_ARCHITECTURE_AR.md)

## Context
Ledgers are the durable, append-only memory of the Intelligence Layer. They
hold every event in a typed, queryable form so that metrics, decisions, and
audit can all read the same truth. Dealix runs nine ledgers — each with a
purpose, a schema, and a single primary consumer. Without this discipline,
events scatter into logs and dashboards, and Dealix loses the ability to
audit its own decisions. See `docs/DEALIX_OPERATING_CONSTITUTION.md` for the
append-only and auditability mandates, and
`docs/AI_OBSERVABILITY_AND_EVALS.md` for the AI Run Ledger's runtime
coupling.

## Ledger principles
- **Append-only.** No updates, no deletes. Corrections are new entries with
  a `corrects` reference.
- **One primary consumer.** Every ledger has exactly one accountable role
  that uses it for decisions. Other roles may read; only the primary acts.
- **Typed payload.** Each ledger has a JSON Schema enforced at write.
- **PDPL-aware.** Ledgers carry minimal personal data; sensitive fields are
  tokenised and resolved via the Source Registry.
- **Retention.** Default 7 years for financial-impacting ledgers, 3 years
  for operational ledgers — see `docs/DATA_RETENTION_POLICY.md`.

## The nine ledgers

### 1. AI Run Ledger
- **Purpose.** Record every AI agent run: inputs, outputs, model, tokens,
  cost, latency, eval verdict, schema validation result.
- **Primary consumer.** Head of AI Ops.
- **Schema fields.** `run_id`, `project_id`, `agent_id`, `model`,
  `input_hash`, `output_hash`, `prompt_tokens`, `completion_tokens`,
  `cost_usd`, `latency_ms`, `eval_verdict`, `schema_valid`, `created_at`,
  `correlation_id`.
- **Feeds.** Cost per project, model fallback rate, schema failure rate,
  QA pass rate.

### 2. Audit Ledger
- **Purpose.** Record every human or agent action that affects a client
  asset, an approval, or a policy boundary.
- **Primary consumer.** Head of Governance.
- **Schema fields.** `audit_id`, `actor_id`, `actor_type` (human|agent),
  `action`, `target_type`, `target_id`, `policy_refs`, `outcome`,
  `created_at`, `evidence_uri`.
- **Feeds.** Approval delays, blocked actions, policy violations, PII flags.

### 3. Proof Ledger
- **Purpose.** Record measurable client value events that can become proof
  packs and case studies.
- **Primary consumer.** Head of Revenue.
- **Schema fields.** `proof_id`, `project_id`, `client_id`, `proof_type`
  (Revenue Value | Time Saved | Risk Reduced | Decision Quality),
  `metric`, `value`, `unit`, `source`, `client_approved`, `created_at`.
- **Feeds.** Proof packs per project, proof-to-retainer conversion, value
  categories covered.

### 4. Capital Ledger
- **Purpose.** Record reusable capital assets produced by delivery —
  scripts, datasets, prompts, playbooks, benchmarks, market-safe insights.
- **Primary consumer.** Head of Product.
- **Schema fields.** `asset_id`, `project_id`, `asset_type`, `reusable`,
  `market_safe`, `owner`, `location_uri`, `created_at`.
- **Feeds.** Assets per project, reusable assets ratio, market-safe
  insights count.

### 5. Productization Ledger
- **Purpose.** Track feature candidates, internal tools, and modules from
  proposal to release.
- **Primary consumer.** Head of Product.
- **Schema fields.** `candidate_id`, `source_project_ids[]`,
  `demand_count`, `status` (proposed|validated|building|released|killed),
  `owner`, `created_at`, `released_at`.
- **Feeds.** Feature candidates, manual hours saved, module adoption.

### 6. Client Health Ledger
- **Purpose.** Track engagement, sentiment, escalations, and retention
  signals per client.
- **Primary consumer.** Head of Customer Success.
- **Schema fields.** `health_id`, `client_id`, `signal_type` (sentiment |
  escalation | renewal_intent | churn_risk), `value`, `source`,
  `created_at`.
- **Feeds.** Retainer recommendations, churn risk dashboard, NPS feed.

### 7. Unit Performance Ledger
- **Purpose.** Aggregate per business unit financial and operational
  performance — revenue, margin, QA, proofs, retainers, product maturity.
- **Primary consumer.** CFO + CEO.
- **Schema fields.** `unit_id`, `period`, `revenue`, `margin`, `qa_score`,
  `proof_count`, `retainer_count`, `product_maturity`,
  `playbook_maturity`, `created_at`.
- **Feeds.** Capital allocation, Venture Readiness Score.

### 8. Partner Ledger
- **Purpose.** Record partner leads, co-sells, joint deliveries, and
  partner revenue share.
- **Primary consumer.** Head of Partnerships.
- **Schema fields.** `partner_lead_id`, `partner_id`, `client_id`,
  `stage`, `value`, `revshare_pct`, `created_at`.
- **Feeds.** Partner program KPIs (`docs/AGENCY_PARTNER_PROGRAM.md`).

### 9. Venture Signal Ledger
- **Purpose.** Record graduation-relevant signals — paid clients, retainers,
  module usage, playbook maturity, margin, owner readiness, proof library
  state — per candidate unit.
- **Primary consumer.** CEO.
- **Schema fields.** `signal_id`, `unit_id`, `signal_type`, `value`,
  `weight`, `created_at`.
- **Feeds.** Venture Readiness Score (`VENTURE_SIGNAL_MODEL.md`).

## Ownership matrix
| Ledger | Writer | Primary consumer | Auditor |
|---|---|---|---|
| AI Run | Agents (auto) | Head of AI Ops | Head of Governance |
| Audit | Runtime guard (auto) | Head of Governance | Compliance |
| Proof | Delivery + Client confirm | Head of Revenue | CEO |
| Capital | Delivery | Head of Product | Head of Engineering |
| Productization | Product | Head of Product | CEO |
| Client Health | Customer Success | Head of CS | CEO |
| Unit Performance | Finance | CFO + CEO | Audit committee |
| Partner | Partnerships | Head of Partnerships | CEO |
| Venture Signal | Chief of Staff | CEO | Board |

## Write rules
- Writes go through the event bus from `EVENT_TO_DECISION_SYSTEM.md`. No
  direct writes from application code.
- Each ledger validates its payload against its JSON Schema; failures land
  in a dead-letter queue and emit an Audit Ledger entry.
- A correction is itself an event with `corrects=<entry_id>`; the original
  entry remains.
- Cross-ledger references use opaque IDs; no joins on raw PII.

## Read rules
- Read access is role-scoped (see
  `docs/governance/PERMISSION_MIRRORING.md`).
- Metrics queries hit ledgers, not application databases.
- BI exports run from ledgers nightly; nothing is computed off raw logs.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Bus events from Core OS | Append-only ledger entries | Chief of Staff | Continuous |
| Ledger entries | Metric Engine inputs | Head of Data | Continuous |
| Ledger entries | Audit & PDPL reports | Head of Governance | Monthly |
| Corrections | New entries with `corrects` ref | Each ledger owner | As needed |

## Metrics
- **Ledger Write Success Rate** — share of bus events successfully
  persisted (target: >=99.9%).
- **Dead-Letter Rate** — share of events failing schema validation
  (target: <0.5%).
- **Correction Rate** — share of entries corrected within 30 days
  (target: <2%).
- **Read Latency** — p95 query latency for metric recomputes
  (target: <2s).

## Related
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — auditability and append-only mandates
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — AI Run Ledger runtime coupling
- `docs/DATA_RETENTION_POLICY.md` — retention rules per ledger class
- `docs/governance/PERMISSION_MIRRORING.md` — role-scoped read access
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
