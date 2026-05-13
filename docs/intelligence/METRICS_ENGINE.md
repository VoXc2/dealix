# Metrics Engine — Intelligence · Operating Brain

**Layer:** Intelligence · Operating Brain
**Owner:** Head of Data
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [METRICS_ENGINE_AR.md](./METRICS_ENGINE_AR.md)

## Context
The Metrics Engine converts ledger entries into indicators that the
Decision Layer can act on. Every ledger has a curated set of metrics, each
with a definition, a unit, a refresh cadence, and a Decision Rule. This is
the catalog of what Dealix watches and why. Without a single canonical
metric catalog, the company drifts into ad-hoc dashboards where the same
indicator is computed three different ways and decisions become unreliable.
See `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` for the surfaced KPI dashboard,
`docs/FINANCE_DASHBOARD.md` for the finance surface, and
`docs/AI_OBSERVABILITY_AND_EVALS.md` for the AI Run metric definitions.

## Engine principles
- **One definition per metric.** Every metric has a single SQL definition
  in the metrics repo. No client of the engine recomputes its own version.
- **Ledger-rooted.** Every metric resolves to one or more ledgers from
  `LEDGER_ARCHITECTURE.md`. No metric reads from application databases.
- **Versioned.** Definitions are versioned; a metric change requires a
  Decision Layer announcement and a 7-day grace window.
- **Cadence-typed.** Each metric has a refresh class — continuous, hourly,
  daily, weekly — driven by its Decision Rule sensitivity.
- **Decision-linked.** Every metric exists because a Decision Rule needs
  it. Orphan metrics are deprecated.

## Catalog by ledger

### AI Run metrics
Source: AI Run Ledger.

| Metric | Definition | Cadence | Decision Rule |
|---|---|---|---|
| AI cost per project | sum(`cost_usd`) grouped by `project_id` | Hourly | Exceed budget → route to cheaper tier |
| AI cost per workflow | sum(`cost_usd`) grouped by `agent_id` + workflow tag | Daily | Top-quartile cost → optimization sprint |
| QA pass rate | share of runs with `eval_verdict=pass` | Daily | <90% → halt agent, open eval |
| Schema failure rate | share of runs with `schema_valid=false` | Continuous | >2% over 7d → halt agent |
| Model fallback rate | share of runs with fallback model | Daily | Sustained >15% → retrain router |
| High-risk run count | count of runs flagged high-risk | Hourly | >0 → approval required |

### Governance metrics
Source: Audit Ledger.

| Metric | Definition | Cadence | Decision Rule |
|---|---|---|---|
| Blocked actions | count by policy ref | Daily | Spike → policy review |
| Approval delays | median time `approval_required` → `approval_granted` | Daily | >24h → escalate |
| PII flags | count of `pii_detected` events | Continuous | >0 → governance review |
| Source attribution coverage | share of outputs with verifiable source | Daily | <95% → source check |
| Audit coverage | share of agent actions audited | Daily | <100% → block deployment |
| Policy violations | count of failed governance checks | Continuous | >0 → incident |

### Proof metrics
Source: Proof Ledger.

| Metric | Definition | Cadence | Decision Rule |
|---|---|---|---|
| Proof packs per project | count of proof events grouped by `project_id` | Weekly | <2 → delivery review |
| Proof events per project | total client-confirmed proofs | Weekly | >=3 across >=3 projects → promote |
| Value categories covered | distinct `proof_type` per service line | Weekly | <3 → diversify proof |
| Client-approved proof count | proofs with `client_approved=true` | Weekly | Trend → case study queue |
| Proof-to-retainer conversion | retainer wins / proof packs delivered | Monthly | <30% → pitch fix |

### Capital metrics
Source: Capital Ledger.

| Metric | Definition | Cadence | Decision Rule |
|---|---|---|---|
| Assets per project | count grouped by `project_id` | Weekly | <2 → delivery review |
| Reusable assets ratio | reusable / total | Monthly | <60% → productization push |
| Playbook updates | count of `playbook_updated` events | Weekly | None → memory gap |
| Feature candidates | open candidates in Productization Ledger | Weekly | Top-3 → roadmap |
| Market-safe insights | count of `market_safe=true` assets | Monthly | >0 → content queue |

### Product metrics
Source: Productization Ledger + Capital Ledger + AI Run Ledger.

| Metric | Definition | Cadence | Decision Rule |
|---|---|---|---|
| Manual hours saved | estimated hours saved by released modules | Monthly | <expected → adoption push |
| Feature reuse rate | share of modules used in >=3 projects | Monthly | <50% → kill or scope |
| Internal tool usage | active users per internal tool | Weekly | <50% team → adoption |
| Module adoption | external adoption rate | Monthly | <20% → repackage |
| Delivery time reduction | median delivery time vs baseline | Quarterly | <10% reduction → process review |

### Business Unit metrics
Source: Unit Performance Ledger + cross-ledger joins.

| Metric | Definition | Cadence | Decision Rule |
|---|---|---|---|
| Unit revenue | sum(`revenue`) per `unit_id` | Monthly | Below target → revenue plan |
| Unit margin | unit margin % | Monthly | <target → cost review |
| Unit QA | average `qa_score` | Monthly | <target → delivery training |
| Unit proof count | count from Proof Ledger | Monthly | <2/project avg → proof discipline |
| Unit retainer count | count of `retainer_won` | Monthly | Trend down → pricing/ICP review |
| Unit product maturity | productization score 0-100 | Quarterly | >=70 → graduation review |
| Unit playbook maturity | playbook coverage score 0-100 | Quarterly | >=70 → graduation review |

## Refresh cadence map
| Class | Examples | Trigger |
|---|---|---|
| Continuous | Schema failure rate, PII flags | On every relevant event |
| Hourly | AI cost per project, high-risk run count | Hourly batch |
| Daily | QA pass rate, blocked actions | 02:00 Riyadh |
| Weekly | Proof packs per project, capital assets | Monday 06:00 |
| Monthly | Unit margin, product adoption | 1st 06:00 |
| Quarterly | Unit maturity scores | 1st of quarter 06:00 |

## Metric lifecycle
1. **Propose** — owner submits a definition + Decision Rule.
2. **Validate** — Head of Data checks ledger feasibility and join cost.
3. **Publish** — definition lands in the metrics repo, versioned.
4. **Wire** — Decision Layer attaches the rule.
5. **Review** — quarterly review; deprecate orphan metrics.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Ledger entries | Metric values | Head of Data | Per cadence class |
| Decision Rules | Metric thresholds | Chief of Staff | At rule change |
| Dashboards | Surfaced indicators | Heads | Per dashboard cadence |
| Quarterly review | Metric deprecations | CEO + Head of Data | Quarterly |

## Metrics
- **Metric Freshness** — share of metrics within their cadence SLO
  (target: >=99%).
- **Definition Drift** — count of clients computing a metric off-engine
  (target: 0).
- **Orphan Metric Count** — metrics without a Decision Rule
  (target: 0).
- **Recompute Latency** — p95 recompute time per class.

## Related
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — surfaced KPI dashboard
- `docs/FINANCE_DASHBOARD.md` — finance surface fed by Unit Performance metrics
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — AI Run metric definitions
- `docs/EVALS_RUNBOOK.md` — eval-driven metrics
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
