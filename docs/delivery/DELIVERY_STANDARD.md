# Delivery Standard — Constitution · Foundational Standards

**Layer:** Constitution · Foundational Standards
**Owner:** Delivery Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DELIVERY_STANDARD_AR.md](./DELIVERY_STANDARD_AR.md)

## Context
The Delivery Standard is Dealix v1 for running an engagement end to
end. It is the operational expression of the operating equation in
`docs/company/OPERATING_EQUATION.md` and of the operating constitution
in `docs/DEALIX_OPERATING_CONSTITUTION.md`. Every Dealix sprint, pilot,
or retainer must follow the eight stages defined here. It is paired
with `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` for relationship management
and `docs/business/MANAGED_PILOT_OFFER.md` for the productized pilot
shape.

## The Eight Stages
> Discover → Diagnose → Design → Build → Validate → Deliver → Prove →
> Expand

Each stage has a defined owner, entry criteria, exit criteria, and a
named artifact. A project cannot enter a stage until the previous
stage's exit criteria are met. Skipping is a process defect.

## Stage Matrix
| # | Stage | Owner | Entry criteria | Exit artifact |
|---|---|---|---|---|
| 1 | Discover | Delivery lead | Signed scope | Intake form completed |
| 2 | Diagnose | Data lead | Intake form | DRS record + diagnosis brief |
| 3 | Design | AI platform lead | Diagnosis brief | Workflow design + governance plan |
| 4 | Build | AI platform lead | Design approved | Drafts generated and logged |
| 5 | Validate | QA reviewer | Drafts available | QA score ≥ 85 |
| 6 | Deliver | Delivery lead | Approved drafts | Delivery note + audit event |
| 7 | Prove | Delivery lead | Delivery complete | Proof pack with before/after |
| 8 | Expand | Revenue | Proof pack | Renewal proposal signed or declined |

## Universal Rules
- No stage may be skipped. Any skip generates a defect ticket.
- Every stage produces an artifact stored under the project record.
- Every external action in stages 4-6 requires an Approval per
  `docs/governance/APPROVAL_MATRIX.md`.
- Every project must produce all four required outputs from the
  Operating Equation by the end of stage 7.

## Quality Bar Per Stage
- Discover — every required intake field captured.
- Diagnose — DRS computed and decision recorded.
- Design — workflow declares the governance class and approval path.
- Build — every AIRun logged in the ledger.
- Validate — QA score ≥ 85 or rework triggered.
- Deliver — delivery note signed off and audit event written.
- Prove — proof pack contains a hero metric tied to an audit event.
- Expand — renewal or expansion proposal sent within 7 days of stage
  7 close.

## Roles
- **Delivery lead** — owns the engagement end to end and the client
  relationship.
- **Data lead** — owns Diagnose; signs off on DRS and cleanup plan.
- **AI platform lead** — owns Design and Build; signs off on workflow
  governance.
- **QA reviewer** — owns Validate; bilingual QA pass.
- **Revenue** — owns Expand; renewal motion.
- **Governance lead** — gates every stage where Approval is required.

## Cadence
- Daily standup during Build and Validate.
- Weekly client check-in across all stages.
- Stage gate review at every stage transition.
- Closeout review at end of stage 7.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Signed scope | Stage gate checklist | Delivery lead | Per project |
| Stage gate review | Go/no-go decision | Delivery lead | Per stage |
| QA review | Delivery approval | QA reviewer | Per delivery |
| Proof pack | Renewal proposal | Revenue | Per project |

## Metrics
- **Stage gate compliance** — share of stage transitions with all
  exit criteria met. Target: 100%.
- **On-time delivery** — share of projects that hit the contract
  end date. Target: ≥ 90%.
- **QA pass rate** — share of deliveries clearing QA on first
  review. Target: ≥ 80%.
- **Renewal-within-30-days** — Target: ≥ 60%.

## Related
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — customer success motion.
- `docs/V14_FOUNDER_DAILY_OPS.md` — founder daily ops.
- `docs/ops/DAILY_OPERATING_LOOP.md` — daily ops loop.
- `docs/business/MANAGED_PILOT_OFFER.md` — productized pilot.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
