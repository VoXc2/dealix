# Governance Product Ladder — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Governance Lead + Commercial Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [GOVERNANCE_PRODUCT_LADDER_AR.md](./GOVERNANCE_PRODUCT_LADDER_AR.md)

## Context
Most clients do not need every governance capability on day one — they need a ladder they can climb as their AI maturity grows. Dealix packages governance as five ascending levels, each a saleable engagement and each a natural step into the next. This is how governance becomes a product, not a one-off project. The ladder sits alongside the broader offer architecture in `docs/OFFER_LADDER_AND_PRICING.md`, the service ladder in `docs/COMPANY_SERVICE_LADDER.md`, and the buyer-facing trust posture in `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`.

## The five levels

### Level 1 — AI Usage Policy
The minimum credible governance posture: written rules for employees, an approval matrix, an employee guide, a tool list.
- **Outcome:** auditable rules in place; employees know what is OK.
- **Time:** 2 weeks.
- **Deliverables:** the Client AI Policy Pack at `docs/services/client_ai_policy_pack/`.

### Level 2 — Data & AI Risk Review
Deep review of the client's data, tools, vendors, and use cases for AI exposure.
- **Outcome:** a risk register, a tools-and-data heatmap, prioritized remediation plan.
- **Time:** 3–4 weeks.
- **Deliverables:** risk register, vendor list, prioritized remediation backlog.

### Level 3 — AI Governance Program
A standing governance program: approval workflows, audit logs, risk register, periodic review cadence.
- **Outcome:** an operating governance function the client can run with light Dealix support.
- **Time:** 6–8 weeks to stand up; ongoing operation.
- **Deliverables:** approval workflow setup, audit log discipline, risk register cadence, monthly review.

### Level 4 — Runtime Governance
Governance checks embedded directly in workflows: permission mirroring, action class enforcement, provenance, rollback.
- **Outcome:** governance is no longer a meeting — it is enforced at runtime.
- **Time:** 8–12 weeks per service.
- **Deliverables:** runtime governance configuration per workspace, integrated with provenance and the AI Action Control framework.

### Level 5 — Enterprise AI Control Tower
A central, monitored, reported view across all agents, workflows, costs, and risks for the enterprise.
- **Outcome:** a board-grade operating view for AI as a category.
- **Time:** ongoing.
- **Deliverables:** Control Tower dashboards, monthly Enterprise AI Report Card, quarterly executive review.

## Climbing the ladder
- Clients enter at the level that matches their maturity.
- Each level is a productized engagement with fixed-fee pricing and a known timeline.
- Lower levels are required dependencies for higher levels: a client cannot purchase Level 4 without the policy of Level 1, the risk register of Level 2, and the governance program of Level 3 in place — though Dealix may deliver them in parallel for an enterprise on-ramp.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client maturity assessment | Recommended entry level + sequencing plan | Governance Lead | Pre-sale |
| Engagement deliverables | Level-specific assets and configurations | Delivery Owner | Per engagement |
| Council reviews + Report Card | Trigger to climb to next level | Council + Client Success | Quarterly |

## Metrics
- Ladder Entry Mix — distribution of new engagements by level.
- Climb Rate — % of clients who advance one level within 12 months.
- Time-Per-Level — median weeks to deliver each level.
- Renewal Rate — % of standing levels (3, 4, 5) renewed at term.

## Related
- `docs/OFFER_LADDER_AND_PRICING.md` — broader offer architecture
- `docs/COMPANY_SERVICE_LADDER.md` — full service ladder
- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` — buyer-facing trust pack
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
