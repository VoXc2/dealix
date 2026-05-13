# Proof Pack Template — AI Quick Win Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** QA Reviewer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [proof_pack_template_AR.md](./proof_pack_template_AR.md)

## Context
The proof pack is the single auditable artifact that turns a 7-day workflow win into defensible corporate evidence. This file specializes the master `docs/templates/PROOF_PACK_TEMPLATE.md` for the AI Quick Win Sprint. It enforces what is measured, anonymized, and re-publishable. It plugs into the strategic claim ledger in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Pack Structure
A proof pack folder contains:
1. `events.jsonl` — append-only event log.
2. `summary.md` — human-readable summary.
3. `evidence/` — anonymized screenshots, SOP final, before/after timings.
4. `signoff.md` — DL + QA + Workflow Owner + Sponsor signature block.
5. `anonymization_rules.md` — rules for any external use.

## Required Events
| Event | Value type | Captured by | Phase |
|---|---|---|---|
| `intake_completed` | bool | Sales Engineer | Pre-kickoff |
| `sprint_initialized` | bool | DL | T-1 |
| `workflow_mapped` | bool | DS | Day 1 |
| `baseline_measured` | decimal (hours/cycle) | DS | Day 2 |
| `ai_step_designed` | bool | DS | Day 3 |
| `draft_built` | bool | DS | Day 4 |
| `owner_reviewed` | bool | WO | Day 5 |
| `test_cycle_complete` | bool | WO | Day 6 |
| `manual_steps_reduced` | integer | WO + DS | Day 6 |
| `hours_saved` | decimal | DL | Day 7 |
| `workflow_created` | bool | DS | Day 7 |
| `qa_complete` | bool | QA | Day 7 |
| `sprint_delivered` | bool | DL | Day 7 |
| `proof_pack_signed_off` | bool | SP | Day 7 |
| `upsell_motion_triggered` | bool | DL/CSM | Day 7 |

## Optional Events
- `sensitive_data_masked` (integer).
- `cross_border_flag_resolved` (bool).
- `revisions_applied` (integer).

## Anonymization Rules
Runs only on explicit publication consent.

### Rules
1. Client name → `<Sector> client (<Region>)`.
2. Workflow name → generic descriptor ("invoicing review", "monthly KPI report").
3. Numeric metrics → round to nearest 0.5 hour or 5%.
4. Date precision → round to month.
5. PII → never published.
6. Tool names → kept only with consent.

### What Can Be Published
- Hours saved per cycle (rounded).
- Cycles run on the new flow.
- Owner role (e.g., "Finance Manager"), never owner name.
- Buyer testimonial (with consent).

### What Cannot Be Published
- Workflow internal logic.
- Prompts used.
- Tool credentials or workspace names.
- Detailed before/after timings beyond aggregates.

## Re-use for Marketing
Pack feeds the trust page only via the anonymized export script. No manual extraction.

## Storage & Retention
- Encrypted at rest in Dealix vault.
- Access: DL, QA, CSM, Capability Lead.
- Retention: project + 365 days; sensitive flag = project + 30 days.
- Deletion logged on retention expiry.

## Signoff Block Template
```
## Signoff
- Delivery Lead: <name>, <date>, <signature>
- QA Reviewer: <name>, <date>, <signature>
- Workflow Owner: <name>, <date>, <signature>
- Sponsor: <name>, <date>, <signature>

This proof pack accurately represents the AI Quick Win Sprint delivered
for <Client>. Publication is bounded by anonymization_rules.md.
```

## Worked Example (Illustrative)
```
{"event":"workflow_mapped","timestamp":"2026-05-13T11:00:00Z","actor_role":"DS","value":true,"notes":"Monthly KPI review workflow"}
{"event":"baseline_measured","timestamp":"2026-05-14T16:00:00Z","actor_role":"DS","value":3.5,"notes":"hours per cycle, n=1"}
{"event":"ai_step_designed","timestamp":"2026-05-15T15:00:00Z","actor_role":"DS","value":true,"notes":"Approval gate before report send"}
{"event":"draft_built","timestamp":"2026-05-16T17:00:00Z","actor_role":"DS","value":true,"notes":""}
{"event":"owner_reviewed","timestamp":"2026-05-17T15:00:00Z","actor_role":"WO","value":true,"notes":"3 revisions"}
{"event":"test_cycle_complete","timestamp":"2026-05-18T17:00:00Z","actor_role":"WO","value":true,"notes":"new cycle = 1.2h"}
{"event":"hours_saved","timestamp":"2026-05-19T12:00:00Z","actor_role":"DL","value":2.3,"notes":"per monthly cycle"}
{"event":"sprint_delivered","timestamp":"2026-05-19T16:00:00Z","actor_role":"DL","value":true,"notes":""}
```

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Real-time event emission | events.jsonl | All roles | Continuous |
| Day-7 review | signoff.md | DL + QA + WO + SP | Day 7 |
| Publication consent | anonymized export | DL + Marketing | Post-delivery |

## Metrics
- **Event capture completeness** — Target = 100%.
- **Signoff lag** — Target ≤ 2 business days.
- **Anonymization audit** — Target = 100%.

## Related
- `docs/templates/PROOF_PACK_TEMPLATE.md` — master scaffold
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/capabilities/operations_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/product/WORKFLOW_RUNTIME_DESIGN.md` — runtime design
- `docs/product/PRODUCTIZATION_LEDGER.md` — productization ledger
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/AI_STACK_DECISIONS.md` — approved stack
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
