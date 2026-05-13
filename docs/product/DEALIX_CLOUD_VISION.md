# Dealix Cloud Vision — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** CPO + Technical Owner
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [DEALIX_CLOUD_VISION_AR.md](./DEALIX_CLOUD_VISION_AR.md)

## Context
The services Dealix sells today converge over time into a platform. Dealix Cloud is the product expression of that platform: the place where client AI capabilities are operated, governed, and proven. The vision in this file describes the modules, the users, and the promise, anchored on the architectural plan in `docs/BEAST_LEVEL_ARCHITECTURE.md`, the reliability work in `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`, and the autonomous revenue OS in `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md`.

## Modules
Dealix Cloud is composed of ten interlocking modules. Each is buildable and saleable as a step on the Governance Product Ladder, and together they form the Enterprise AI Control Tower.

- **Client Workspace** — the single tenant surface for a client's people, agents, workflows, and data.
- **Capability Scorecards** — maturity tracking per capability stream per client.
- **Data OS** — the data layer: connectors, classifications, retention, and access policies.
- **Revenue OS** — agents and workflows for outreach, qualification, and opportunity progression.
- **Knowledge OS** — sourced, versioned, retrievable internal knowledge.
- **Workflow OS** — the orchestration layer for governed AI workflows.
- **Governance OS** — runtime governance: identity mirroring, action class enforcement, provenance.
- **Proof Ledger** — the immutable record of proof events delivered per client.
- **AI Control Tower** — cross-workspace monitoring for the enterprise customer and for Dealix itself.
- **Reporting Dashboard** — the Enterprise AI Report Card and the executive dashboards.

## User roles
The Cloud is designed for the roles that actually decide and execute inside customer organizations:

- **Founder / CEO** — strategic visibility, decisions, narrative.
- **Sales lead** — Revenue OS surface, pipeline view, agent outputs.
- **Support lead** — Customer-facing workflows and quality.
- **Operations lead** — internal workflow status, productivity, costs.
- **Governance reviewer** — risk register, incidents, blocked actions, approval queue.
- **Dealix delivery owner** — the cross-customer view used to run engagements.

## Core promise
The Dealix Cloud promise, stated plainly:

> Turn AI projects into governed operating capabilities.

Operationally, this means: every workflow has an owner, a policy, an audit trail, a cost line, and a value record. The Cloud is where that becomes real.

## What it is not
Dealix Cloud is not a model lab, not a chat interface, not a generic automation platform. It is the operating layer for governed, proven AI capabilities — specifically targeted at Saudi and Gulf enterprises and their compliance reality.

## Sequencing
The Cloud is built in alignment with the Governance Product Ladder. Modules ship in the order that maximizes early enterprise revenue: Workspace + Governance OS + Proof Ledger first, then Revenue/Knowledge/Workflow OS, then AI Control Tower, then Marketplace.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Module build decisions | Shipped capabilities per workspace | CPO + Tech | Per release |
| Client onboarding | Provisioned workspace + scorecards | Delivery | Per engagement |
| Reliability and security work | Cloud SLO posture | Reliability Lead | Continuous |

## Metrics
- Workspace Activation Rate — % of contracted workspaces fully activated within 30 days.
- Module Adoption — % of contracted modules in active use per workspace.
- Cloud-Backed Service Revenue — share of total revenue running through Cloud-operated workflows.
- Proof Ledger Density — proof events per active workspace per quarter.

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architectural plan
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — reliability hardening
- `docs/DEALIX_V3_AUTONOMOUS_REVENUE_OS.md` — Revenue OS direction
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
