# Data Request — AI Quick Win Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Analyst
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [data_request_AR.md](./data_request_AR.md)

## Context
The client-facing checklist of what Dealix needs before Day 1. The Sprint is short (7 days); every late item compresses delivery time. This document enforces the DPA in `docs/DPA_DEALIX_FULL.md` and the retention regime in `docs/ops/PDPL_RETENTION_POLICY.md`. It is consumed in the operations capability blueprint via `docs/capabilities/operations_capability.md`.

## Summary
Client provides:
1. **Process documentation** of the chosen workflow.
2. **Sample inputs and outputs** (anonymized OK).
3. **Owner contact details** + their daily availability window.
4. **Current tool list** + access notes.
5. **Signed data handling acknowledgement** (auto-generated from intake).

Time budget: **≤ 1 business day**.

## Item 1 — Process Documentation

### Minimum Content
- A description of the workflow in 1 page or less.
- Step-by-step list of what the current performer does.
- Decisions made at each step.
- Tools touched at each step.
- Outputs handed to whom.

### Acceptable Formats
- PDF, DOCX, Notion page link, Loom video link.
- Bullet list in an email is fine for simple workflows.

### What We'll Do With It
- Produce a workflow map.
- Identify the candidate AI step.
- Design the human approval gate.

## Item 2 — Sample Inputs and Outputs

### Required
- **At least 3 example inputs** the workflow consumes.
- **At least 3 example outputs** the workflow produces.
- All anonymized if they contain PII or sensitive data.

### Why
- We need to design an AI step that handles the actual variation in inputs.
- Outputs anchor the success measure.
- Without samples, the Sprint must default to synthetic data, which weakens proof.

## Item 3 — Owner Contact + Availability

- Owner full name, role, corporate email, mobile.
- Preferred daily 1-hour slot during the Sprint.
- Backup contact in case of owner absence (≤ 2 days OK; longer = pause).

## Item 4 — Current Tool List + Access

### Tools to List
- Notion / Sheets / Slack / Outlook / WhatsApp Business / custom apps.

### Access Required
- Read-only access to the relevant workspaces or shared folders.
- No production credentials. Sandbox or test environment preferred.
- If a tool requires SSO, client adds Dealix delivery emails to a named group.

## Item 5 — Data Handling Acknowledgement
Auto-generated from intake. Sponsor signs electronically. Confirms:
- Lawful basis for the processing implied.
- Agreement to `docs/DPA_DEALIX_FULL.md`.
- Cross-border posture per `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.
- Retention policy per `docs/ops/PDPL_RETENTION_POLICY.md`.

## Sensitive Data Handling
If intake flagged sensitivity:
- All shared files encrypted in transit and at rest.
- Two-person delivery team only.
- Proof pack anonymizes sensitive fields.
- Retention reduced to project + 30 days.

## Delivery Method
- Preferred: shared encrypted folder (Drive/OneDrive) with named access.
- SFTP available on request.
- Not acceptable: WhatsApp file send, public link.

## SLA
- Client uploads expected within **1 business day** of kickoff.
- Per business day of delay, Sprint slips by 1 day.
- After 3 business days of delay, restart fee SAR 1,000.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Welcome email | Drop folder ready | Dealix Ops | T-1 |
| Client upload | Receipt + integrity check | Dealix Analyst | Day 1 |
| Missing items | Chase email | Sales Engineer | Daily |

## Metrics
- **On-time data provision** — Target ≥ 85%.
- **Data sufficiency** — `% sprints where samples enable design without rework`. Target ≥ 90%.
- **Lawful-basis acknowledgement** — Target = 100%.

## Related
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention
- `docs/capabilities/operations_capability.md` — capability blueprint
- `docs/product/WORKFLOW_RUNTIME_DESIGN.md` — runtime design
- `docs/quality/QUALITY_STANDARD_V1.md` — quality regime
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/AI_STACK_DECISIONS.md` — approved stack
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
