# Intake — AI Governance Program

**Layer:** Service Catalog · Operational Kit
**Owner:** Sales Engineer
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [intake_AR.md](./intake_AR.md)

## Context
Intake decides whether the client's organization is ready for a multi-phase governance build, and what the right governance level (1–5) target is. It surfaces premium triggers and feeds the initial `intake_completed` event per `docs/templates/PROOF_PACK_TEMPLATE.md`. It is the entry to the governance ladder defined in `docs/governance/RUNTIME_GOVERNANCE.md`.

## Intake Goals
1. Confirm AI use inventory is realistic (5–30 uses).
2. Surface regulatory exposure.
3. Identify the DPO, legal counsel, and program sponsor.
4. Set the target governance level (1–5).
5. Produce a signed intake summary.

## Governance Level Scale
- **Level 1**: Ad-hoc — no formal governance, AI used in pockets.
- **Level 2**: Policy-only — AI usage policy exists but unmonitored.
- **Level 3**: Approved use — inventory + approval matrix + risk register.
- **Level 4**: Operationalized — audit cadence + controls matrix + role training.
- **Level 5**: Continuous — monthly governance retainer + board reporting + sector overlays.

Most clients land at Level 3 or 4 after the Program.

## 18-Question Discovery Form

### Section 1 — Sponsor, DPO, Counsel
1. **Legal entity + sponsor name + role.** (required)
2. **DPO (or equivalent) name + role + email.** (required)
3. **Counsel-of-record name + firm.** (required)
4. **Internal program owner if different from sponsor.** (optional)

### Section 2 — AI Tools & Processes
5. **List the AI tools currently in use.** (required, list — count must be 5–30)
6. **For each tool, name the business owner.** (required, structured)
7. **List the AI-touching processes (not just tools).** (required, list)

### Section 3 — Data Flows & Sensitivity
8. **Do AI processes touch sensitive data (PII, health, finance, government, minors)?** (required, yes/no + breakdown)
9. **Where do AI processes run jurisdictionally (KSA only, GCC, international)?** (required, structured)
10. **Are any data flows cross-border?** (required, yes/no + description)

### Section 4 — Existing Posture
11. **Do you have an AI Usage Policy?** (required, yes/no + file if yes)
12. **Do you have a Data Handling Policy?** (required, yes/no)
13. **Do you have an Incident Response Runbook?** (required, yes/no)
14. **Do you have a Vendor / Third-Party Policy?** (required, yes/no)
15. **Do you have an Approval Matrix for new AI use cases?** (required, yes/no)

### Section 5 — Regulatory Pressure & Engagement
16. **What is your sector?** (required, single-select — healthcare/finance/government/etc.)
17. **Are you under any active regulatory engagement (audit, inquiry, certification path)?** (required, yes/no + description)
18. **What is your target governance level after the Program (1–5)?** (required, integer)

## Validation Rules
- AI uses < 5 → route to AI Readiness Review (lighter offer).
- AI uses > 30 → route to scoped Enterprise Governance Engagement.
- Sensitive data = yes → +20–40% premium.
- Multi-jurisdiction = yes → +20–40% premium + multi-jurisdiction overlay.
- Sector premium triggered automatically:
  - Healthcare → +30–50%.
  - Government → +30–50%.
  - Finance → +20–40%.
- Active regulatory engagement → enterprise premium +50–100%.

## Form Fields (Notion DB schema)
| Field | Type | Required |
|---|---|---|
| `client_id` | autogen | yes |
| `legal_name` | string | yes |
| `sponsor_name`, `sponsor_email` | string, email | yes |
| `dpo_name`, `dpo_email` | string, email | yes |
| `counsel_name`, `counsel_firm` | string, string | yes |
| `program_owner` | string | no |
| `ai_tools_list` | list (5–30) | yes |
| `ai_tool_owners` | structured | yes |
| `ai_processes_list` | list | yes |
| `sensitive_data` | bool + breakdown | yes |
| `jurisdictions` | structured | yes |
| `cross_border_flows` | bool + description | yes |
| `has_ai_usage_policy` | bool | yes |
| `has_data_handling_policy` | bool | yes |
| `has_incident_runbook` | bool | yes |
| `has_vendor_policy` | bool | yes |
| `has_approval_matrix` | bool | yes |
| `sector` | single-select | yes |
| `active_regulatory_engagement` | bool + description | yes |
| `target_governance_level` | integer (1–5) | yes |

## Premium Triggers
- Sensitive data → +20–40%.
- Multi-jurisdiction → +20–40%.
- Healthcare / government → +30–50%.
- Finance → +20–40%.
- Enterprise (5,000+ employees) → +50–100%.
- Urgency < 8 weeks → +20–40%.

## Output
- Signed Intake Summary (2 pages).
- SOW with priced band + premiums.
- Initial `intake_completed` proof event.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Qualified lead | Intake call scheduled | Sales Engineer | ≤ 3 days |
| 90-min discovery call | Filled intake | Sales Engineer + Client | One or two sessions |
| Filled intake | SOW | Sales Engineer + Margin Controller | Within 2 days |

## Metrics
- **Intake-to-SOW conversion** — Target ≥ 40%.
- **Intake completeness** — Target = 100%.
- **Governance level fit accuracy** — `% programs where target level matches client's actual readiness`. Target ≥ 80%.

## Related
- `docs/capabilities/governance_capability.md` — capability blueprint
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime governance
- `docs/governance/AI_ACTION_TAXONOMY.md` — action taxonomy
- `docs/governance/AI_ACTION_CONTROL.md` — action control
- `docs/enterprise/CONTROLS_MATRIX.md` — enterprise controls
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — certifications
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
