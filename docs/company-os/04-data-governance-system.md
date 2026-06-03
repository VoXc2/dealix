# Data Governance System

## Purpose
Make Dealix data reliable enough for dashboards, AI workflows, customer proof, and executive decisions.

## Data ownership

| Data domain | Examples | Owner | Review cadence |
|---|---|---|---|
| Accounts | Company, segment, ICP, source | GTM/RevOps | Weekly |
| Opportunities | Stage, value, owner, next step | Sales/RevOps | Weekly |
| Customers | Health, usage, onboarding, proof | CS | Weekly |
| Product usage | Activation, workflow events, defects | Product/Engineering | Weekly |
| AI outputs | prompts, outputs, evaluation, incidents | AI/Product | Weekly |
| Finance | cash, revenue, burn, margin | Finance/Founder | Monthly |
| Security | access, incidents, vendors, risks | Security/Engineering | Monthly |

## Data quality dimensions

| Dimension | Definition | Example check |
|---|---|---|
| Completeness | Required fields are present | Every opportunity has owner and next step |
| Accuracy | Field reflects reality | Stage matches buyer status |
| Freshness | Data is recent enough | Pipeline updated in last 7 days |
| Consistency | Same meaning across systems | KPI definitions match dashboard |
| Traceability | Source is known | Account source recorded |
| Permission | Access is appropriate | No unnecessary admin access |

## KPI definition template

| Field | Detail |
|---|---|
| KPI name | TBD |
| Business question | TBD |
| Formula | TBD |
| Source system | TBD |
| Owner | TBD |
| Update cadence | TBD |
| Thresholds | Green / Yellow / Red |
| Decision attached | TBD |

## Data change rules

- Do not create a new metric without owner and formula.
- Do not use dashboard numbers without source system.
- Do not send customer data to AI tools without documented purpose.
- Do not keep stale account or pipeline data past review cadence.
- Do not merge data imports without preview and rollback plan.

## Weekly data review

- Missing critical fields
- Stale opportunities
- Conflicting KPI definitions
- Duplicate accounts
- Unreviewed AI outputs
- Customer data risks
- Dashboard decision gaps

## Required artifacts

- KPI dictionary
- Data owner map
- Data quality checklist
- Import checklist
- AI data boundary note
- Dashboard source map
