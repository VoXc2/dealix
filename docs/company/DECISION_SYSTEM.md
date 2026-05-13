# Decision System — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CEO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DECISION_SYSTEM_AR.md](./DECISION_SYSTEM_AR.md)

## Context

Dealix gets pulled in many directions every week: client requests,
feature ideas, hiring asks, partner pitches, conference invitations,
content topics. Without a system, the company drifts. The Decision
System is the single, mechanical filter every initiative passes
through before it consumes time or capital. It refines the
discretionary judgment used in
`docs/DEALIX_OPERATING_CONSTITUTION.md` and operationalizes the
strategic verdict in `docs/company/DEALIX_CEO_STRATEGY.md`. Use it
in weekly leadership review and inside the founder daily loop
(`docs/V14_FOUNDER_DAILY_OPS.md`).

## The 5 Filters

Every initiative (offer, project, feature, hire, partner, content
piece, internal tool, contract) is scored against the same five
filters. A filter is either **passed** or **failed**. There is no
partial credit.

### Filter 1 — Revenue Filter

> Will this help us **sell, renew, expand, or increase margin** in
> the next 90 days?

Passes if the initiative does at least one of:

- Generates a qualified sales opportunity.
- Closes an open opportunity.
- Renews or expands an existing client.
- Raises pricing power or reduces cost-to-serve.

Fails if the only justification is "interesting", "innovative",
"competitive parity", or "for the future".

### Filter 2 — Delivery Filter

> Can this be **delivered repeatedly with QA**, not heroically once?

Passes if the initiative does at least one of:

- Fits an existing productized sprint or retainer.
- Has an intake form, scope, and checklist (or one can be built
  inside the initiative itself).
- Has a defined QA gate (see `docs/quality/QA_SYSTEM.md`).
- Can be staffed by current team without a hero week.

Fails if delivery requires a custom workflow we cannot reproduce.

### Filter 3 — Governance Filter

> Can this be done **safely** — with approvals, logs, and no
> forbidden actions?

Passes only if all of the following hold:

- No personal-data scraping, cold WhatsApp, or LinkedIn automation.
- External actions require human approval (see
  `docs/product/GOVERNANCE_AS_CODE.md`).
- PDPL implications are mapped (see `docs/DPA_DEALIX_FULL.md`).
- Audit logs are written for any AI run or data movement.

Fails if any forbidden action category is touched.

### Filter 4 — Product Filter

> Can repeated work from this become a **reusable module, workflow,
> template, or playbook**?

Passes if the initiative does at least one of:

- Will produce a template, prompt, eval, SOP, or component asset.
- Will retire an existing manual step.
- Will feed `docs/product/PRODUCTIZATION_LEDGER.md`.

Fails if everything we produce is one-off and ungeneralizable.

### Filter 5 — Capital Filter

> Will this create **Service / Product / Knowledge / Trust / Market
> capital** as defined in `docs/company/DEALIX_CAPITAL_MODEL.md`?

Passes if the initiative deposits at least one of:

- **Service capital** — a sellable, repeatable service unit.
- **Product capital** — a reusable internal/external module.
- **Knowledge capital** — a vertical insight, objection, pattern.
- **Trust capital** — a Proof Pack, testimonial, audit record.
- **Market capital** — a public asset (post, benchmark, talk).

Fails if delivery leaves no asset behind.

## Decision Outcomes

After scoring 0–5 filters passed, the initiative gets routed to one
of six outcomes:

| Filters passed | Outcome | Meaning |
|---|---|---|
| 5 / 5 | **Sell now** | Add to standard offers, scale aggressively. |
| 4 / 5 | **Sell as pilot** | Run at controlled scale, capture missing filter. |
| 3 / 5 | **Build now** | Internal initiative; build before selling. |
| 2 / 5 | **Template only** | Document the pattern but do not invest cycles. |
| 1 / 5 | **Research only** | Low priority, parking lot, revisit quarterly. |
| 0 / 5 | **Reject** | Do not start. Log reason to decision archive. |

The headline rule:

> **If it does not sell, deliver, prove, govern, or compound — do
> not do it.**

Any initiative passing fewer than **3 of 5** filters does not enter
execution.

## How To Use It

1. **Intake** — any new idea is written on one line: "We should X
   because Y".
2. **Score** — leadership scores the 5 filters yes/no in <5 minutes.
3. **Route** — assign one of the six decision outcomes.
4. **Log** — write to the Decision Log (date, idea, score, outcome,
   owner, review date).
5. **Reopen rule** — a rejected idea can be reopened only if a new
   filter pass is achieved (e.g. new partner unlocks Revenue Filter).

Cadence:

- **Daily** — 1-2 fast scores during founder ops loop.
- **Weekly** — leadership review of the Decision Log.
- **Monthly** — re-score live initiatives that have drifted.
- **Quarterly** — purge or revive Research-only items.

## Worked Example

| Idea | Revenue | Delivery | Gov | Product | Capital | Score | Outcome |
|---|---|---|---|---|---|---|---|
| Lead Intelligence Sprint | Yes | Yes | Yes | Yes | Yes | 5/5 | Sell now |
| Custom enterprise data lake | Yes | No | Yes | No | Yes | 3/5 | Build now |
| Cold WhatsApp automation | Yes | Yes | **No** | Yes | No | 3/5 fails Gov | Reject |
| Build internal eval suite | No | Yes | Yes | Yes | Yes | 4/5 | Sell as pilot (productize first) |
| Attend small generic AI meetup | No | n/a | Yes | No | No | 1/5 | Research only |

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Idea backlog, client asks, partner asks, internal proposals | Decision Log entries, prioritized initiatives | CEO + leadership | Daily / Weekly |
| Capital ledger state | Filter 5 scoring inputs | CTO / CSO | Monthly |
| Service readiness scores | Filter 2 scoring inputs | COO | Monthly |

## Metrics

- **Filter score average across active initiatives** — target ≥4.0.
- **% of active initiatives scoring ≥3/5** — target 100%.
- **Rejected ideas logged with reason** — target 100% of rejections.
- **Decision-to-action latency** — median ≤7 days from intake to
  outcome.
- **Reopened ideas with new filter pass** — tracked, not capped.

## Related

- `docs/V14_FOUNDER_DAILY_OPS.md` — daily ops loop where filtering happens.
- `docs/EXECUTIVE_DECISION_PACK.md` — exec-level decision template sibling.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — constitutional rules backing filters.
- `docs/company/DEALIX_CEO_STRATEGY.md` — umbrella strategy.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — capital types referenced in Filter 5.
- `docs/product/GOVERNANCE_AS_CODE.md` — runtime guardrails for Filter 3.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
