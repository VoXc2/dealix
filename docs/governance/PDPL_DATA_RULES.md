---
title: PDPL Data Rules — Art. 5/13/14/18/21 Application
doc_id: W6.T37.pdpl-data-rules
owner: HoLegal
status: draft
last_reviewed: 2026-05-13
audience: [internal, customer]
language: en
ar_companion: none
related: [W3.T07b]
kpi:
  metric: pdpl_compliance_audit_findings
  target: 0
  window: per_audit
rice:
  reach: 0
  impact: 3
  confidence: 0.95
  effort: 0.5
  score: governance-pdpl
---

# PDPL Data Rules

## 1. Context

The Saudi Personal Data Protection Law (PDPL — Royal Decree M/19) sets the
non-negotiable rules for processing personal data of Saudi data subjects.
This document maps the five most operationally relevant PDPL articles to the
rules Dealix applies in code, in delivery, and in commercial agreements. The
authoritative customer-facing statement is
[`../trust/data_governance.md`](../trust/data_governance.md).

## 2. Audience

Engineers (must encode the rules), CSMs (must enforce them during delivery),
HoLegal (must approve exceptions), customers' DPOs (read this to verify our
posture).

## 3. PDPL Article Map

### 3.1 Art. 5 — Lawful Basis

Every personal data processing operation must have one of the supported
lawful bases recorded against it:

- Consent (Art. 6 controls).
- Performance of a contract with the data subject.
- Compliance with a legal obligation.
- Protection of vital interests.
- Public interest.
- Legitimate interests (with balancing test).

The basis is selected in the DPA scope worksheet and persisted in the
customer's tenant config. Code path: lawful basis is required input to
the consent ledger and policy checks.

### 3.2 Art. 13 — Notice

Notice content (in AR and EN) is provided by Dealix as a template. The
customer (controller) remains responsible for surfacing notices to data
subjects. Dealix surfaces just-in-time notice elements where the customer
opts in.

**Onboarding rule**: PDPL Art. 13 acknowledgement is captured from every
new customer before any data is processed.

### 3.3 Art. 14 — Consent

When consent is the chosen basis, the consent ledger records minimum
metadata: data subject identifier, purpose, version of notice presented,
timestamp, channel, proof-of-affirmative-action. Withdrawal is processed
within the deletion SLA (§3.5).

### 3.4 Art. 18 — Cross-Border Transfer

Transfers occur only under: (a) SDAIA adequacy list, (b) executed
Cross-Border Transfer Addendum with SDAIA-aligned safeguards, or (c)
explicit informed consent specific to the transfer. The Kingdom Residency
option (Enterprise plan) pins all production data to Kingdom-eligible
regions.

### 3.5 Art. 21 — Retention

Personal data is retained only for the period necessary to the purpose.
Default windows are in [`DATA_RETENTION.md`](DATA_RETENTION.md). Customers
may shorten via the DPA worksheet.

## 4. Lawful Basis Inventory (Per Service)

| Service | Default lawful basis | Special-category? |
|---------|---------------------|--------------------|
| Lead Intelligence Sprint | Legitimate interests + customer contract | No |
| AI Quick Win Sprint | Customer contract | No (case-by-case) |
| Company Brain Sprint | Customer contract | Possibly (HR / health docs); requires explicit ack |
| Outbound Outreach | Consent (Art. 14) for cold; legitimate interests for warm | No |

## 5. Data Inventory

The data categories Dealix processes are enumerated in `docs/DATA_MAP.md`.
At a summary level: customer end-user identifiers, customer-uploaded
content, authentication artefacts, billing metadata (tokenised), and
operational telemetry. Sensitive personal data only with explicit ack.

## 6. Cross-links

- Customer-facing canon: [`../trust/data_governance.md`](../trust/data_governance.md)
- Compliance perimeter: [`COMPLIANCE_PERIMETER.md`](COMPLIANCE_PERIMETER.md)
- Data retention: [`DATA_RETENTION.md`](DATA_RETENTION.md)
- PII policy: [`PII_REDACTION_POLICY.md`](PII_REDACTION_POLICY.md)
- Cross-border addendum: `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`
- DSAR SOP: `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`
- Data map: `docs/DATA_MAP.md`

## 7. Owner & Review Cadence

- **Owner**: HoLegal (DPO is functional owner).
- **Review**: quarterly; immediate on any Implementing Regulation revision.

## 8. Change Log

| Date | Author | Change |
|------|--------|--------|
| 2026-05-13 | HoLegal | Initial Art. 5/13/14/18/21 application map |
