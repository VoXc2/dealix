# Client AI Policy Pack — Policy Template

**Layer:** L5 · Enterprise Governance
**Owner:** Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [policy_template_AR.md](./policy_template_AR.md)

## Context
This is the master template Dealix tailors to each client. The aim is not the longest policy possible — it is a policy short enough that employees read it, specific enough that auditors accept it, and operational enough that it survives day-to-day work. It anchors on `docs/DPA_DEALIX_FULL.md`, `docs/DATA_RETENTION_POLICY.md`, and the local PDPL discipline at `docs/ops/PDPL_RETENTION_POLICY.md`, and is one of the deliverables in `./offer.md`.

## How to use this template
- Replace `[Client]` with the client's legal name.
- Replace `[Effective date]` with the policy effective date.
- Replace `[Owner]` with the named internal owner (often Chief Compliance Officer or COO).
- Keep the section structure intact; tailor the bullet content per industry.

## Section 1 — Purpose
The purpose of this policy is to define how [Client] uses artificial intelligence ("AI") tools and services in the course of its business, so that AI use is consistent with [Client]'s legal obligations, customer commitments, and operational standards.

## Section 2 — Scope
This policy applies to:
- All employees, contractors, interns, and partners of [Client].
- All AI tools, whether internally hosted, vendor-hosted, or public.
- All use cases involving [Client] data, customer data, or partner data.

## Section 3 — Allowed AI uses
- Drafting internal communications and summaries from approved internal data.
- Summarizing public information and approved documents.
- Assisting with code, documentation, training material.
- Generating analyses from sanctioned datasets through approved tools.

## Section 4 — Prohibited uses
- Uploading customer data, employee data, or commercial sensitive data to public chatbots.
- Using AI to generate communications presented as human authored when regulation or client contract requires disclosure.
- Using AI to make consequential decisions (hire/fire, credit, eligibility) without a documented human-in-the-loop and review record.
- Using unapproved AI tools or browser plugins on company devices.

## Section 5 — Data handling
- Customer data is classified per [Client]'s data classification policy.
- Sensitive data (PII, financial, health, regulated) must never leave the approved tool list.
- Data uploaded to AI tools must follow least-data: only what is needed for the task.
- Outputs derived from internal data are themselves internal until reviewed.

## Section 6 — Sensitive data
- A defined list of data categories is sensitive by default (national ID, banking, health, biometrics, M&A and HR exits).
- Sensitive data is allowed only in enterprise-grade tools approved by the Vendor Approval process.
- Any incident involving sensitive data triggers the Incident Response process.

## Section 7 — Vendor approval
- New AI tools require evaluation and approval before use.
- Approval criteria: data residency, vendor security posture, data retention, sub-processor list, contract terms, and alignment with this policy.
- Approved tools are listed in the Tool Usage Rules document.

## Section 8 — Audit
- AI tool usage is auditable: logs are retained per the data retention policy.
- Audits run quarterly and on incident.
- Audit findings feed updates to this policy and to the Approval Matrix.

## Section 9 — Incident response
- Any suspected data exposure, unsafe output, or policy breach is reported to [Owner] within 24 hours.
- Incident handling follows the Dealix-aligned runbook at `docs/ops/INCIDENT_RUNBOOK.md`.
- Material incidents are reported to the executive sponsor and, where required, to regulators.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client data classification | Tailored policy text | Governance Lead + Client legal | Per engagement |
| Industry regulations | Section adjustments | Governance Lead | Per engagement |
| Tool inventory | Vendor approval list | Governance + IT | Quarterly |

## Metrics
- Policy Sign-Off Coverage — % of relevant staff who acknowledged the policy.
- Quarterly Review Compliance — % of clients whose policy was reviewed each quarter.
- Incident-Linked Policy Updates — count of policy amendments triggered by incidents per year.

## Related
- `docs/DPA_DEALIX_FULL.md` — DPA the policy aligns with
- `docs/DATA_RETENTION_POLICY.md` — retention rules the policy enforces
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention alignment
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — certifications roadmap
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
