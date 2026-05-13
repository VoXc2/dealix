# Trust Capital System — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CEO + Compliance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [TRUST_CAPITAL_SYSTEM_AR.md](./TRUST_CAPITAL_SYSTEM_AR.md)

## Context

In Saudi B2B, trust is the limiting factor on every enterprise deal.
We do not buy trust; we earn and store it. The Trust Capital System
defines the assets, the rules for public claims, and the storage of
evidence that makes Dealix credible to executives, compliance
officers, and regulators. It pairs with
`docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`, the AR enterprise
trust pack `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md`,
and the data processing agreement in `docs/DPA_DEALIX_FULL.md`.

## Trust Asset Types

| Asset | Definition |
|---|---|
| Proof Pack | End-of-engagement evidence pack (anonymized metrics, before/after, governance log) |
| Anonymized case study | Public 1-2-page narrative with consent + redaction |
| Testimonial | Named quote, role, sector, approved in writing |
| Governance record | Approval log + audit log per engagement |
| Audit log | System-level event log for AI runs, data movement, external actions |
| Public standard | Published policy (PDPL handling, eval method, model routing) |
| Privacy-safe example | Synthetic or fully anonymized sample of an output |
| Client handoff report | Final signed-off package given to client at close |

Each asset is recorded in the Trust Ledger with: id, type, source
engagement, consent status, date, owner.

## The Claim Rule

> **Every public claim must be backed by a Proof Pack, anonymized
> metric, approved testimonial, or marked sample.**

If a claim cannot be linked to one of those, the claim is removed.
Period.

## Allowed Claims

These are types of claim Dealix can make publicly:

- "Banking sector pilot improved qualified opportunities per week
  by **X%** in 6 weeks." (with Proof Pack link, anonymized.)
- "We delivered **N** governed AI workflows under PDPL." (with audit
  log count.)
- "Our retainer clients renew at **X%** annual rate." (with cohort
  size disclosed.)
- "Average Arabic Business Quality score across delivered work:
  **X**." (with sample size.)

## Not-Allowed Claims

- "Best AI company in Saudi." Superlative, unverifiable.
- "Guaranteed revenue uplift." Guarantee + unverifiable.
- "Trusted by leading enterprises." No named, consented testimonial.
- "Cuts your cost by 80%." Specific without source = fabrication.
- "Saudi's #1 AI Operations partner." Ranking without authority.
- "Our AI never hallucinates." False technical claim.

## Storage and Retention

- Proof Packs and case studies stored under client consent terms.
- Audit logs retained per `docs/DATA_RETENTION_POLICY.md`.
- PDPL handling per `docs/DPA_DEALIX_FULL.md` and
  `docs/ops/PDPL_RETENTION_POLICY.md`.
- Cross-border transfers governed by
  `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.

## Workflow

1. **Engagement close** — Delivery + CSM assemble Proof Pack
   (anonymized).
2. **Consent capture** — CSM requests consent for case-study /
   testimonial / logo. Default position: anonymized only.
3. **Claim review** — every public claim is reviewed by Compliance
   Lead before publication.
4. **Trust Ledger entry** — record asset; mark consent state; set
   review date.
5. **Annual audit** — verify all public claims still link to live
   assets.

## Trust Capital Compounding

A Proof Pack does not stop at the client. It is the unit of
marketing, partner enablement, and category leadership. Each Proof
Pack should produce at least:

- One Market Capital asset (see
  `docs/growth/MARKET_CAPITAL_SYSTEM.md`).
- One Knowledge Capital entry (see
  `docs/company/KNOWLEDGE_CAPITAL_SYSTEM.md`).
- One partner enablement update (see
  `docs/partners/PARTNER_OPERATING_SYSTEM.md`).

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Engagement evidence, consent forms | Trust Ledger entries | CSM + Compliance Lead | Per close |
| Public claim drafts | Approved / blocked claim list | Compliance Lead | Per claim |
| Audit logs | Annual compliance report | Compliance Lead | Annual |

## Metrics

- **% engagements producing a Proof Pack** — target 100%.
- **% public claims with linked evidence** — target 100%.
- **# approved testimonials/year** — target ≥6.
- **# governance breaches** — target 0.
- **Audit log completeness** — target 100%.

## Related

- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` — business-side trust pack.
- `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md` — enterprise AR pack.
- `docs/DPA_DEALIX_FULL.md` — data processing agreement.
- `docs/DATA_RETENTION_POLICY.md` — retention policy.
- `docs/ops/PDPL_BREACH_RUNBOOK.md` — breach runbook.
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — compliance certifications.
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border addendum.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
