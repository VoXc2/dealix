# Dealix Stop Doing

> Companies don't die from not doing enough. They die from doing too many
> wrong things. This is the canonical list of what Dealix will not do —
> ever, or at least until specific gates open.

## Permanent stops (Dealix-Standard violations)

Dealix will **never**:

1. Sell a service below the readiness score floor (`SELLABILITY_POLICY.md`).
2. Accept a customer who insists on forbidden actions (cold WhatsApp, scraping, LinkedIn automation, guaranteed outcomes, PII without lawful basis).
3. Build features before repeated paid demand (Decision Rule 5).
4. Deliver reports without QA approval (5-gate + 80-point floor).
5. Deliver projects without a Proof Pack.
6. Offer Enterprise contracts before Enterprise Decision gate is met.
7. Compete as a cheap AI agency. Price reflects standard, not market floor.
8. Promise guaranteed business outcomes (revenue, leads, sales).
9. Answer Company Brain questions without a verified source.
10. Execute any external action without human approval per the approval matrix.

## Until-the-gate-opens stops

| Activity | Why blocked now | What unlocks it |
|----------|-----------------|----------------|
| Pure SaaS subscription | Service-assisted SaaS path is correct for Year-1 | After 15+ retainers + repeatable delivery |
| Multi-tenant RBAC | Premature without enterprise customer | First Enterprise contract signed |
| WhatsApp Business API integration | High compliance / spam risk | Mature consent registry + WhatsApp Business approval |
| Geographic expansion (UAE / GCC / MENA) | Local moat not proven yet | `docs/strategy/MENA_EXPANSION_LOGIC.md` gates met |
| Launching Dealix Academy | Authority not yet earned | 10+ customers + 3 published case studies |
| Hiring AE #2 | Capacity not justified | AE #1 closes SAR 3M trailing 6mo |
| Custom builds for enterprises | Productization not yet proven | 3+ retainers + audit-export capability |

## "We are not / will not" list (for the website + sales)

Public-facing version (use in marketing + sales calls):

> We are not an AI agency. We do not build chatbots. We do not sell tools.
> We do not promise pipelines. We do not run cold WhatsApp. We do not
> scrape. We do not automate LinkedIn. We do not answer without sources.
> We do not deliver without proof.
>
> We are an AI Operating Partner. We deliver operating outcomes with
> data readiness, workflow design, governance, measurable outputs, and
> proof of impact.

## How to use this list

- **Sales**: review monthly; every "no" must align with this list. Exceptions require CRO + CEO co-sign with documented gate path.
- **Engineering**: review monthly; backlog items in violation are rejected.
- **CS**: review monthly; client asks in violation route to `YES_BUT_PLAYBOOK.md`.

## Why this list exists

A "yes" to the wrong thing costs more than a "no". Every entry above is
captured because the wrong "yes" would damage:
- reputation (one bad delivery takes months to recover)
- margins (custom enterprise without readiness = -30% margin)
- compliance (one PDPL violation can end the company)
- focus (every "yes" to a not-ready item is a "no" to a Sellable one)

## Owner & cadence

- **Owner**: CEO. CRO + CTO + HoLegal review monthly.
- **Refresh**: monthly; the most important update each month is removing rows (i.e., a gate has opened).

## Cross-links

- `docs/company/DECISION_RULES.md`
- `docs/company/SELLABILITY_POLICY.md`
- `docs/company/DO_NOT_SELL_YET.md`
- `docs/governance/FORBIDDEN_ACTIONS.md`
- `docs/sales/YES_BUT_PLAYBOOK.md`
- `docs/enterprise/ENTERPRISE_DECISION.md`
