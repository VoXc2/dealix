# Event-to-Decision System — Intelligence · Operating Brain

**Layer:** Intelligence · Operating Brain
**Owner:** Chief of Staff
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [EVENT_TO_DECISION_SYSTEM_AR.md](./EVENT_TO_DECISION_SYSTEM_AR.md)

## Context
The Event-to-Decision System is the pipeline that converts raw operational
events into binding strategic decisions. Every meaningful action inside
Dealix — an AI run, an approval, a proof event, a retainer win — must emit
a structured event, land in a ledger, contribute to a metric, and (when
thresholds are crossed) trigger a decision. This file defines the event
vocabulary, the pipeline stages, and the worked sample flows. It is the
operating contract between Core OS (which emits events) and the Intelligence
Layer (which consumes them). See `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`
for the strategic posture this system enables, and
`docs/AI_OBSERVABILITY_AND_EVALS.md` for the observability backbone that
carries event payloads.

## Pipeline stages
```
+---------+    +--------+    +---------+    +----------+    +---------+
|  Event  | -> | Ledger | -> | Metric  | -> | Decision | -> | Action  |
+---------+    +--------+    +---------+    +----------+    +---------+
   emit         append        compute        threshold      Core OS
```

1. **Emit** — Core OS code, agents, and humans publish a JSON event via the
   event bus. Every event carries `event_type`, `project_id`, `client_id`,
   `created_at`, and a payload.
2. **Append** — the event is written to one or more ledgers
   (see `LEDGER_ARCHITECTURE.md`). Ledger writes are append-only and
   PDPL-aware.
3. **Compute** — the Metric Engine recomputes the affected indicators
   (see `METRICS_ENGINE.md`).
4. **Threshold** — a Decision Rule evaluates the metric against a band and
   either fires a decision or stays quiet.
5. **Action** — the decision is dispatched back to Core OS owners (Delivery,
   Revenue, Product, Governance) for execution.

The pipeline is asynchronous; the only synchronous coupling is between Emit
and Append. Everything else is recomputed on a schedule (continuous, hourly,
daily, weekly depending on the metric).

## Event taxonomy (verbatim)
Twenty-one canonical event types. Any new event type requires a written
proposal to the Chief of Staff and a corresponding ledger schema update.

```
project_created
client_intake_completed
data_source_registered
dataset_uploaded
data_quality_scored
pii_detected
governance_checked
ai_run_completed
account_scored
draft_generated
approval_required
approval_granted
proof_event_created
report_delivered
capital_asset_created
feature_candidate_created
retainer_recommended
retainer_won
playbook_updated
partner_lead_created
venture_signal_detected
```

Events not in this list MUST NOT be emitted to the Intelligence bus.
Operational telemetry (logs, traces, metrics) goes to the observability
stack, not here.

## Event envelope
Every event uses the same envelope. The `event_type` determines which
payload fields are required.

```json
{
  "event_type": "proof_event_created",
  "project_id": "PRJ-001",
  "client_id": "CL-001",
  "proof_type": "Revenue Value",
  "metric": "accounts_scored",
  "value": 50,
  "source": "Revenue Intelligence Report",
  "created_at": "2026-05-13T12:00:00Z"
}
```

Field rules:
- `event_type` — exact match against the taxonomy above.
- `project_id`, `client_id` — opaque identifiers. Never raw client names in
  the bus payload; resolve via the Source Registry.
- `created_at` — ISO 8601 UTC.
- Payload fields beyond the envelope are event-type specific and validated
  by a JSON Schema in the Productization Ledger.

## Sample flows

### Flow A — Cost blowout to model routing
```
Event: account_scored                (emitted by Revenue Intelligence agent)
   -> Ledger: AI Run Ledger          (appends run cost, tokens, model)
   -> Metric: AI cost per project    (Metric Engine recomputes)
   -> Threshold: > model budget      (Decision Rule fires)
   -> Decision: route to cheaper tier
   -> Action: Core OS model router updates project profile
```
Outcome: the same workflow continues to run, but on a lower-cost model. The
decision is logged in the Decision Layer and visible in the weekly Decision
Pack.

### Flow B — Proof to productization
```
Event: proof_event_created           (delivered Revenue Intelligence Report)
   -> Ledger: Proof Ledger           (appends proof type, metric, value)
   -> Metric: proof events per project
   -> Threshold: provable across >=3 projects
   -> Decision: this service is provable, promote
   -> Action: Product creates feature candidate, Revenue updates pitch
```
Outcome: a service line is recognised as repeatable and routed toward
productization (see `CAPITAL_ALLOCATION_SCORE.md` for the priority math).

### Flow C — Venture graduation
```
Event: retainer_won + venture_signal_detected
   -> Ledger: Venture Signal Ledger
   -> Metric: Venture Readiness Score
   -> Threshold: score >= 85
   -> Decision: venture candidate
   -> Action: CEO opens graduation review
```
Outcome: the unit enters a venture review per `VENTURE_SIGNAL_MODEL.md`.

## Decision Rules
A Decision Rule is a (metric, threshold, decision-type, owner) tuple. Rules
are versioned and live with their metric in `METRICS_ENGINE.md`. Examples:

| Metric | Threshold | Decision | Owner |
|---|---|---|---|
| AI cost per project | > model budget for 2 runs | Route to cheaper tier | Head of AI Ops |
| Proof events per project | >= 3 across >= 3 projects | Promote service line | Head of Product |
| Schema failure rate | > 2% over 7 days | Halt agent / open eval | Head of AI Ops |
| Retainer win rate | < 20% over 30 days | Review pricing & ICP | Head of Revenue |
| Venture Readiness Score | >= 85 sustained 30 days | Open graduation review | CEO |

## Forbidden patterns
- Emitting events without a project/client identifier.
- Backfilling events after the fact without an Audit Ledger entry.
- Bypassing the bus by writing directly to a ledger.
- Creating ad-hoc dashboards that read from logs instead of ledgers.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Core OS event emissions | Ledger writes | Engineering | Continuous |
| Ledger entries | Metric recomputes | Metric Engine | Continuous / scheduled |
| Metric values + Decision Rules | Decisions | Decision Layer | Per threshold cross |
| Decisions | Core OS instructions | Chief of Staff | Weekly |

## Metrics
- **Event Schema Pass Rate** — share of emitted events passing JSON schema
  validation (target: >=99.5%).
- **Event-to-Decision Latency** — median time from event emission to
  decision dispatch (target: <=24h for weekly cadence rules).
- **Decision Coverage** — share of fired thresholds producing a documented
  decision (target: 100%).
- **Unmapped Event Rate** — share of attempted events whose type is not in
  the taxonomy (target: 0%).

## Related
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability stack carrying events
- `docs/EVALS_RUNBOOK.md` — eval rules feeding agent-related decisions
- `docs/EXECUTIVE_DECISION_PACK.md` — destination of weekly decisions
- `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` — autonomous revenue events
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
