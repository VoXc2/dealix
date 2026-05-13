# Dealix CEO Strategy — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CEO (Sami)
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DEALIX_CEO_STRATEGY_AR.md](./DEALIX_CEO_STRATEGY_AR.md)

## Context

This is the umbrella strategy document for Dealix. It collapses the
CEO, CTO, and CSO points of view into one operating verdict, one
North Star, one commercial promise, and one execution sequence. Every
other Operating Manual file (DECISION_SYSTEM, SERVICE_READINESS_SYSTEM,
PROJECT_ACCEPTANCE_SYSTEM, PRICING_ENGINE, MARGIN_GUARD, COMMANDMENTS,
QA_SYSTEM, ARABIC_BUSINESS_QUALITY, SALES_QUALIFICATION, PROPOSAL_LIBRARY,
CLIENT_HEALTH_SCORE, RETAINER_OPERATING_SYSTEM, PRODUCTIZATION_SYSTEM,
KNOWLEDGE_CAPITAL_SYSTEM, TRUST_CAPITAL_SYSTEM, MARKET_CAPITAL_SYSTEM,
PARTNER_OPERATING_SYSTEM, CATEGORY_POINT_OF_VIEW) plugs into this doc.
It tightens and replaces ad-hoc strategy memos and refines the direction
already set in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` and
`docs/DEALIX_OPERATING_CONSTITUTION.md`.

## Strategic Verdict

Dealix does **not** compete as:

- A CRM vendor.
- An AI chatbot agency.
- A scraping / lead-list vendor.
- An automation freelancer or no-code shop.
- A generic "AI consultancy".

Dealix competes as the **Saudi AI Revenue & Operations System** —
"the governed AI operating layer for Saudi companies." Everything we
sell, build, hire, write, or publish must reinforce that single
position. If a decision does not reinforce it, the decision is wrong.

## North Star

> Dealix is the operating system that helps Saudi companies turn
> data, workflows, and knowledge into **governed, measurable,
> AI-powered business capabilities** — Arabic-first, proof-led,
> PDPL-aligned, and ready for Vision 2030 buyers.

The North Star is the test for the next 24 months of work. Any feature,
service, partner, hire, or model decision that does not move the
company closer to that operating system is deprioritized.

## Commercial Promise

We sell five transitions, in this order:

1. **From chaos to system** — data, workflow, and approvals get
   organized into a documented operating layer.
2. **From data to opportunities** — the system surfaces ranked,
   reasoned, governed business opportunities from existing data.
3. **From AI experiments to operating capability** — pilots become
   reusable capabilities with QA, evals, and ownership.
4. **From delivery to proof** — every engagement ends with a Proof
   Pack (anonymized metrics, before/after, governance record).
5. **From project to retainer** — proven capabilities convert to a
   monthly operating cadence (retainers) — not "support".

If a buyer does not understand at least three of these transitions
inside the first 30 minutes, we have not pitched Dealix. We have
pitched a generic AI vendor.

## Strategic Thesis

AI alone does not create business value in Saudi Arabia. Value comes
from the **stack** under the AI:

| Layer | Required because |
|---|---|
| Clean data | Models are useless on dirty inputs |
| Clear workflow | Outputs need a destination to be used |
| Human approval | Saudi enterprises will not run autonomous external actions |
| Governance | PDPL, internal policy, and reputation require it |
| QA + evals | Buyers need repeatable trustworthy quality |
| Measurable proof | Otherwise pilots cannot convert to retainers |
| Recurring cadence | Without it, value is a single moment, not a system |

Dealix is the firm that productizes this stack, in Arabic, for Saudi
and MENA buyers. That is the moat.

## Saudi Context

- **PDPL** is now operational; data residency, consent, retention,
  cross-border, and breach reporting are decision factors in every
  enterprise deal.
- **Vision 2030** is forcing AI adoption — but enterprises lack
  internal capability. They want a partner that handles governance.
- **Arabic** quality is a hard differentiator. Most global vendors
  produce business-broken Arabic.
- **SMEs and mid-market** want outcomes, not infrastructure. They
  cannot operate raw LLMs. They will pay for a capability.
- **Enterprises** want auditability, approvals, and a proof trail
  more than they want raw model power.

## The 6 Systems

The company runs on six interlocking systems. Each has its own
canonical Operating Manual doc.

| # | System | Owner | Canonical doc |
|---|---|---|---|
| 1 | Revenue | CEO + Sales | `docs/sales/SALES_QUALIFICATION.md` + `docs/company/PRICING_ENGINE.md` |
| 2 | Operations | COO (interim CEO) | `docs/retainers/RETAINER_OPERATING_SYSTEM.md` + `docs/company/PROJECT_ACCEPTANCE_SYSTEM.md` |
| 3 | Knowledge | CTO/CSO | `docs/company/KNOWLEDGE_CAPITAL_SYSTEM.md` |
| 4 | Customer | CSM | `docs/client/CLIENT_HEALTH_SCORE.md` |
| 5 | Governance | CTO + Legal | `docs/company/TRUST_CAPITAL_SYSTEM.md` + `docs/DPA_DEALIX_FULL.md` |
| 6 | Proof | CEO | `docs/company/TRUST_CAPITAL_SYSTEM.md` + Proof Pack templates |

All six must run together. Removing any one collapses the model:
revenue without governance loses enterprises; governance without
proof loses pilots; proof without product loses margin.

## Top 3 Offers (Start Here)

We do **not** sell a menu. We sell three sprints. Each one is the
front door to a six-system engagement.

1. **Lead Intelligence Sprint** — turns existing CRM/data into a
   ranked, reasoned, governed list of opportunities. Front door for
   sales-led companies. See `docs/sales/LEAD_INTELLIGENCE_SALES_PAGE.md`.
2. **AI Quick Win Sprint** — picks one repetitive operational task,
   builds it into a governed AI workflow with QA + approvals. Front
   door for operations-led companies. See
   `docs/sales/AI_QUICK_WIN_SALES_PAGE.md`.
3. **Company Brain Sprint** — productizes knowledge (SOPs, contracts,
   FAQs, product docs) into a governed, Arabic-first answer system.
   Front door for knowledge-led companies. See
   `docs/sales/COMPANY_BRAIN_SALES_PAGE.md`.

Each sprint must end with a Proof Pack and a retainer proposal.

## Technical Moat (CTO View)

We build the layer **above** the LLM, not the LLM itself. Components:

- **Saudi localization** — Arabic tokenization, gender/register
  handling, business idioms, Hijri/Gregorian, PDPL-safe defaults.
- **Arabic Quality System** — see
  `docs/quality/ARABIC_BUSINESS_QUALITY.md`.
- **Runtime governance** — approvals, forbidden actions, scope locks,
  see `docs/product/GOVERNANCE_AS_CODE.md`.
- **Proof Ledger** — every output writes to an evidence record.
- **Capital Ledger** — every engagement deposits Service / Product /
  Knowledge / Trust / Market capital, tracked in
  `docs/company/DEALIX_CAPITAL_MODEL.md`.
- **Capability Maturity Model** — see
  `docs/company/CAPABILITY_MATURITY_MODEL.md`.
- **Productized services** — see
  `docs/company/SERVICE_CATALOG_V1.md` and
  `docs/product/PRODUCTIZATION_LEDGER.md`.
- **LLM gateway** — model routing per task class, cost-aware, evals
  enforced — see `docs/AI_MODEL_ROUTING_STRATEGY.md`.
- **AI Run Ledger** — every run captures inputs, prompts, model,
  cost, evals, approvals — see `docs/product/AI_RUN_PROVENANCE.md`.
- **Data Readiness** — checked at intake, see
  `docs/company/PROJECT_ACCEPTANCE_SYSTEM.md`.
- **Client Workspace** — single environment per client, with their
  scoped knowledge, governance rules, retainer cadence.

## Business Moat (CSO View)

- **Saudi-first** — built on PDPL, Arabic register, Saudi buyer
  rhythm. Global vendors cannot replicate this without local presence.
- **Proof-led** — Proof Packs as the unit of marketing.
- **Governance-first** — approvals and audit are default, not
  add-on. Enterprises sign because of this.
- **Productized** — repeated work becomes a reusable module. Margin
  rises every quarter — see `docs/company/UNIT_ECONOMICS.md`.
- **Capital accumulation** — every project deposits capital. The
  company gets stronger per delivery — see
  `docs/company/DEALIX_CAPITAL_MODEL.md`.

## Do Not Build

- A general-purpose CRM.
- A standalone chatbot product for marketing sites.
- A scraping tool for personal data.
- A marketplace of AI agents.
- An "AI employee" branded as autonomous.
- A no-code workflow builder.
- A consumer app.
- A multi-region SaaS before Saudi dominance.
- An internal LLM (we route, not train).
- Anything we cannot QA or govern.

## Build Now

- The three top offers (Lead / Quick Win / Company Brain) as fully
  productized sprints with intake → delivery → QA → Proof Pack.
- The five Operating Manual systems below.
- A single Proof Pack template and Proof Ledger.
- A single Arabic Quality scoring system.
- A single Pricing Engine (`docs/company/PRICING_ENGINE.md`).
- A single Decision System
  (`docs/company/DECISION_SYSTEM.md`).
- A single Retainer Operating System
  (`docs/retainers/RETAINER_OPERATING_SYSTEM.md`).
- A single Partner Program
  (`docs/partners/PARTNER_OPERATING_SYSTEM.md`).
- Capital ledgers (Knowledge / Trust / Market) wired to delivery.

## CEO Success Criteria

A quarter is successful if **all** the following hold:

1. **Narrow entry** — we only sold the three approved offers.
2. **High-trust delivery** — every project ended with a Proof Pack
   and a satisfied executive sponsor.
3. **Proof-backed marketing** — every public claim links to a Proof
   Pack, anonymized metric, or approved testimonial.
4. **Productize** — at least one manual step became a template,
   script, or internal tool — tracked in
   `docs/product/PRODUCTIZATION_LEDGER.md`.
5. **Retainer convert** — at least 40% of completed sprints
   converted into a retainer.
6. **Saudi-first** — Arabic Business Quality score ≥85 on all
   client-visible outputs.
7. **Governance moat** — zero unsafe actions, zero PDPL escalations,
   100% approval coverage on external actions.

## Failure Modes

These are the ways Dealix dies. Each has a guardrail.

| Failure mode | Guardrail |
|---|---|
| Premature SaaS | `docs/product/PRODUCTIZATION_SYSTEM.md` rule: no SaaS module before internal tool proves repeated value. |
| Trying to sell everything | `docs/company/DECISION_SYSTEM.md` 5-filter rule. |
| Accepting unsafe projects | `docs/company/PROJECT_ACCEPTANCE_SYSTEM.md` reject-if list. |
| Building without repetition | `docs/product/PRODUCTIZATION_SYSTEM.md` 3+ repetition trigger. |
| Skipping proof | `docs/company/TRUST_CAPITAL_SYSTEM.md` claim rule. |
| Underpricing | `docs/company/PRICING_ENGINE.md` discount rule + `docs/company/MARGIN_GUARD.md`. |
| Premature enterprise expansion | `docs/company/CAPABILITY_MATURITY_MODEL.md` gate. |
| Losing Arabic quality | `docs/quality/ARABIC_BUSINESS_QUALITY.md` scoring. |
| Capital not compounding | `docs/company/DEALIX_CAPITAL_MODEL.md` ledgers. |

## Bottom Line

**Sprint → Proof → Retainer → Product → Standard.**

That is the only sequence Dealix runs. Sprints earn the right to
deliver retainers. Retainers earn the right to productize. Products
earn the right to define a standard. The standard is what makes
Dealix the category — see
`docs/strategy/CATEGORY_POINT_OF_VIEW.md`.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Market signals, partner pipeline, client wins/losses | North Star, top offers, capital allocation | CEO | Monthly |
| Tech stack risks, eval scores | Build/no-build verdicts | CTO | Monthly |
| Category signals, competitive intel | Positioning updates | CSO | Quarterly |
| Capital ledgers (Service/Product/Knowledge/Trust/Market) | Strategic priorities | CEO + CSO | Monthly |

## Metrics

- **Top-3-offer share of pipeline** — % of pipeline that is one of the three approved offers (target ≥80%).
- **Retainer conversion rate** — % of completed sprints converting to retainer (target ≥40%).
- **Proof Pack coverage** — % of delivered projects with a published Proof Pack (target 100%).
- **Arabic Business Quality score** — average across client-visible outputs (target ≥85).
- **Governance breach count** — unsafe actions, PDPL escalations, missing approvals (target 0).
- **Capital deposit rate** — Knowledge/Trust/Market assets deposited per delivery (target ≥3 per project).
- **Gross margin by track** — Sprint ≥70%, Retainer ≥65%, Enterprise 50-70%.

## Related

- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — long-form strategic plan this CEO doc collapses.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — constitutional rules that bind this strategy.
- `docs/BUSINESS_MODEL.md` — revenue model, segments, channels.
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — system architecture under the moat.
- `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md` — Arabic master operating model.
- `docs/strategic/DEALIX_CATEGORY_EXECUTIVE_SUMMARY_EN.md` — category brief.
- `docs/company/DEALIX_MASTER_OPERATING_BLUEPRINT.md` — execution blueprint sibling.
- `docs/company/DEALIX_CONSTITUTION.md` — company-level constitution sibling.
- `docs/company/DEALIX_CAPITAL_MODEL.md` — capital ledgers powering the moat.
- `docs/company/DECISION_SYSTEM.md` — 5-filter decision system (L1).
- `docs/company/SERVICE_READINESS_SYSTEM.md` — readiness scoring (L2).
- `docs/company/PROJECT_ACCEPTANCE_SYSTEM.md` — intake gate (L3).
- `docs/company/PRICING_ENGINE.md` — pricing formula (L4).
- `docs/company/MARGIN_GUARD.md` — margin guardrail (L5).
- `docs/company/COMMANDMENTS.md` — 10 commandments (L6).
- `docs/quality/QA_SYSTEM.md` — QA framework (L7).
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
