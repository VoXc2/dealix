# AI Agent Governance Council — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AI_AGENT_GOVERNANCE_COUNCIL_AR.md](./AI_AGENT_GOVERNANCE_COUNCIL_AR.md)

## Context
As Dealix scales beyond a handful of agents and a handful of clients, the risk of ungoverned AI behavior grows faster than the value it produces. The AI Agent Governance Council is the standing body that decides which agents exist, what they may do, and on whose behalf. It enforces the principles encoded in `docs/DEALIX_OPERATING_CONSTITUTION.md` and the strategic intent in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`, and supplies the human accountability layer behind every AI workflow Dealix runs for itself or a client.

## Purpose
The Council exists to govern AI agents, workflows, risks, and value across client environments — both Dealix-internal environments and any AI capability Dealix deploys into a client workspace. It is the named, accountable body answering the procurement question: *"who, on your side, signed off on this AI behavior?"*

## Internal roles
The Council is intentionally cross-functional. Each role has a defined seat and a defined accountability.

- **Business Owner** — accountable for business value, scope, and proof of impact.
- **Delivery Owner** — accountable for engagement-level execution and quality.
- **Technical Owner** — accountable for agent design, model routing, eval coverage.
- **Governance Reviewer** — accountable for risk, compliance, and policy fit.
- **QA Reviewer** — accountable for output quality, eval pass rate, and rework.
- **Client Success Owner** — accountable for client satisfaction, expansion, and Report Card delivery.

A quorum requires at least the Delivery Owner, the Governance Reviewer, and one of Business Owner / Technical Owner present.

## Responsibilities
The Council holds the following standing responsibilities:

1. **Approve new agents** before they are activated against any production workspace.
2. **Classify autonomy level** (0–6) for each agent per workspace, per service.
3. **Approve data access** for each agent against the workspace data classifications.
4. **Monitor behavior** through eval scores, QA scores, incident logs, and AI run provenance.
5. **Review incidents** and approve mitigation, rollback, or retirement actions.
6. **Retire redundant agents** that overlap, are unused, or have failed monitoring.
7. **Approve enterprise deployments** before any agent is promoted from pilot into recurring enterprise operation.

## Cadence
- **Weekly** for active enterprise clients — review behavior, incidents, eval scores, AI cost, and any pending approval requests.
- **Monthly** for internal governance — review inventory, sprawl, retirements, policy updates, and the company-wide Report Card.
- **Ad-hoc** within 24 working hours for incident response or high-risk agent approval.

## Decision record
Every Council decision is logged with: date, agents reviewed, decision (approve / hold / reject / retire), autonomy level set, data access granted, approver list, and link to the run or incident triggering the review.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Agent registration requests, eval scores, incident logs | Approved agent catalogue, autonomy classifications | Council | Weekly / Monthly |
| Client policy pack, regulatory updates | Governance configuration per workspace | Governance Reviewer | Per engagement |
| Monthly Report Card draft | Approved Report Card | Council + Client Success | Monthly |
| Incident reports | Mitigation / rollback / retirement decision | Council | Within 24h |

## Metrics
- Council Coverage — % of active agents reviewed in the last 30 days.
- Decision Latency — median hours from agent registration to Council decision.
- Incident-Driven Retirements — count of agents retired due to incidents per quarter.
- Approval-Without-Rework Rate — % of Council approvals that did not require a second review pass.

## Related
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating constitution the Council enforces
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability and eval feeds powering Council reviews
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan the Council aligns with
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
