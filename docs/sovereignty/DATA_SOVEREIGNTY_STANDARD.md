# Data Sovereignty Standard

Every dataset that enters Dealix is governed before it is used. Data sovereignty is operational, not aspirational.

## 1. Five preconditions

A dataset can only be used after answering, in writing:

- Where did it come from?
- Who owns it?
- What is the allowed use?
- Does it contain PII?
- Can it be ingested by AI? Can it be used externally?
- When is it deleted?

The answers are captured in a **Source Passport** (`SOURCE_PASSPORT_STANDARD.md`).

## 2. Hard rules

- No Source Passport → no AI use.
- No declared allowed use → internal analysis only.
- PII without a documented basis → redact or block.
- External action → approval required.

## 3. Operating posture

- Data residency defaults to in-region unless explicitly waived.
- Cross-tenant data is forbidden by default; aggregation requires a written aggregation rule.
- Retention is per-tenant, per-engagement, and enforced by code.
- Data subject requests are honored within published SLAs.

## 4. Alignment with regional governance

NDMO and SDAIA frame the national posture on data management and protection. Dealix builds against these principles by default — even for engagements outside the public sector — because the same posture protects every buyer.

## 5. Operating discipline

- Source Passports are produced at engagement intake, not after a problem arises.
- Every passport has a `last_reviewed_at`; stale passports are flagged.
- Access decisions are auditable; denied requests are recorded with reasons.
- The Capital Ledger never stores raw client data; it stores derived artifacts.

## 6. Anti-patterns

- “Just-this-once” exceptions to passport rules.
- Conditional approvals that never expire.
- Aggregated benchmarks built without an aggregation rule.
- Datasets shared between BUs without re-checking allowed use.

## 7. The principle

> We do not put AI on unclear data. We start with source, allowed use, sensitivity, and governance — then AI.
