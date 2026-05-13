# Proof Pack Template — AI Support Desk Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** QA Reviewer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [proof_pack_template_AR.md](./proof_pack_template_AR.md)

## Context
The single auditable artifact for the AI Support Desk Sprint. Specializes the master `docs/templates/PROOF_PACK_TEMPLATE.md` for the customer-tier service. Plugs into `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` and the strategic claim ledger in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Pack Structure
Folder contains:
1. `events.jsonl` — append-only event log.
2. `summary.md` — human-readable summary.
3. `evidence/` — anonymized category samples, reply library snapshots, escalation log.
4. `signoff.md` — DL + QA + GR + SL + Sponsor signature.
5. `anonymization_rules.md`.

## Required Events
| Event | Value type | Captured by | Phase |
|---|---|---|---|
| `intake_completed` | bool | Sales Engineer | Pre-kickoff |
| `sprint_initialized` | bool | DL | T-1 |
| `messages_classified` | integer | AN | Days 1–3 |
| `category_coverage` | decimal (%) | AN | Days 1–3 |
| `replies_drafted` | integer | CL | Days 4–7 |
| `escalations_routed` | integer | GR | Days 8–10 |
| `sensitive_blocks` | integer | GR | Days 8–10 |
| `auto_send_incidents` | integer | QA | Ongoing |
| `qa_round_1_complete` | bool | QA | Day 12 |
| `qa_round_2_complete` | bool | QA | Day 14 |
| `sprint_delivered` | bool | DL | Day 14 |
| `proof_pack_signed_off` | bool | Sponsor | Day 14 |
| `upsell_motion_triggered` | bool | DL/CSM | Day 14 |

## Optional Events
- `sensitive_data_masked` (integer).
- `clinics_playbook_applied` (bool) — when clinics premium triggered.
- `cross_border_flag_resolved` (bool).

## Anonymization Rules
Runs only on explicit publication consent.

### Rules
1. Client name → `<Sector> client (<Region>)`.
2. Customer message text → never quoted verbatim.
3. Reply library text → never quoted verbatim.
4. Counts → rounded to nearest 5.
5. PII → never published.
6. Sensitive categories (clinics, finance, complaints) → only published with extra consent.

### What Can Be Published
- Categories covered (rounded count).
- Coverage % (rounded).
- Replies drafted (rounded count).
- Escalations routed (rounded count).
- Buyer testimonial (with consent).

### What Cannot Be Published
- Customer message text.
- Reply library text verbatim.
- Sensitive case examples.
- Escalation contact identities.

## Re-use for Marketing
Pack feeds the trust page only via the anonymized export script. No manual extraction.

## Storage & Retention
- Encrypted at rest.
- Access: DL, QA, GR, CSM, Capability Lead.
- Retention: project + 365 days; sensitive flag or clinics premium = project + 30 days.
- Deletion logged.

## Signoff Block Template
```
## Signoff
- Delivery Lead: <name>, <date>, <signature>
- QA Reviewer: <name>, <date>, <signature>
- Governance Reviewer: <name>, <date>, <signature>
- Support Lead: <name>, <date>, <signature>
- Sponsor: <name>, <date>, <signature>

This proof pack accurately represents the AI Support Desk Sprint delivered
for <Client>. Publication is bounded by anonymization_rules.md.
```

## Worked Example (Illustrative)
```
{"event":"messages_classified","timestamp":"2026-05-15T17:00:00Z","actor_role":"AN","value":4823,"notes":""}
{"event":"category_coverage","timestamp":"2026-05-15T17:00:00Z","actor_role":"AN","value":92.4,"notes":"holdout"}
{"event":"replies_drafted","timestamp":"2026-05-19T16:00:00Z","actor_role":"CL","value":78,"notes":"39 categories × 2 langs"}
{"event":"escalations_routed","timestamp":"2026-05-22T15:00:00Z","actor_role":"GR","value":6,"notes":"sensitive types"}
{"event":"sensitive_blocks","timestamp":"2026-05-22T15:00:00Z","actor_role":"GR","value":0,"notes":"no auto-reply to sensitive in tests"}
{"event":"auto_send_incidents","timestamp":"2026-05-26T12:00:00Z","actor_role":"QA","value":0,"notes":""}
{"event":"sprint_delivered","timestamp":"2026-05-26T15:00:00Z","actor_role":"DL","value":true,"notes":""}
```

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Real-time event emission | events.jsonl | All roles | Continuous |
| Day 14 review | signoff.md | All signatories | Day 14 |
| Publication consent | anonymized export | DL + Marketing | Post-delivery |

## Metrics
- **Event capture completeness** — Target = 100%.
- **Signoff lag** — Target ≤ 3 business days.
- **Anonymization audit** — Target = 100%.
- **Auto-send incidents in production retainer** — Target = 0.

## Related
- `docs/templates/PROOF_PACK_TEMPLATE.md` — master scaffold
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/capabilities/customer_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` — HITL rules
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — CS playbook
- `docs/playbooks/clinics_playbook.md` — clinics premium
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
