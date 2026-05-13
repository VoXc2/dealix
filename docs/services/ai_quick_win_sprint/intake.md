# Intake — AI Quick Win Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Sales Engineer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [intake_AR.md](./intake_AR.md)

## Context
The intake decides whether a workflow is small enough, owned enough, and safe enough for a 7-day Sprint. It surfaces premium triggers and protects against scope creep. It feeds the proof pack `intake_completed` event per `docs/templates/PROOF_PACK_TEMPLATE.md` and is the gate to the productization ledger in `docs/product/PRODUCTIZATION_LEDGER.md`.

## Intake Goals
1. Confirm one workflow that meets the "weekly + ≥ 1h + named owner" rule.
2. Surface risk and sensitivity triggers.
3. Capture baseline (current time per cycle, frequency).
4. Identify the workflow owner who will be present 1h/day.
5. Produce a signed intake summary.

## 12-Question Discovery Form

### Section 1 — Sponsor & Owner
1. **Legal entity + sponsor name + role.** (required)
2. **Workflow owner name + role + email.** (required — must NOT be the sponsor unless they will personally run the test cycle)

### Section 2 — Workflow Selection
3. **Which weekly process do you want to attack?** (required, free text + name)
4. **How often does it run (per week)?** (required, integer ≥ 1)
5. **How many hours does one cycle currently take?** (required, decimal ≥ 1.0)
6. **Who currently performs it?** (required, role or name)

### Section 3 — Sensitivity & Risk
7. **Does the workflow handle sensitive data (health, finance, PII, government)?** (required, yes/no — yes triggers sensitivity premium)
8. **Does it touch customers directly (auto-send, auto-respond)?** (required, yes/no — yes triggers a re-scope to a different service)
9. **What approval points exist today, if any?** (required, free text)

### Section 4 — Tools & Environment
10. **List the tools used in this workflow.** (required, multi-select: Notion, Sheets, Slack, Outlook, custom, other)
11. **Do you have sample inputs and outputs we can use?** (required, yes/no — no triggers a scoping risk flag)

### Section 5 — Success Metric
12. **What time-saving (hours/cycle) would make this Sprint a success in your eyes?** (required, decimal ≥ 0.5)

## Validation Rules
- Workflow must run ≥ once a week.
- Current cycle ≥ 1.0 hour.
- Workflow owner must NOT be the sponsor unless they personally run the cycle.
- Customer-facing workflows are rejected from this Sprint and routed to AI Support Desk or Pilot.
- High-risk auto-action workflows are rejected.
- Sensitive data triggers a +20–40% premium and a PDPL pre-check.

## Form Fields (Notion DB schema)
| Field | Type | Required |
|---|---|---|
| `client_id` | autogen | yes |
| `legal_name` | string | yes |
| `sponsor_name`, `sponsor_email` | string, email | yes |
| `owner_name`, `owner_email` | string, email | yes |
| `workflow_name` | string | yes |
| `frequency_per_week` | integer | yes |
| `current_hours_per_cycle` | decimal | yes |
| `current_performer` | string | yes |
| `sensitive_data` | bool | yes |
| `customer_facing` | bool | yes |
| `approval_points` | text | yes |
| `tools_used` | multi-select | yes |
| `samples_available` | bool | yes |
| `success_target_hours_saved` | decimal | yes |
| `urgency_days` | integer | no |

## Premium Triggers
- Sensitive = yes → +20–40%.
- Urgency < 7 days → +20–50%.
- Stakeholders > 3 → +15–30%.

## Output
- Signed Intake Summary (1 page PDF).
- Auto-generated SOW with priced band + premiums.
- Initial proof event `intake_completed`.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Qualified lead | Intake call scheduled | Sales Engineer | ≤ 2 days |
| 30-min discovery call | Filled intake | Sales Engineer + Client | One session |
| Filled intake | SOW | Sales Engineer + Margin Controller | Same day |

## Metrics
- **Intake-to-SOW conversion** — Target ≥ 55%.
- **Intake completeness** — Target = 100%.
- **Workflow rejection rate** — `% intakes rejected due to wrong-fit workflow`. Target ≤ 15% (a healthy gate, not an indictment).

## Related
- `docs/capabilities/operations_capability.md` — capability blueprint
- `docs/company/CAPABILITY_VALUE_MAP.md` — capability map
- `docs/product/WORKFLOW_RUNTIME_DESIGN.md` — runtime design
- `docs/product/PRODUCTIZATION_LEDGER.md` — productization ledger
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/AI_STACK_DECISIONS.md` — approved stack
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
