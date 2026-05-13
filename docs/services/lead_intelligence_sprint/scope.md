# Scope — Lead Intelligence Sprint

**Layer:** Service Catalog · Operational Kit
**Owner:** Delivery Lead — Revenue
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [scope_AR.md](./scope_AR.md)

## Context
This document is the **contractually binding scope** for the Lead Intelligence Sprint. It exists to prevent scope creep, define the in/out boundary, and pre-clear the assumptions on which the fixed-fee delivery depends. It is referenced from the master service ladder in `docs/COMPANY_SERVICE_LADDER.md` and the canonical pricing ladder in `docs/OFFER_LADDER_AND_PRICING.md`. The scope is enforced in QA against `docs/quality/QUALITY_STANDARD_V1.md` and is part of the proof pack record (`docs/templates/PROOF_PACK_TEMPLATE.md`).

## Duration
- **10 business days** end-to-end, from kickoff to final handoff.
- Kickoff occurs within 5 business days of the signed SOW and deposit.
- Optional Day 11 review session if requested at SOW time (no extra fee).

## In Scope
1. **Data review** of up to 1 source export, maximum 10,000 rows. Larger volumes are scoped separately.
2. **Quality scoring** per row: completeness, duplicate likelihood, recency, source clarity.
3. **Deduplication** using deterministic rules (email, normalized domain, phone hash) with a manual review queue for fuzzy matches.
4. **ICP scoring** of the cleaned set against a documented rubric agreed in intake.
5. **Top 50 ranked accounts** with score, explanation, and recommended channel.
6. **Top 10 action plan** with named owner, first-touch suggestion, fallback path.
7. **Outreach draft pack** — 4 sequences × Arabic + English × `draft_only` flag.
8. **Mini CRM board** in Notion or Google Sheets (client choice). One workspace, up to 5 named users.
9. **Executive proof report** — PDF + Markdown, signed off by client sponsor.
10. **Proof pack** — events log, anonymization rules applied, hand-off note.

## Not In Scope
- **CRM integration** (HubSpot/Salesforce/Pipedrive/Zoho push). Add-on: SAR 6,000+ depending on platform.
- **Email or SMS sending automation.** All drafts ship as text only.
- **WhatsApp Business API setup** or any messaging-platform deployment.
- **Paid advertising, retargeting, or media buying.**
- **Brand or visual identity work.** Drafts use client's existing tone references.
- **Multi-source data merging** beyond one primary export. Each additional source = SAR 2,500.
- **Custom data enrichment via paid providers** (Clearbit, Apollo, etc.) unless the client provides licensed credentials.
- **Pen-testing, security audit, or compliance certification.**
- **Ongoing list maintenance after Day 10.** Continuation is handled via the Monthly RevOps OS retainer.

## Assumptions
1. The client provides a **clean primary export** in CSV or XLSX within 1 business day of kickoff. Columns expected: company, contact name, email, phone, city, sector, source, last_contact (when applicable).
2. The client has an **ICP definition** or is prepared to define one with the Dealix Analyst in the Day 2 intake.
3. The client nominates a **single decision-maker** for the sprint (typically Head of Sales or CEO).
4. The client's data has a **lawful basis** for the contact processing implied by outreach (consent, legitimate interest with a documented assessment, or contractual). Dealix will not process data without it.
5. The client agrees to the **Dealix data handling DPA** in `docs/DPA_DEALIX_FULL.md` and confirms cross-border posture per `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` if applicable.
6. The client provides **one named reviewer** available for ≤ 2 hours/day during the sprint.
7. The client accepts that **Dealix does not guarantee meetings or deals** — the deliverable is the ranked pipeline and drafts.

## Dependencies
- Access to the data export must be granted on Day 1.
- ICP review must be completed by end of Day 2 or the sprint timeline slips by 1 business day per day of delay.
- Proof pack signoff requires the client sponsor's signature on Day 10. If the sponsor is unavailable, signoff defers but Dealix considers delivery complete.

## Change Control
- Any scope change request after Day 3 requires a written change order signed by both parties.
- Change orders may extend the sprint by up to 5 business days at SAR 1,500/day.
- Out-of-scope work always carries a separate SOW.

## Geography & Language
- Primary delivery languages: **Arabic (Saudi/Gulf register) and English**.
- Other languages on request, at +SAR 1,500/language.
- Compliant with PDPL (Saudi Personal Data Protection Law). Cross-border processing only on the basis defined in `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`.

## Acceptance
The Sprint is considered accepted when:
1. The executive proof report is delivered.
2. The proof pack events log is shared.
3. The client sponsor signs the handoff note (electronic signature accepted).

If no signoff and no objection is received within 5 business days of delivery, the Sprint is auto-accepted.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed SOW + deposit | Kickoff schedule | Dealix Ops + Client Sponsor | T-5 days |
| Primary data export | Cleaning queue | Client RevOps + Dealix Analyst | Day 1 |
| ICP definition | Scoring rubric | Client Head of Sales + Dealix Analyst | Day 2 |
| Reviewer feedback | Final deliverables | Client Reviewer + Dealix Delivery Lead | Day 9 |
| Signed handoff | Proof pack closure | Client Sponsor + Dealix QA | Day 10 |

## Metrics
- **Scope-change request rate** — `% sprints with ≥ 1 change order`. Target ≤ 20%.
- **On-time delivery** — `% sprints delivered on Day 10`. Target ≥ 95%.
- **Acceptance lead time** — `business days from delivery to signoff`. Target ≤ 3 days.

## Related
- `docs/capabilities/revenue_capability.md` — the parent capability blueprint
- `docs/company/MARGIN_CONTROL.md` — pricing floor enforcement
- `docs/company/RISK_ADJUSTED_PRICING.md` — premium triggers
- `docs/quality/QUALITY_STANDARD_V1.md` — quality gates the sprint must clear
- `docs/templates/PROOF_PACK_TEMPLATE.md` — proof pack scaffold
- `docs/DPA_DEALIX_FULL.md` — data processing addendum
- `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` — cross-border rules
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic context
- `docs/COMPANY_SERVICE_LADDER.md` — service ladder neighbours
- `docs/OFFER_LADDER_AND_PRICING.md` — canonical pricing ladder
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
