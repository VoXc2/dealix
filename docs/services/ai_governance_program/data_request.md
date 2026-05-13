# Data Request — AI Governance Program

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Analyst
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [data_request_AR.md](./data_request_AR.md)

## Context
The client-facing checklist of everything Dealix needs before Phase 1 of the Governance Program. Governance work is highly information-dependent — every late item compresses the Program. Enforces the DPA in `docs/DPA_DEALIX_FULL.md`, PDPL retention in `docs/ops/PDPL_RETENTION_POLICY.md`, and compliance certifications context in `docs/legal/COMPLIANCE_CERTIFICATIONS.md`.

## Summary
Client provides:
1. **AI tool list** — 5–30 entries.
2. **Data flow diagrams** (or accept a workshop to draft them).
3. **Existing policies** — AI Usage, Data Handling, Vendor, Incident, Approval (whichever exist).
4. **Incident history** — last 24 months.
5. **Lawful-basis statements per dataset.**
6. **Signed data handling acknowledgement.**

Time budget: **≤ 10 business days**.

## Item 1 — AI Tool List

### Format
- Structured spreadsheet or Notion database.
- Required columns: `tool_name`, `vendor`, `internal_owner`, `internal_owner_email`, `purpose`, `data_categories_touched`, `users_in_use`.

### Volume
- 5–30 entries. Outside → scoped engagement.

### What We'll Do
- Build the AI inventory.
- Map each tool to data flow and risk profile.
- Flag governance gaps per tool.

## Item 2 — Data Flow Diagrams

### Acceptable Formats
- Existing diagrams (Visio, Lucid, draw.io, PDF).
- Notion pages with text descriptions.
- "We don't have any — please run the workshop" is acceptable; we run a 2-hour workshop in Phase 1.

### Minimum Content
- Source systems (where data enters).
- Processing steps.
- AI tool involvement points.
- Storage destinations.
- Cross-border crossings.
- Sensitive-data touchpoints.

## Item 3 — Existing Policies

### What To Send
- AI Usage Policy (if exists).
- Data Handling Policy.
- Vendor / Third-Party Policy.
- Incident Response Runbook.
- Approval Matrix.
- Any sector-specific compliance docs (healthcare, finance, government).

### Format
- PDF, DOCX, Notion link.
- Versions identified.

### If Missing
We draft from scratch and you review.

## Item 4 — Incident History

### What To Send
- List of AI-relevant incidents in the last 24 months.
- For each: date, description (anonymized), impact, resolution, lessons.
- "None" is acceptable if attested in writing.

### Sensitivity
Some incidents are highly sensitive. Send via encrypted channel and we treat them under the sensitive-data regime.

## Item 5 — Lawful Basis Statements

For each dataset processed by AI tools, a 1-line lawful basis statement per the Saudi PDPL:
- "Consent of data subjects" (with proof of collection mechanism).
- "Performance of a contract" (with contract reference).
- "Legitimate interest" (with documented assessment).
- "Legal obligation" (with reference).
- "Public interest" (rare).

If you don't have these statements yet, we help derive them in Phase 1.

## Item 6 — Signed Data Handling Acknowledgement

Auto-generated from intake. Sponsor + DPO sign. Confirms:
- Lawful basis posture.
- Agreement to `docs/DPA_DEALIX_FULL.md`.
- Cross-border posture per `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.
- Retention per `docs/ops/PDPL_RETENTION_POLICY.md`.
- Engagement with the client's counsel-of-record for any regulatory filing.

## Sensitive Data Handling
Governance programs touch sensitive information by definition. Mandatory:
- All transfers encrypted in transit; vault encrypted at rest.
- Two-person delivery team (DL + Governance Reviewer) only.
- Three-person team for healthcare / government clients (add Capability Lead).
- Proof pack auto-anonymizes sensitive fields.
- Retention reduced to project + 60 days for sensitive subsets.

## Delivery Method
- Preferred: encrypted shared folder with named access for Dealix delivery team only.
- SFTP available on request.
- For very sensitive content: encrypted USB drop with chain of custody.
- Not acceptable: WhatsApp file send, public link, personal email attachment unencrypted.

## SLA
- Upload expected within **10 business days** of kickoff.
- Per business day of delay, Program slips by 1 day.
- After 10 business days of delay, restart fee SAR 5,000.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Welcome email | Drop folder ready | Dealix Ops | T-3 |
| Client upload | Receipt + integrity check | Dealix Analyst | Phase 1 |
| Sensitive flag | Vault placement | Dealix Governance Reviewer | Phase 1 |
| Missing items | Chase email | Sales Engineer | Daily until resolved |

## Metrics
- **On-time data provision** — Target ≥ 75%.
- **Policy submission rate** — `% policies submitted vs. existing ones` per intake. Target ≥ 90%.
- **Lawful-basis acknowledgement** — Target = 100%.

## Related
- `docs/DPA_DEALIX_FULL.md` — DPA
- `docs/DATA_RETENTION_POLICY.md` — retention
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — compliance
- `docs/governance/RUNTIME_GOVERNANCE.md` — runtime governance
- `docs/governance/AI_ACTION_TAXONOMY.md` — action taxonomy
- `docs/governance/AI_ACTION_CONTROL.md` — action control
- `docs/enterprise/CONTROLS_MATRIX.md` — enterprise controls
- `docs/capabilities/governance_capability.md` — capability blueprint
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
