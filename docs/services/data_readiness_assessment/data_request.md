# Data Readiness Assessment — Data Request — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Data Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [data_request_AR.md](./data_request_AR.md)

## Context
A Readiness Assessment is only as good as the inputs it gets. This
data request is the standard list of source files and confirmations
Dealix needs from the client before sampling and scoring begin. It
operates under `docs/DPA_DEALIX_FULL.md`,
`docs/DATA_RETENTION_POLICY.md`, and the PDPL retention schedule in
`docs/ops/PDPL_RETENTION_POLICY.md`. All transfers are read-only
samples per the scope in `scope.md`.

## What We Ask the Client For

### 1. Lead and Account Exports
- A recent export of leads and accounts (CSV / XLSX).
- Fields: account name, owner, stage, source, last activity, value,
  industry, region.
- 12 months of records is sufficient; older is welcome.

### 2. CRM Dump
- A read-only dump or report from the CRM (HubSpot, Salesforce,
  Zoho, etc.).
- Entities: accounts, contacts, deals, activities, owners.
- A snapshot is fine; we do not need a live connection.

### 3. Document Samples
- 20 to 50 representative documents (proposals, SOPs, FAQs, contracts,
  marketing assets).
- Mix of internal and external; mix of Arabic and English where
  relevant.

### 4. Current Process Documents
- Any written process, SOP, RACI, or playbook for the workflows we
  will assess.
- If undocumented, a brief written description from the owner is
  acceptable.

### 5. Sensitivity Classification
- Indication of which sources contain personal data, financial data,
  or contractual confidentiality.
- If no classification exists, we will produce a draft classification
  as part of the assessment.

### 6. Owner Contacts
- A named owner per source with email and phone.
- A named decision maker for sign-off on the readout.

## How We Receive Data
- Encrypted upload to the Dealix workspace, or
- Encrypted transfer over an agreed channel.
- No personal data is requested in plain text email.
- Samples are retained for the duration of the engagement plus the
  retention window in `docs/DATA_RETENTION_POLICY.md`, then deleted.

## What We Do Not Need
- We do not need live system credentials.
- We do not need full database exports.
- We do not need anything outside the scope in `scope.md`.
- We do not need uncontrolled access; sampling is targeted.

## Common Substitutes
- If CRM exports are not possible, screenshots of representative
  records are acceptable for sampling.
- If documents are scattered, a SharePoint or Drive folder is
  acceptable, provided access is read-only and scoped.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client confirmations and uploads | Sampled datasets ready for scoring | Data Lead | Per engagement |
| Owner contact list | Interview schedule | Data Lead, Client | Per engagement |
| Data request acknowledgement | Signed sub-DPA addendum if needed | Founder, Client | Per engagement |

## Metrics
- **Data Request Completeness** — share of requests fully satisfied at
  kickoff (target ≥ 80%).
- **Time-to-Sampling** — calendar days from request to first sample
  loaded (target ≤ 3 days).
- **Sample Coverage** — share of in-scope sources sampled (target =
  100%).
- **Sensitive Data Incidents** — count of mishandlings during transfer
  (target = 0).

## Related
- `docs/DPA_DEALIX_FULL.md` — data processing agreement governing the
  transfer.
- `docs/DATA_RETENTION_POLICY.md` — retention on samples.
- `docs/ops/PDPL_RETENTION_POLICY.md` — PDPL retention.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture for sample
  handling.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
