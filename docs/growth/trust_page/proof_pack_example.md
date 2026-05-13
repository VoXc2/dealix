# Proof Pack Example — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of Delivery
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [proof_pack_example_AR.md](./proof_pack_example_AR.md)

## Context
This page shows what a Dealix proof pack actually contains, using an
anonymized example. It is the public reference for the proof pack
discipline grounded in
`docs/DEALIX_OPERATING_CONSTITUTION.md` and
`docs/company/VALUE_REALIZATION_SYSTEM.md`.

## Anonymized example (Lead Intelligence engagement)

- **Engagement:** 2-week Lead Intelligence sprint for a B2B SaaS client.
- **Inputs (approved):** Salesforce export (anonymized), ICP brief, three
  prior closed-won account profiles.
- **Outputs:**
  - **Top 50 ranked accounts** with explanation per account (top three
    fit/signal reasons).
  - **Before/after data quality** — baseline score 62, end-of-engagement
    score 81 across completeness, validity, and freshness.
  - **Draft samples (synthetic).** Three outreach drafts per top-tier
    account, generated against the no-guarantee rule and tone library.
    Sender, names, and identifiers are synthetic to protect the real
    client.
  - **Executive summary.** Bilingual page with the decision, top metrics,
    and a clear next action.
- **Evidence trail:**
  - Dataset versions and access log.
  - Prompt versions and eval suite results.
  - Compliance Guard verdicts (block / allow) per draft.
  - Reviewer sign-off names and timestamps.
- **Value Ledger entry:** `V-0XX` with Revenue + Time value claims and a
  next-value entry for Pilot Conversion.

## How to read a proof pack

1. Start with the executive summary.
2. Open the ranked output to inspect explanations.
3. Verify before/after metrics against the evidence trail.
4. Inspect the Compliance Guard log to confirm blocks.
5. Find the ledger entry to confirm the value claim.

## What it does **not** include

- Real PII or client identifiers.
- AI outputs without provenance.
- "Guaranteed conversion" numbers.
- Knowledge answers without citations.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Engagement artifacts | Anonymized proof pack | Delivery owner | Per engagement |
| Reviewer sign-off | Signed proof pack | Reviewer | Per engagement |
| Ledger entry | Linked value record | Head of Delivery | Per engagement |

## Metrics
- Proof Pack Completeness — % of packs with all required sections.
- Anonymization Verification — % of public packs reviewed for PII leakage.
- Reviewer Sign-off Latency — hours from draft to sign-off.
- Public Pack Reuse — packs cited in sales conversations.

## Related
- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` — business trust pack
- `docs/DPA_DEALIX_FULL.md` — data processing agreement
- `docs/DATA_RETENTION_POLICY.md` — retention rules
- `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md` — Arabic trust pack
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
