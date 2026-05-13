# Proof Pack Template — Company Brain Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** QA Reviewer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [proof_pack_template_AR.md](./proof_pack_template_AR.md)

## Context
The single auditable artifact for the Company Brain Sprint. Specializes the master `docs/templates/PROOF_PACK_TEMPLATE.md` to the knowledge-tier service. Connects to `docs/governance/AI_INFORMATION_GOVERNANCE.md` and the strategic claim ledger in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`.

## Pack Structure
Folder containing:
1. `events.jsonl` — append-only event log.
2. `summary.md` — human-readable summary.
3. `evidence/` — coverage map, citation samples (anonymized), governance log excerpts.
4. `signoff.md` — DL + QA + GR + KO + Sponsor signature.
5. `anonymization_rules.md`.

## Required Events
| Event | Value type | Captured by | Phase |
|---|---|---|---|
| `intake_completed` | bool | Sales Engineer | Pre-kickoff |
| `sprint_initialized` | bool | DL | T-1 |
| `documents_indexed` | integer | KE | Week 1 |
| `source_registry_complete` | bool | KE + GR | Week 1 |
| `index_tuned` | bool | KE | Week 2 |
| `permission_model_implemented` | bool | GR | Week 2 |
| `answers_with_sources` | integer | KE | Week 3 |
| `insufficient_evidence_responses` | integer | KE | Week 3 |
| `hallucinated_citations` | integer | QA | Week 3 |
| `blocked_unauthorized_accesses` | integer | GR | Week 4 |
| `qa_round_1_complete` | bool | QA | End Week 3 |
| `qa_round_2_complete` | bool | QA | End Week 4 |
| `sprint_delivered` | bool | DL | Week 4 |
| `proof_pack_signed_off` | bool | Sponsor | Week 4 |
| `upsell_motion_triggered` | bool | DL/CSM | Week 4 |

## Optional Events
- `sensitive_data_masked` (integer).
- `freshness_flags_raised` (integer).
- `cross_border_flag_resolved` (bool).

## Anonymization Rules
Runs only on explicit publication consent.

### Rules
1. Client name → `<Sector> client (<Region>)`.
2. Document titles → never published verbatim.
3. Source-system identities (Notion workspace name, Drive path) → masked.
4. Citation samples → reworded to avoid quoting verbatim policy text.
5. Counts → rounded to nearest 5.
6. PII → never published.

### What Can Be Published
- Documents indexed (rounded).
- Answers with sources (rounded percent).
- Insufficient-evidence rate (rounded percent).
- Buyer testimonial (with consent).
- Coverage-map shape (sector-agnostic).

### What Cannot Be Published
- Document titles.
- Citation text verbatim.
- Source-system internal identifiers.
- Permission-model details.
- User-group definitions.

## Re-use for Marketing
Pack feeds the trust page only via the anonymized export script. No manual extraction.

## Storage & Retention
- Encrypted at rest.
- Access: DL, QA, GR, CSM, Capability Lead.
- Retention: project + 365 days; sensitive flag = project + 30 days.
- Deletion logged.

## Signoff Block Template
```
## Signoff
- Delivery Lead: <name>, <date>, <signature>
- QA Reviewer: <name>, <date>, <signature>
- Governance Reviewer: <name>, <date>, <signature>
- Knowledge Owner: <name>, <date>, <signature>
- Sponsor: <name>, <date>, <signature>

This proof pack accurately represents the Company Brain Sprint delivered
for <Client>. Publication is bounded by anonymization_rules.md.
```

## Worked Example (Illustrative)
```
{"event":"documents_indexed","timestamp":"2026-05-15T17:00:00Z","actor_role":"KE","value":142,"notes":"3 source systems"}
{"event":"source_registry_complete","timestamp":"2026-05-16T16:00:00Z","actor_role":"KE","value":true,"notes":""}
{"event":"index_tuned","timestamp":"2026-05-22T17:00:00Z","actor_role":"KE","value":true,"notes":"chunk=512, top_k=5"}
{"event":"answers_with_sources","timestamp":"2026-05-29T17:00:00Z","actor_role":"KE","value":287,"notes":"out of 300 test queries"}
{"event":"insufficient_evidence_responses","timestamp":"2026-05-29T17:00:00Z","actor_role":"KE","value":13,"notes":""}
{"event":"hallucinated_citations","timestamp":"2026-05-29T17:00:00Z","actor_role":"QA","value":0,"notes":""}
{"event":"blocked_unauthorized_accesses","timestamp":"2026-06-05T15:00:00Z","actor_role":"GR","value":7,"notes":"test users"}
{"event":"sprint_delivered","timestamp":"2026-06-08T12:00:00Z","actor_role":"DL","value":true,"notes":""}
```

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Real-time event emission | events.jsonl | All roles | Continuous |
| End-Week-4 review | signoff.md | All signatories | End Week 4 |
| Publication consent | anonymized export | DL + Marketing | Post-delivery |

## Metrics
- **Event capture completeness** — Target = 100%.
- **Signoff lag** — Target ≤ 3 business days.
- **Anonymization audit** — Target = 100%.

## Related
- `docs/templates/PROOF_PACK_TEMPLATE.md` — master scaffold
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/capabilities/knowledge_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/governance/AI_INFORMATION_GOVERNANCE.md` — governance
- `docs/ledgers/SOURCE_REGISTRY.md` — source registry
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — routing
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
