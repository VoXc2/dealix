# Enterprise Governance Layer — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Governance Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [ENTERPRISE_GOVERNANCE_LAYER_AR.md](./ENTERPRISE_GOVERNANCE_LAYER_AR.md)

## Context
Enterprise buyers in Saudi Arabia and the wider Gulf do not buy AI tools — they buy *governed AI capabilities*. Before a CIO, CFO, or Risk Committee approves a Dealix engagement they ask: who owns this workflow, who approved this action, what data did the model see, was PII redacted, can we roll back, where is the audit trail, what did this cost, and where is the proof of value. Layer 5 — Enterprise Governance — exists to remove the gap between "AI demo" and "enterprise-ready operating capability". It plugs into the wider model defined in `docs/DEALIX_OPERATING_CONSTITUTION.md` and the strategic plan in `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md`, and it is the layer enterprise procurement, legal, and risk teams read first.

## Seven domains of enterprise governance
Enterprise readiness at Dealix is governed across seven domains. Every Dealix service, agent, and deliverable must answer each question for the relevant client environment.

1. **People** — who owns the workflow, who approves changes, who signs off on AI-assisted decisions.
2. **Processes** — which workflows are AI-assisted, which are human-approved, which are blocked from automation entirely.
3. **Data** — what information AI agents are allowed to access, what classifications apply, what redaction is enforced.
4. **Agents** — which agents exist, what each can do, what autonomy level they hold, and who is accountable for their behavior.
5. **Actions** — what AI is allowed to recommend, queue, or execute; where the human-in-the-loop sits.
6. **Risk** — what must be reviewed, logged, blocked, escalated; how incidents are handled.
7. **Value** — what business value is being proven, measured, and reported back to the buyer.

## The enterprise interrogation
When Dealix sells into an enterprise account, the buyer asks the same family of questions. The Enterprise Governance Layer pre-answers all of them, so the engagement does not stall in legal or risk review.

- Who owns this AI workflow on the client side, and who owns it on the Dealix side?
- Who approved this specific recommendation or action?
- What data did the model access? Was any PII or commercial sensitive data exposed?
- Is there a rollback or mitigation path if this action turns out to be wrong?
- Where is the audit trail? Can we replay this run?
- What is the AI cost per workflow, per client, per month?
- What is the proof of value — what changed in the business because of Dealix?

## How this layer plugs into the rest of Dealix
Layer 5 is the governance overlay across all other operating layers. It binds:

- The capability and offer layers (Layers 1–3) to actual approved, owned, monitored workflows.
- The observability stack (`docs/AI_OBSERVABILITY_AND_EVALS.md`) to a governance-grade audit trail.
- The legal and trust stack (`docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`, `docs/legal/COMPLIANCE_CERTIFICATIONS.md`) to operational controls.
- The cost stack (`docs/V7_COST_CONTROL_POLICY.md`) to AI FinOps reporting per client.

The detailed sub-documents (Agent Governance Council, Autonomy Validation Gates, AI Action Control, Reversibility & Rollback, Permission Mirroring, AI Run Provenance, Enterprise AI Report Card, Governance Product Ladder, Internal Controls, Board Pack) each expand one slice of this layer.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Client risk requirements, regulatory constraints (PDPL, sector rules) | Governance design per engagement | Governance Lead + Delivery Owner | Per engagement |
| Agent inventory, autonomy classifications | Approved agent catalogue per workspace | AI Agent Governance Council | Weekly active / Monthly review |
| AI run logs, eval results, incidents | Enterprise AI Report Card | Governance + Delivery | Monthly |
| Client policies, approval matrix | Runtime governance configuration | Governance Reviewer | Per release |

## Metrics
- Governance Readiness Score — % of seven domains answered, evidenced, and signed off per enterprise engagement.
- Time-to-Procurement-Approval — days from first commercial conversation to signed MSA + DPA.
- Governed Workflow Coverage — % of client AI workflows running with full provenance and approval workflow.
- Incident-Free Months — count of months with zero governance incidents per enterprise client.
- Proof-of-Value Density — number of evidenced value events per active enterprise workspace per quarter.

## Related
- `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md` — buyer-facing trust and compliance pack
- `docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md` — Arabic enterprise trust pack
- `docs/legal/COMPLIANCE_CERTIFICATIONS.md` — certifications roadmap supporting this layer
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating constitution this layer enforces
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
