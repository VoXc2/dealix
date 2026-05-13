# Delivery Command — Project Template

> Copy this file to `clients/<client_codename>/DELIVERY_COMMAND.md` at the
> start of every paying project. The file is the single source of truth for
> who is doing what and what's blocking us, refreshed daily by the project
> owner.

## Client
- **Codename**: `<sector>-<seq>` (e.g., BFSI-A1)
- **Vertical**:
- **Tier**: SME / Mid-market / Enterprise / Sovereign
- **Region**:
- **Service**: Lead Intelligence / AI Quick Win / Company Brain / …
- **SOW reference**: `templates/sow/<service>.md` — signed on YYYY-MM-DD

## Team
- **Delivery Owner**:
- **QA Reviewer** (must differ from Owner):
- **Founder oversight**: CEO

## Goal
One sentence the customer would write themselves.

## Timeline
- **Start**: YYYY-MM-DD
- **Target end**: YYYY-MM-DD
- **Current stage** (per `delivery_factory/stage_machine.py`): Discover / Diagnose / Design / Build / Validate / Deliver / Prove / Expand

## Current status
One paragraph. What's done, what's in flight, what's next.

## Blockers
- 1.
- 2.

## Pending client decisions
- 1.
- 2.

## QA status
- Latest Quality Score: __ / 100 (floor 80)
- 5-gate status: Business __ · Data __ · AI __ · Compliance __ · Delivery __

## Governance status
- Pending approvals:
- PII findings:
- Forbidden-claim catches:
- Source-attribution coverage:

## Proof Pack status
- Stage-7 captured? YES / NO
- Reference: `clients/<codename>/proof_pack.md`

## Next 3 actions

1.
2.
3.

## Daily log

| Date | Note |
|------|------|
| YYYY-MM-DD | |

## Cross-links

- `clients/<codename>/governance_events.md`
- `clients/<codename>/delivery_approval.md`
- `clients/<codename>/proof_pack.md`
- `clients/<codename>/POST_PROJECT_REVIEW.md` (created at close)
