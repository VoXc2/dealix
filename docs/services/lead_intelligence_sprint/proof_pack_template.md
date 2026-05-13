# Proof Pack Template — Lead Intelligence Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** QA Reviewer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [proof_pack_template_AR.md](./proof_pack_template_AR.md)

## Context
The proof pack is the **single auditable artifact** that turns a Dealix Sprint from a vendor invoice into a defensible piece of corporate evidence. This file specializes the master `docs/templates/PROOF_PACK_TEMPLATE.md` for the Lead Intelligence Sprint. It enforces what is measured, how it is anonymized, and what may be re-published on the Dealix trust page. It plugs into the strategic claim ledger in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and the quality regime in `docs/quality/QUALITY_STANDARD_V1.md`.

## Pack Structure
A proof pack is a folder containing:
1. `events.jsonl` — append-only event log.
2. `summary.md` — human-readable summary of the events.
3. `evidence/` — supporting files (anonymized exports, screenshots, signed reports).
4. `signoff.md` — Delivery Lead + QA Reviewer + Client Sponsor signature block.
5. `anonymization_rules.md` — rules applied for any external use.

## Required Events
Every Sprint MUST capture, at minimum, these events. Each event has the schema:
```
{
  "event": "<name>",
  "timestamp": "<ISO8601>",
  "actor_role": "DL|AN|CL|QA|CS|CR",
  "value": <number|bool|string>,
  "notes": "<short freetext>"
}
```

| Event | Value type | Captured by | Phase |
|---|---|---|---|
| `intake_completed` | bool | Sales Engineer | Pre-kickoff |
| `sprint_initialized` | bool | DL | T-1 |
| `rows_imported` | integer | AN | Day 1 |
| `duplicates_removed` | integer | AN | Day 2 |
| `accounts_scored` | integer | AN | Day 3 |
| `top_50_locked` | bool | DL | Day 4 |
| `top_10_action_plan_complete` | bool | DL | Day 4 |
| `drafts_generated` | integer | CL | Day 5 |
| `mini_crm_provisioned` | bool | DL | Day 6 |
| `qa_round_1_complete` | bool | QA | Day 7 |
| `qa_round_1_failures` | integer | QA | Day 7 |
| `client_preview_held` | bool | DL | Day 9 |
| `qa_round_2_complete` | bool | QA | Day 10 |
| `sprint_delivered` | bool | DL | Day 10 |
| `proof_pack_signed_off` | bool | CS | Day 10 |
| `upsell_motion_triggered` | bool | DL/CSM | Day 10 |

## Optional Events (when applicable)
- `sensitive_data_masked` (integer) — fields masked.
- `cross_border_flag_resolved` (bool).
- `pdpl_pre_check_completed` (bool).
- `revision_requests` (integer).

## Anonymization Rules
Anonymization runs **only** when the client signs an explicit publication consent in the SOW or post-delivery.

### Rules
1. **Client name** → replace with `<Sector> client (<Region>)` (e.g., "B2B SaaS client (Riyadh)").
2. **Account names** in top 50 → never published; aggregated counts only.
3. **Numeric metrics** → round to nearest 5% when published.
4. **Date precision** → round to month, not day, when published externally.
5. **PII** → never published in any form.
6. **Sensitive sector flags** (health, government, finance, minors) → published only with an additional written consent.

### What Can Be Published
- Counts: rows imported, duplicates removed, accounts scored, drafts generated.
- Time-to-delivery (days).
- Conversion rate (top 10 acceptance %).
- Buyer testimonial (with named consent).

### What Cannot Be Published
- Top 50 list.
- Individual account names.
- Outreach drafts verbatim.
- Score values per row.
- Source data origin.

## Re-use for Marketing
The proof pack feeds the Dealix trust page only via the **anonymized export script** in `docs/templates/PROOF_PACK_TEMPLATE.md`. No manual extraction. The trust page builder reads the export, not the raw proof pack.

## Storage & Retention
- Stored encrypted at rest in the Dealix vault.
- Access: Delivery Lead, QA Reviewer, Customer Success Manager, Capability Lead.
- Retention: project + 365 days, or project + 30 days if intake flagged sensitive data.
- Deletion: automated on retention expiry; deletion logged.

## Signoff Block
The `signoff.md` file template:
```
## Signoff

- Delivery Lead: <name>, <date>, <signature>
- QA Reviewer: <name>, <date>, <signature>
- Client Sponsor: <name>, <date>, <signature>

This proof pack accurately represents the work delivered in the Lead
Intelligence Sprint for <Client>. Publication is bounded by the
anonymization rules above.
```

## Worked Example (Illustrative — Not a Real Client)
```
{"event":"intake_completed","timestamp":"2026-05-07T10:00:00Z","actor_role":"SE","value":true,"notes":""}
{"event":"rows_imported","timestamp":"2026-05-13T09:12:00Z","actor_role":"AN","value":6431,"notes":"Single XLSX, 11 columns"}
{"event":"duplicates_removed","timestamp":"2026-05-14T16:30:00Z","actor_role":"AN","value":872,"notes":"Email + domain dedupe"}
{"event":"accounts_scored","timestamp":"2026-05-15T18:00:00Z","actor_role":"AN","value":5559,"notes":"Rubric v1.2"}
{"event":"top_50_locked","timestamp":"2026-05-16T17:00:00Z","actor_role":"DL","value":true,"notes":""}
{"event":"drafts_generated","timestamp":"2026-05-17T15:00:00Z","actor_role":"CL","value":16,"notes":"4 seq × 2 lang × 2 versions"}
{"event":"qa_round_1_complete","timestamp":"2026-05-19T17:00:00Z","actor_role":"QA","value":true,"notes":"1 gate failure on tone"}
{"event":"sprint_delivered","timestamp":"2026-05-22T12:00:00Z","actor_role":"DL","value":true,"notes":""}
```

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Real-time event emission | events.jsonl | All roles | Continuous |
| Day-10 review | signoff.md | DL + QA + CS | Day 10 |
| Publication consent | anonymized export | DL + Marketing | Post-delivery |

## Metrics
- **Event capture completeness** — `% required events present at signoff`. Target = 100%.
- **Proof pack signoff lag** — `business days between Day 10 and signoff`. Target ≤ 3.
- **Anonymization audit** — `% packs where anonymization rules apply correctly`. Target = 100%.

## Related
- `docs/templates/PROOF_PACK_TEMPLATE.md` — master scaffold
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/capabilities/revenue_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — revenue playbook
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability
- `docs/COMPANY_SERVICE_LADDER.md` — service ladder
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing ladder
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
