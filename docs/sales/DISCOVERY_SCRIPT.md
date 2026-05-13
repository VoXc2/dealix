# Discovery Script — Dealix Growth Layer

**Layer:** L6 · Growth Machine
**Owner:** Head of Growth / Founder
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DISCOVERY_SCRIPT_AR.md](./DISCOVERY_SCRIPT_AR.md)

## Context
The discovery script is the structured conversation used in stage 5
(Discovery Booked) of `docs/sales/SALES_PIPELINE_V1.md`. It removes the
constraint of unstructured, founder-dependent discovery and ensures
every call produces enough information to choose between a Diagnostic,
a Sprint, or a Nurture decision. It is consistent with the strategic
framing in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and operational
discipline in `docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Use rules

- Time-box: 25–35 minutes.
- One scribe, one driver.
- Never sell during discovery. Listen first.
- Capture answers in plain text in CRM.
- End with one of three exits: Diagnostic, Sprint, Nurture.

## Section 1 — Opening (3 min)

> "Thank you for the time. We will spend ~25 minutes understanding the
> most painful operational area in your business right now. We will not
> pitch on this call. At the end we will tell you whether we can help —
> and if we can, what the smallest first step looks like."

Then ask: **"Where in your operations is the most pain right now —
sales, support, reports, knowledge?"**

## Section 2 — Revenue (6 min)

- Where do leads come from today?
- How many leads per month?
- Do you know your **top 20 opportunities** by name?
- How is follow-up done — manually, on paper, in WhatsApp?
- Is a CRM in place? If yes, is it used daily?
- Where do leads typically die in the funnel?

## Section 3 — Data (6 min)

- Where does customer / opportunity data live?
- How many separate places (sheet, WhatsApp, email, paper)?
- Any duplicates or missing data you already know about?
- Are sources tracked per lead?
- Who owns this data internally?

## Section 4 — Operations (5 min)

- Which **weekly report** repeats in your team?
- How many hours per week does that report take?
- Who reviews it and what do they do with it?
- What other recurring manual work eats time?

## Section 5 — AI & Governance (5 min)

- Does the team currently use AI (ChatGPT, Copilot, others)?
- Is there a written AI usage policy?
- Is any sensitive data (PII, client info, financials) involved?
- Have you had any near-miss issues with AI output?
- Reference: `docs/ops/PDPL_RETENTION_POLICY.md` for our default
  posture.

## Section 6 — Close (5 min)

Frame the next step:

> "Based on what you described, the right first step is a **Sprint**,
> not a big project. A Sprint takes 10 days, has a fixed price, and
> ends with a Proof Pack showing what value we created. We do not
> guarantee revenue outcomes — we guarantee deliverables, governed
> outputs, and measurable proof."

Offer one of:
- **Lead Intelligence Sprint** if revenue/CRM pain dominated.
- **AI Quick Win Sprint** if recurring report / workflow pain dominated.
- **Company Brain** path if knowledge pain dominated.

If no clear fit: schedule a paid Diagnostic.

## Decision template (filled at end of call)

| Field | Value |
|---|---|
| Dominant pain area | Revenue / Ops / Knowledge / Governance |
| Best offer | Lead Intelligence / AI Quick Win / Company Brain / Diagnostic |
| Risk flags | PII / regulated industry / unknown-source data |
| Next action | Send proposal / Nurture / Decline |
| Owner | Single human |

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Booked discovery calls | Filled decision template | Growth | Per call |
| Decision template | Proposal draft | Founder / Growth | Within 48h |
| Risk flags | Compliance review trigger | Compliance Owner | Same week |

## Metrics

- **Discovery → Proposal** conversion %.
- **Average call length** (target 25–35 min).
- **Decline-rate from risk flags** (PII / unknown data).
- **Time-to-proposal** after discovery (target ≤ 48h).

## Related

- `docs/sales/DEMO_SCRIPT.md` — used after Discovery for technical buyers.
- `docs/sales/ONE_PAGER.md` — leave-behind after Discovery.
- `docs/sales/OBJECTION_HANDLER.md` — handling pushback inside Discovery.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
