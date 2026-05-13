# Client AI Policy Pack — Approval Matrix

**Layer:** L5 · Enterprise Governance
**Owner:** Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [approval_matrix_AR.md](./approval_matrix_AR.md)

## Context
The approval matrix turns the policy into operational decisions: for any given AI action, *who* approves and *when*. Without an approval matrix, AI use defaults to the most senior person available, which is both a bottleneck and a risk. This file standardizes approvers and aligns with the policy in `./policy_template.md`, the employee guide in `./employee_guide.md`, and the tool rules in `./tool_usage_rules.md`. It also aligns with `docs/DPA_DEALIX_FULL.md`, `docs/DATA_RETENTION_POLICY.md`, and the PDPL discipline in `docs/ops/PDPL_RETENTION_POLICY.md`.

## Approver roles
- **Manager** — the requester's direct manager.
- **Governance Reviewer** — the client-side AI governance owner (often Compliance, Risk, or COO).
- **Data Owner** — the named owner of the dataset in question.
- **Executive Sponsor** — the C-level sponsor for AI program decisions.

## Default matrix
The default approval matrix maps action class (consistent with `docs/governance/AI_ACTION_CONTROL.md`) to required approver(s):

| Action Class | Description | Approver(s) | Audit Required |
|---|---|---|---|
| A | Internal insight, summary, classification | None (logged) | Yes |
| B | Client-facing draft / report | Manager + Governance Reviewer for new categories | Yes |
| C | Internal system change (CRM update, task create) | Manager | Yes |
| D | External communication (email, message, post) | Manager + Data Owner; Executive Sponsor for high-stakes channels | Yes |
| E | Autonomous external action | Blocked by default; Executive Sponsor + Governance Reviewer for any exception | Yes |

## Dataset overlay
The matrix also maps dataset class to required approver for AI access to that dataset:

| Dataset Class | Examples | Approver(s) |
|---|---|---|
| Public | Marketing site, public knowledge | None |
| Internal | Internal docs, non-sensitive analytics | Manager |
| Confidential | Customer data, deal data | Data Owner |
| Restricted | PII, regulated data, M&A, HR exits | Data Owner + Governance Reviewer |
| Special | Health, financial regulated, government | Data Owner + Governance Reviewer + Executive Sponsor |

When an action involves multiple classes, the strictest class governs.

## How approvals are recorded
- Approvals are recorded with: approver name, role, action class, dataset class, timestamp, scope of approval, and expiry (if scoped).
- Approval records are linked to the AI run provenance (`docs/product/AI_RUN_PROVENANCE.md`).
- Standing approvals (e.g., "approve all Class-B drafts from this agent for this campaign") are time-limited and recorded once.

## Escalation
- A request unresolved by the named approver within the SLA (default: 48 working hours) escalates to that approver's manager.
- A pattern of escalations triggers a Governance review of the matrix.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Action class + dataset class | Required approver list | Governance Reviewer | Per request |
| Approval decisions | Recorded approval tokens | Approvers | Per request |
| Escalations | Council review trigger | Governance | As needed |

## Metrics
- Matrix Coverage — % of approvable actions that ran through the matrix.
- Approval-Within-SLA Rate — % of approvals completed within 48 working hours.
- Standing-Approval Hygiene — % of standing approvals with an expiry date.
- Escalation Rate — escalations per 100 approval requests.

## Related
- `docs/DPA_DEALIX_FULL.md` — DPA framing approvals
- `docs/DATA_RETENTION_POLICY.md` — retention rules behind approval records
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL alignment
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — certifications context
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
