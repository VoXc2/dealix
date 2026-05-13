# Sales Qualification — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CEO / Sales Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [SALES_QUALIFICATION_AR.md](./SALES_QUALIFICATION_AR.md)

## Context

Sales qualification at Dealix has one job: hand off only projects
that can be Accepted under `docs/company/PROJECT_ACCEPTANCE_SYSTEM.md`
and priced cleanly under `docs/company/PRICING_ENGINE.md`. Bad
qualification fills the calendar and empties the bank. This
document standardizes the questions and the fit matrix used in every
discovery call. It plugs into the existing discovery script
(`docs/sales/DISCOVERY_SCRIPT.md`) and feeds the proposal library
(`docs/sales/PROPOSAL_LIBRARY.md`).

## Qualification Dimensions

Seven dimensions. Each dimension has 2-4 questions. The sales call
ends when all dimensions are answered or the prospect declines —
whichever first.

### 1. Pain

- "What's the operational pain that made you book this call?"
- "What happens if you don't solve it this quarter?"
- "Who feels the pain daily, weekly, monthly?"

### 2. Data

- "What systems hold the data you'd want to work on?"
- "Who owns the export? Can they grant access in 5 business days?"
- "Has this data been touched by AI/ML before? What happened?"

### 3. Process

- "What is the current workflow today, step by step?"
- "Which step would, if removed or automated, save the most?"
- "Is there a written SOP, or is it tribal knowledge?"

### 4. Buyer

- "Who has signing authority above the proposed budget?"
- "Who is the executive sponsor for the outcome?"
- "Who would block this internally and why?"

### 5. Value

- "If we deliver the outcome, what changes in your numbers?"
- "What is the value of that change in SAR for one quarter?"
- "What is your acceptable ratio of price to value?"

### 6. Risk

- "Does this involve personal data? PDPL exposure?"
- "Are there approvals or audit requirements?"
- "Has a project like this failed here before? Why?"

### 7. Fit

- "What outcome would you stop us if we didn't deliver?"
- "What timeline must we beat?"
- "What proof do you need before going to retainer?"

## Fit Matrix

The matrix maps the client's dominant signal to the recommended
Dealix offer.

| Client situation | Recommended offer |
|---|---|
| Sales-led, CRM full but not converting | **Lead Intelligence Sprint** |
| Operations-led, one repetitive task burning hours | **AI Quick Win Sprint** |
| Knowledge-led, support/sales drowning in FAQs/SOPs | **Company Brain Sprint** |
| Already ran a successful pilot, wants ongoing cadence | **RevOps / AI Ops Retainer** |
| Wants enterprise governance, audit, scale | **Enterprise Sprint** (governance-first) |
| Cannot articulate problem, "explore AI" | **Paid Diagnostic** (not a free meeting) |
| Asks for spam automation / scraping | **Reject + content offer** |

## Disqualification Triggers

Stop qualification (politely) if any of the following arises:

- Asks for guaranteed results in writing.
- Refuses to share data source or owner.
- Insists on cold outbound automation.
- Requires us to bypass PDPL or internal approval.
- Will not name an executive sponsor.
- Budget signal more than 10x below offer band, no path to expand.

## Handoff Packet

When qualification completes successfully, the sales lead produces
a packet for Acceptance review:

- Client name, sector, size.
- Pain, Data, Process, Buyer, Value, Risk, Fit answers.
- Suggested offer + Base.
- Premium signals (per Pricing Engine bands).
- Disqualifier checks (pass/fail).
- Sponsor + decision-maker map.

## Workflow

1. Inbound or outbound lead lands in pipeline.
2. Discovery call run with this dimension list (≤45 min).
3. Sales lead writes Handoff Packet within 24h.
4. Acceptance Review by COO per
   `docs/company/PROJECT_ACCEPTANCE_SYSTEM.md`.
5. Pricing via `docs/company/PRICING_ENGINE.md` then Proposal via
   `docs/sales/PROPOSAL_LIBRARY.md`.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Inbound / outbound lead, intake form | Handoff Packet, fit recommendation | Sales Lead | Per opportunity |
| Updated offer/pricing | Refreshed fit matrix | CEO + Sales Lead | Quarterly |
| Acceptance feedback | Improved qualification script | Sales Lead | Monthly |

## Metrics

- **Qualified-to-Accepted rate** — target ≥70%.
- **Time from first call to Handoff Packet** — target ≤24h.
- **Disqualifier catch rate (pre-proposal)** — target 100%.
- **Sponsor named at proposal** — target 100% of accepted projects.

## Related

- `docs/sales/DISCOVERY_SCRIPT.md` — call script sibling.
- `docs/sales/DEMO_SCRIPT.md` — demo script sibling.
- `docs/sales/ONE_PAGER.md` — one-pager.
- `docs/sales/BATTLECARDS.md` — battlecards.
- `docs/sales/PROPOSAL_LIBRARY.md` — proposal generation downstream.
- `docs/company/PROJECT_ACCEPTANCE_SYSTEM.md` — acceptance gate.
- `docs/company/PRICING_ENGINE.md` — pricing downstream.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
