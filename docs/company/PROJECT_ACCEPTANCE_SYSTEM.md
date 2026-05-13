# Project Acceptance System — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CEO + COO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PROJECT_ACCEPTANCE_SYSTEM_AR.md](./PROJECT_ACCEPTANCE_SYSTEM_AR.md)

## Context

Every accepted project either compounds Dealix or damages it.
Bad-fit projects do not just waste a quarter — they erode Trust
Capital, Arabic Quality, and Margin Guard simultaneously. This
system is the gate between qualified interest and signed contract.
It complements `docs/DPA_DEALIX_FULL.md`, the sales qualification
process in `docs/sales/SALES_QUALIFICATION.md`, and the pricing
formula in `docs/company/PRICING_ENGINE.md`. The Decision System
(`docs/company/DECISION_SYSTEM.md`) decides *what* to sell; the
Project Acceptance System decides *which engagement* to sign.

## Must-Have Checklist

A project may only be accepted if all eight items are satisfied:

1. **Clear buyer** — the executive sponsor and economic buyer are
   named, contactable, and aligned on outcome.
2. **Clear problem** — the buyer can state the pain in one sentence
   without help.
3. **Clear data** — known source, known owner, known access path,
   PDPL-compatible.
4. **Clear deliverable** — the artifact the buyer will receive is
   described in writing (file, dashboard, workflow, report).
5. **Clear metric** — at least one quantitative success metric the
   buyer agrees to.
6. **Governance fit** — no forbidden actions; approvals scope
   defined; audit/logging plan exists.
7. **Margin fit** — projected margin ≥ track minimum
   (`docs/company/MARGIN_GUARD.md`).
8. **Proof capability** — we can produce a Proof Pack for this
   engagement at the end.

If any item is unclear, the project is downgraded to a paid Diagnostic
(scoped, fixed-fee discovery) before any commitment.

## Reject-If List

A project is **automatically rejected** if any of the following is
true. These cannot be overridden by revenue size.

- Requires spam automation (mass cold messaging, follow-up loops
  without consent).
- Requires scraping personal data, contact lists, or private profiles.
- Requires cold WhatsApp outreach.
- Requires LinkedIn automation that violates platform terms.
- Requires guaranteed business results (deals, leads, revenue,
  rankings) language in the contract.
- Data source is unknown, unowned, or unverifiable.
- Scope is vague (no written boundaries, "we'll figure it out").
- High risk paired with low budget (governance burden exceeds
  recoverable fee).
- Requires us to act as a regulated party we are not (legal,
  medical, financial advice).
- Buyer requires us to skip QA or governance to meet timeline.

A rejection is logged with reason in the Project Acceptance Log so
patterns inform future qualification scripts.

## Project Score Model

For projects that clear the reject-if list, an 8-factor score is
computed. Each factor is 0-10 points (max 80).

| # | Factor | What we score | Weight |
|---|---|---|---:|
| 1 | Buyer fit | Clear sponsor, decision authority, urgency | 10 |
| 2 | Problem clarity | Articulated in one sentence by the buyer | 10 |
| 3 | Data readiness | Source, owner, access, quality | 10 |
| 4 | Scope clarity | Written, bounded, with examples in/out | 10 |
| 5 | Outcome measurability | Quantitative metric agreed in writing | 10 |
| 6 | Governance fit | PDPL, approvals, no forbidden actions | 10 |
| 7 | Margin fit | Projected vs track minimum | 10 |
| 8 | Proof capability | Proof Pack feasible at end | 10 |

Decision thresholds:

| Score | Action |
|---|---|
| **70+** | **Accept** — sign and onboard. |
| 55-69 | **Diagnostic only** — sell a paid diagnostic (1-2 weeks, fixed scope) to mature the project. |
| <55 | **Reject** — log reason; offer asynchronous content/templates. |

## Workflow

1. Sales qualification ends with handoff packet
   (`docs/sales/SALES_QUALIFICATION.md`).
2. Acceptance reviewer (COO) scores the project against the 8
   factors and checks the reject-if list.
3. If score 70+, finance issues proposal using
   `docs/sales/PROPOSAL_LIBRARY.md`.
4. If score 55-69, sales offers a paid Diagnostic. After Diagnostic,
   project is re-scored.
5. If <55 or rejected, send a polite "not a fit right now" note;
   offer content; log in Acceptance Log.

## Acceptance Log

A single tracker (sheet or CRM stage) records:

- Project name, account, date.
- Reject-if checks (pass/fail per item).
- 8-factor scores.
- Outcome: Accept / Diagnostic / Reject.
- Reason notes.
- Reviewer.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Sales handoff packet, intake form, data fit notes | Accept / Diagnostic / Reject decision | COO | Per project |
| Pricing engine | Quoted proposal | CEO | Per accepted project |
| Governance rules | Approval plan, PDPL notes | CTO + Legal | Per accepted project |

## Metrics

- **Acceptance rate of qualified opportunities** — target 60-80% (too high = poor qualification; too low = poor sales).
- **Diagnostic-to-project conversion** — target ≥50%.
- **Post-acceptance failure rate** — target ≤5% (projects accepted that should not have been).
- **Reject-if catch rate** — target 100% before contract.

## Related

- `docs/DPA_DEALIX_FULL.md` — data processing agreement template.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — constitutional rejects.
- `docs/OFFER_LADDER_AND_PRICING.md` — pricing tied to acceptance tier.
- `docs/sales/SALES_QUALIFICATION.md` — upstream qualification.
- `docs/company/PRICING_ENGINE.md` — used at proposal step.
- `docs/company/MARGIN_GUARD.md` — margin minimums per track.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
