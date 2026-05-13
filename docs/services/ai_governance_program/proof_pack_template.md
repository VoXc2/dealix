# Proof Pack Template — AI Governance Program

**Layer:** Service Catalog · Operational Kit
**Owner:** QA Reviewer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [proof_pack_template_AR.md](./proof_pack_template_AR.md)

## Context
The single auditable artifact for the AI Governance Program. Specializes the master `docs/templates/PROOF_PACK_TEMPLATE.md` for the governance-tier service. Plugs into the runtime governance regime in `docs/governance/RUNTIME_GOVERNANCE.md` and the strategic claim ledger in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Pack Structure
Folder contains:
1. `events.jsonl` — append-only event log.
2. `summary.md` — human-readable summary.
3. `evidence/` — anonymized inventory excerpts, risk register slices, controls matrix snapshots, audit log samples.
4. `signoff.md` — DL + QA + GR + CL-cap + Sponsor + DPO signature.
5. `anonymization_rules.md`.

## Required Events
| Event | Value type | Captured by | Phase |
|---|---|---|---|
| `intake_completed` | bool | Sales Engineer | Pre-kickoff |
| `program_initialized` | bool | DL | T-1 |
| `ai_uses_inventoried` | integer | GR | Phase 1 |
| `risks_logged` | integer | GR | Phase 1 |
| `data_flows_mapped` | integer | GR | Phase 1 |
| `lawful_basis_documented` | integer | CS-comp | Phase 1 |
| `approvals_documented` | integer | GR | Phase 2 |
| `policy_updates` | integer | CS-comp | Phase 2 |
| `controls_implemented` | integer | GR | Phase 3 |
| `incidents_addressed` | integer | CS-comp | Phase 3 |
| `audit_dry_run_complete` | bool | QA | Phase 3 |
| `training_delivered` | integer (sessions) | GR | Phase 4 |
| `qa_phase_complete` | bool | QA | End of each phase |
| `program_delivered` | bool | DL | Phase 4 |
| `proof_pack_signed_off` | bool | Sponsor + DPO | Final week |
| `upsell_motion_triggered` | bool | DL/CSM | Final week |

## Optional Events
- `sensitive_data_masked` (integer).
- `clinics_overlay_applied` (bool).
- `government_overlay_applied` (bool).
- `cross_border_flag_resolved` (bool).

## Anonymization Rules
Runs only on explicit publication consent. Given the sensitivity of governance content, the default is **no publication**; trust-page use requires extra written consent.

### Rules
1. Client name → `<Sector> enterprise (<Region>)`.
2. AI tool names → genericized ("LLM tool", "transcription tool").
3. Policy text → never quoted verbatim.
4. Risk register contents → never quoted.
5. Controls matrix detail → only structural counts publishable, never specific rows.
6. Counts → rounded to nearest 5.
7. PII → never published.
8. Sector overlays (clinics, government, finance) → published only with extra consent.

### What Can Be Published
- AI uses inventoried (rounded).
- Risks logged (rounded).
- Controls implemented (rounded).
- Approvals documented (rounded).
- Training sessions delivered (rounded).
- Sector-agnostic governance maturity move (e.g., "from Level 2 to Level 4").
- Buyer testimonial (with extra consent).

### What Cannot Be Published
- Policy text.
- Risk register details.
- Controls matrix details.
- Counsel identity.
- Regulatory engagement details.

## Re-use for Marketing
Pack feeds the trust page only via the anonymized export script + sector consent. No manual extraction.

## Storage & Retention
- Encrypted at rest in Dealix vault.
- Access: DL, QA, GR, CL-cap, CSM, Capability Lead.
- Retention: project + 365 days; sensitive subsets = project + 60 days.
- Deletion logged.

## Signoff Block Template
```
## Signoff
- Delivery Lead: <name>, <date>, <signature>
- QA Reviewer: <name>, <date>, <signature>
- Governance Reviewer: <name>, <date>, <signature>
- Capability Lead: <name>, <date>, <signature>
- Sponsor: <name>, <date>, <signature>
- DPO: <name>, <date>, <signature>

This proof pack accurately represents the AI Governance Program delivered
for <Client>. Publication is bounded by anonymization_rules.md. This pack
does not constitute legal advice.
```

## Worked Example (Illustrative)
```
{"event":"ai_uses_inventoried","timestamp":"2026-05-22T17:00:00Z","actor_role":"GR","value":22,"notes":"Across 4 depts"}
{"event":"risks_logged","timestamp":"2026-05-23T17:00:00Z","actor_role":"GR","value":28,"notes":"Top 30 attempted; 28 ranked"}
{"event":"lawful_basis_documented","timestamp":"2026-05-26T15:00:00Z","actor_role":"CS-comp","value":15,"notes":"15 datasets"}
{"event":"approvals_documented","timestamp":"2026-06-05T16:00:00Z","actor_role":"GR","value":34,"notes":"34 use case patterns"}
{"event":"policy_updates","timestamp":"2026-06-10T15:00:00Z","actor_role":"CS-comp","value":5,"notes":""}
{"event":"controls_implemented","timestamp":"2026-06-19T17:00:00Z","actor_role":"GR","value":41,"notes":""}
{"event":"audit_dry_run_complete","timestamp":"2026-06-20T16:00:00Z","actor_role":"QA","value":true,"notes":"3 uses audited"}
{"event":"training_delivered","timestamp":"2026-07-03T15:00:00Z","actor_role":"GR","value":4,"notes":"exec, owner, builder, user"}
{"event":"program_delivered","timestamp":"2026-07-10T12:00:00Z","actor_role":"DL","value":true,"notes":""}
```

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Real-time event emission | events.jsonl | All roles | Continuous |
| Final week review | signoff.md | All signatories | Final week |
| Publication consent | anonymized export | DL + Marketing | Post-delivery |

## Metrics
- **Event capture completeness** — Target = 100%.
- **Signoff lag** — Target ≤ 5 business days.
- **Anonymization audit** — Target = 100%.
- **Publication leak** — `count of publications without dual consent`. Target = 0.

## Related
- `docs/templates/PROOF_PACK_TEMPLATE.md` — master scaffold
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/capabilities/governance_capability.md` — capability blueprint
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime governance
- `docs/governance/AI_ACTION_TAXONOMY.md` — action taxonomy
- `docs/governance/AI_ACTION_CONTROL.md` — action control
- `docs/enterprise/CONTROLS_MATRIX.md` — enterprise controls
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — compliance
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
