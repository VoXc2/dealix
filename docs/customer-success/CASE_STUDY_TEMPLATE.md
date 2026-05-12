# Case Study — `<Customer Display Name>`

> **Use this template** for every paying customer who agrees to be referenced.
> Fill it during the QBR after they hit their first measurable outcome.
> Until a customer signs off on a written case study, **do not** publish
> them on the landing page or in sales decks. Synthetic case studies erode
> trust faster than they generate pipeline.

---

## Meta

| Field | Value |
| --- | --- |
| Customer name | _Acme Real Estate Co. (use legal name; confirm with customer)_ |
| Sector | _real-estate / construction / hospitality / SaaS / agency / etc._ |
| Geography | _Riyadh / Jeddah / Eastern Province / Multi-region_ |
| Headcount band | _10–50 / 50–200 / 200–1000 / 1000+_ |
| Tier | _Starter / Growth / Scale_ |
| Contract value (SAR/yr) | _redact if customer prefers; otherwise actual number_ |
| Contract start date | _YYYY-MM-DD_ |
| Reference contact | _name + title + email; with explicit permission to share_ |
| Permission scope | _logo only / logo + first name / full attribution + quote_ |
| Last reviewed | _YYYY-MM-DD by founder_ |

## 1. The before — what was broken

What was the customer trying to do, and what was getting in the way? **Be
specific.** Quantify the pain. The reader should recognise their own
business in the description.

- The problem: _2-3 sentences_
- The cost of the problem: _hours wasted / leads dropped / deals lost / SAR_
- Why existing tools (CRM, sales automation, custom scripts) failed
  to solve it: _1-2 sentences_

## 2. The decision — why Dealix

Capture the **buyer's reasoning**, not our marketing.

- Triggering event: _what made them start looking?_
- Alternatives considered: _HubSpot, Gong, Salesloft, in-house — be honest_
- Why Dealix won: _PDPL stance / Arabic-first / agentic flow / sovereign
  hosting / pricing — quote the customer if possible_

## 3. The deployment — what we did

A short, factual deployment narrative.

- Workflow scoped from `docs/product/CORE_WORKFLOWS.md` (Workflow 1 / 2 / 3).
- Integrations enabled: _list (HubSpot, WhatsApp, Calendly, n8n, etc.)_
- Time from contract signature to first production traffic: _days_
- Onboarding hours invested by Dealix: _hours_ (so we can compute LTV/CAC).

## 4. The after — measurable outcomes

**Only include metrics the customer is willing to attest to in writing.**
For every metric, name the baseline window, the post-deployment window,
and the method of measurement.

| Metric | Baseline | After | Delta | Source of truth |
| --- | --- | --- | --- | --- |
| Qualified leads / week | _N_ | _N_ | _+X%_ | _CRM export_ |
| Demo-to-close conversion | _%_ | _%_ | _+pp_ | _Pipeline report_ |
| Avg time-to-first-response | _hours_ | _hours_ | _−X%_ | _Email/WhatsApp logs_ |
| Net Revenue Retention | _%_ | _%_ | _+pp_ | _Finance system_ |
| _(your most credible metric)_ | _baseline_ | _after_ | _delta_ | _source_ |

Avoid vanity metrics. If a number can't be reproduced from a system of
record, it does not belong here.

## 5. The quote

A single paragraph in the customer's own voice. Have them write it (or
edit a draft) — never put words in their mouth.

> _"…we needed a system that respected PDPL and worked in Arabic from day
> one. Dealix shipped both, and our pipeline finally reflects how Saudi
> buyers actually behave."_
> — _Name, Title, Company_

## 6. Risks and caveats (private — internal-only section)

Not for the public version. Used for QBR honesty and future case-study
quality.

- Where did we underperform? _be specific_
- What did the customer compromise on?
- What does their renewal probability look like (1-5)? Why?
- What would we do differently?

## 7. Sign-off

| Stakeholder | Name | Signed? | Date |
| --- | --- | --- | --- |
| Customer reference contact | | | |
| Founder | | | |
| Customer legal/marketing (if logo used) | | | |

Without a `Signed = yes` in the customer reference contact row, **this
case study is internal-only**. No sales rep, partner, or AI agent may
quote it externally.

---

## How to publish

1. Copy this filled template to `landing/case-studies/<slug>.md`.
2. Generate the HTML view via the existing landing pipeline.
3. Add the customer logo to `landing/assets/case-studies/`.
4. Update `landing/case-studies/index.html` to surface the new story.
5. Notify customer success — they will reuse this case in QBRs and
   renewal conversations.

## How to rotate / retire

When the metrics are >12 months stale, re-validate with the customer or
move the case study to `landing/case-studies/archive/`. We do not show
out-of-date results as if they were current.
