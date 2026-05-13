# Enterprise AI Report Card — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Client Success Owner
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [ENTERPRISE_AI_REPORT_CARD_AR.md](./ENTERPRISE_AI_REPORT_CARD_AR.md)

## Context
Large clients do not stay sold by promises — they stay sold by evidence. The Enterprise AI Report Card is the monthly, board-quality narrative Dealix delivers to every enterprise account, showing usage, quality, governance, value, cost, and capability maturity. It is the artifact that turns Dealix from "AI vendor" into "AI operating partner". It draws on the same metric definitions used in `docs/BUSINESS_KPI_DASHBOARD_SPEC.md`, the executive lens in `docs/EXECUTIVE_DECISION_PACK.md`, and the financial framing in `docs/FINANCE_DASHBOARD.md`.

## Sections
The Report Card is a single document, six sections, delivered monthly:

### 1. Usage
- Active workflows in the workspace.
- Active agents and their categories.
- AI runs total and by workflow.
- Approvals raised, approved, rejected.

### 2. Quality
- Average QA score across delivered outputs.
- Eval pass rate by service.
- Rework rate (outputs producing a v2 within 30 days).
- Notable quality wins and quality misses.

### 3. Governance
- Blocked actions by class.
- PII flags raised and resolved.
- Approval delays (median + outliers).
- Incidents and incident resolution times.

### 4. Value
- Proof events recorded.
- Hours saved (with method).
- Opportunities generated or progressed.
- Reports automated.

### 5. Cost
- Total AI cost for the month.
- Cost per workflow.
- Cost per proof event.
- Trend versus prior months and budget.

### 6. Capability Maturity
Maturity rating per capability stream:

- Revenue
- Customer
- Operations
- Knowledge
- Data
- Governance
- Reporting

Each is scored on a 1–5 scale with a one-line narrative for progress and next step.

## Delivery
- Cadence: monthly, calendar-aligned, delivered within the first 5 business days of the following month.
- Owner: Client Success Owner, signed by Delivery Owner and Governance Reviewer.
- Format: PDF or in-workspace report with provenance footer.
- Review: live monthly review meeting with the client executive sponsor.

## Closing block
Every Report Card ends with three explicit items:

- **Decisions requested from the client** — new workflows, expanded scope, hiring or training requests.
- **Risks flagged** — what Dealix sees as a risk to the client's program.
- **Next month's plan** — committed workflows, eval focus, governance work.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Run logs, eval scores, incident logs, AI cost, value events | Draft Report Card | Client Success | Monthly |
| Governance Council approval | Signed Report Card | Council | Monthly |
| Executive review meeting feedback | Action items + plan for next month | Delivery Owner | Monthly |

## Metrics
- Report Card On-Time Rate — % of monthly Report Cards delivered within 5 business days.
- Decision-Acted-On Rate — % of requested client decisions acted on within the month.
- Maturity Trend — count of capability streams that improved their maturity score quarter-over-quarter.
- Value-Reported-vs-Delivered — ratio of reported value to invoiced value.

## Related
- `docs/BUSINESS_KPI_DASHBOARD_SPEC.md` — KPI definitions used in the card
- `docs/EXECUTIVE_DECISION_PACK.md` — executive lens behind the closing block
- `docs/FINANCE_DASHBOARD.md` — financial framing for the cost section
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
