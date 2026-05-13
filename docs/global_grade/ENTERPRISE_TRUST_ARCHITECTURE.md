# Enterprise Trust Architecture

Enterprise buyers ask about **trust** before features. Dealix therefore productizes trust as an architecture, not as a checklist.

## 1. Components

- **Source Passport** — every dataset entering the system carries provenance, owner, allowed use, sensitivity, residency.
- **Data Readiness Score** — quality, duplication, completeness, freshness.
- **PII Detection** — automated detection and redaction at runtime.
- **Allowed Use Registry** — explicit per-source allowed actions.
- **Governance Runtime** — see `RUNTIME_GOVERNANCE_PRODUCT.md`.
- **AI Run Ledger** — immutable record per AI run.
- **Approval Engine** — channel-aware, role-aware, audit-aware.
- **Audit Events** — append-only, exportable.
- **Proof Pack** — evidence record per engagement.
- **Human Oversight Model** — explicit approval points and accountabilities.
- **Incident Response** — runbook + escalation matrix.

## 2. The trust sentence

> We do not put AI on unclear data. We start with source, allowed use, sensitivity, and governance — then AI.

## 3. Why this matters

Enterprise concerns around AI adoption consistently rank **data security, privacy, and compliance** at the top. Regulated industries cannot accept opaque AI behavior or unbounded agents. The trust architecture is the artifact that lets a CISO, DPO, or risk officer say *yes*.

## 4. Default postures

| Concern | Default |
| --- | --- |
| Data residency | In-region |
| Personal data | Redact before transit |
| External actions | Draft-only until approved |
| Cold outreach | Forbidden |
| Public claims | Require Proof Pack ID |
| Cross-tenant data | Forbidden |
| Model output as a contract | Forbidden — outputs are drafts |

## 5. Trust artifacts shipped to the buyer

- A signed **Source Passport** per data source.
- A **Data Readiness Report** scoped to the engagement.
- A **Governance Pack** with rule definitions and approvals.
- An **Audit Export** at every quarterly review.
- The **Proof Pack** as the engagement’s closing artifact.

## 6. Operating invariants

- An action without an active Source Passport is rejected.
- An external action without an approval record is rejected.
- A public claim without a Proof Pack ID is doctrine violation.
- An audit gap is treated as a P1 incident.

## 7. Failure modes to engineer against

- Trust packaged as a PDF instead of as a runtime artifact.
- Source Passports created at sale but not enforced at runtime.
- Approvals captured in chat instead of the approval engine.
- “Trust theater” — long policies, short audit logs.
