# Intake — Company Brain Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Sales Engineer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [intake_AR.md](./intake_AR.md)

## Context
Intake decides whether the client's document corpus is realistic for a 3–4 week Sprint and whether the governance regime is mature enough to support a citation-bearing assistant. It surfaces premium triggers and feeds the initial proof pack `intake_completed` event per `docs/templates/PROOF_PACK_TEMPLATE.md`. It plugs into the governance regime in `docs/governance/AI_INFORMATION_GOVERNANCE.md`.

## Intake Goals
1. Confirm a document corpus that fits the 50–200 range.
2. Confirm sensitivity-tagging capability.
3. Identify user groups and a single knowledge owner.
4. Surface freshness expectations.
5. Produce a signed intake summary.

## 14-Question Discovery Form

### Section 1 — Sponsor & Owner
1. **Legal entity + sponsor name + role.** (required)
2. **Knowledge owner name + role + email.** (required — usually Chief of Staff or Head of Operations)
3. **Outcome that defines success?** (required, free text ≤ 200 chars)

### Section 2 — Document Volume & Types
4. **How many documents do you want in this Sprint?** (required, integer 50–200)
5. **What types of documents?** (required, multi-select: policy / SOP / contract templates / pricing / playbooks / FAQs / training materials / other)
6. **Where do they currently live?** (required, multi-select: Notion / Drive / SharePoint / Confluence / file shares / inboxes / other)
7. **Can you export them in 3 business days?** (required, yes/no)

### Section 3 — Sensitivity
8. **Do any documents contain sensitive data (health, finance, government, minors, customer PII)?** (required, yes/no — yes triggers sensitivity premium)
9. **Do any documents have lawful-basis restrictions on access?** (required, free text)

### Section 4 — Users & Groups
10. **List the user groups you want to serve.** (required, list — max 3 in scope)
11. **For each group, list what they may see and what they may NOT see.** (required, structured)

### Section 5 — Discovery Pain
12. **Describe the current pain — where do people get stuck looking for answers?** (required, free text)
13. **How often must the answer be fresh (within X days)?** (required, integer days)

### Section 6 — Success Metric
14. **What metric would you report internally for the Sprint?** (required, free text)

## Validation Rules
- Document count must be 50–200. Outside → scoped engagement.
- Sensitivity = yes → +20–40% premium and PDPL pre-check (`docs/ops/PDPL_RETENTION_POLICY.md`).
- User groups > 3 → +15–30% premium.
- Documents in > 4 source systems → +10% premium for ingestion complexity.

## Form Fields (Notion DB schema)
| Field | Type | Required |
|---|---|---|
| `client_id` | autogen | yes |
| `legal_name` | string | yes |
| `sponsor_name`, `sponsor_email` | string, email | yes |
| `knowledge_owner_name`, `knowledge_owner_email` | string, email | yes |
| `success_outcome` | text | yes |
| `document_count` | integer | yes |
| `document_types` | multi-select | yes |
| `source_systems` | multi-select | yes |
| `export_ready` | bool | yes |
| `sensitive_data` | bool | yes |
| `lawful_basis_restrictions` | text | yes |
| `user_groups` | list | yes |
| `group_permissions` | structured | yes |
| `discovery_pain` | text | yes |
| `freshness_days` | integer | yes |
| `success_metric` | text | yes |

## Premium Triggers
- Sensitive = yes → +20–40%.
- User groups > 3 → +15–30%.
- Source systems > 4 → +10%.
- Urgency < 3 weeks → +20–50%.

## Output
- Signed Intake Summary.
- SOW with priced band + premiums.
- Initial proof event `intake_completed`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Qualified lead | Intake call scheduled | Sales Engineer | ≤ 2 days |
| 60-min discovery call | Filled intake | Sales Engineer + Client | One session |
| Filled intake | SOW | Sales Engineer + Margin Controller | Same day |

## Metrics
- **Intake-to-SOW conversion** — Target ≥ 45%.
- **Intake completeness** — Target = 100%.
- **Corpus right-sizing** — `% intakes where final corpus stayed within ±10% of intake estimate`. Target ≥ 80%.

## Related
- `docs/capabilities/knowledge_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/governance/AI_INFORMATION_GOVERNANCE.md` — governance regime
- `docs/ledgers/SOURCE_REGISTRY.md` — source registry
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — model routing
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/AI_STACK_DECISIONS.md` — approved stack
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
