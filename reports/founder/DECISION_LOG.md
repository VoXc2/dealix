# Founder Decision Log — Dealix

Append-only log of decisions that agents escalated to the founder. Agents must
not act on these until a decision is recorded here.

| # | Date | Decision needed | Options | Decision | Status |
|---|------|-----------------|---------|----------|--------|
| D-001 | 2026-06-03 | Authenticate governance `approve` mutation | authedQuery / adminQuery / leave | — | **OPEN (critical)** |
| D-002 | 2026-06-03 | Consolidate duplicate `company_os/company_os/` tree | keep root / keep nested / merge | — | OPEN |
| D-003 | 2026-06-03 | Fix or remove broken `package.json` `commercial:*` scripts | create JS / remove scripts | — | OPEN |
| D-004 | 2026-06-03 | Provision email infra (SPF/DKIM/DMARC, subdomain, Postmaster) | provision / defer | — | OPEN (blocks sending) |
| D-005 | 2026-06-03 | Confirm KSA data residency + sign vendor DPAs | confirm / alternative | — | OPEN |
| D-006 | 2026-06-03 | SDAIA PDPL registration timing | at revenue / earlier | — | OPEN |

## How to use
- Add a row when an agent escalates (collision, legal, ambiguous fix).
- Record the decision + date; only then may the relevant agent proceed.
