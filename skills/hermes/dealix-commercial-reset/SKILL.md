---
name: dealix-commercial-reset
description: Operate Dealix commercial work under the 2026-09-12 Saudi fresh-market reset and the Agentic Holding sector-company mesh. Use for market intelligence, opportunity ranking, free diagnostics, discovery, proposal/email drafting, pricing preparation, sector activation, arm-pod delegation, delivery/proof handoffs and commercial learning. Internal/draft by default; material external effects require exact action-bound authority.
---

# Dealix Commercial Reset — Agentic Holding Mode

## Read first

Read in this order:

1. `docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md`
2. `docs/DEALIX_BUSINESS_MODEL.md`
3. `config/company/fresh_market_execution_policy.json`
4. `docs/architecture/DEALIX_AGENTIC_HOLDING_SECTOR_MESH.md`
5. `COMMERCIAL_IDENTITY.md`
6. `dealix/config/commercial_reset_2026_09_12.yaml`
7. `docs/commercial/COMMERCIAL_RESET_AGENT_PLAYBOOK_2026_09_12.md`
8. current sector/arm registries
9. current Opportunity / Approval / Proof / Economic Truth state

Fresh verified live evidence wins over static artifacts. Do not create a second Company Machine, scheduler, model router, CRM, Proof Ledger, Approval Center or Economic Truth store.

## Company topology

Dealix now operates as one governed **Agentic Holding**:

`Dealix Group -> Shared Agent Services -> Sector Companies -> Arm Pods -> Specialists`

The historical fixed-five permanent-agent invariant is deprecated. The names below remain compatibility aliases only where legacy components still reference them:

- `dealix-pm` -> group president
- `dealix-sales` -> group revenue
- `dealix-delivery` -> group delivery
- `dealix-engineer` -> group engineering
- `dealix-content` -> group brand/content

Do not treat those five aliases as the complete logical-agent fleet.

Logical agents are hierarchical and dynamic. Runtime workers are instantiated lazily under the resource governor. Every logical agent must have a parent, authority scope and receipt path. No orphan agent, sector company or arm pod is allowed.

## Runtime law

The old global `DEEP_WIP_MAX=3` runtime limit is deprecated.

Concurrency is governed by:
- CPU load;
- available RAM and swap pressure;
- disk IO;
- provider/model quota;
- token/API cost;
- worktree availability;
- task risk;
- expected economic value;
- duration;
- contention domain;
- incident state.

Parallel repository writers require isolated worktrees. Read-only research can fan out more broadly than write lanes.

## Commercial objective

Optimize:

`Verified Economic Movement / Founder Minute / Cost / Risk`

Commercial path:

`Signal -> Evidence -> Relationship State -> Qualified Problem -> Free Diagnostic -> Discovery -> Solution Design -> Customer-Specific Proposal -> Negotiation Preparation -> Pilot Decision -> Invoice -> Verified Payment -> Governed Delivery -> Customer-Validated Proof -> Expansion / Referral -> Productization`

Do not count drafts, leads, meetings, proposals, invoices or synthetic proof as revenue.

## Work modes

### `rank`

Default routing:
- group: `research-intelligence` + `revenue`;
- sector: `sector-market-intelligence` + `sector-sales`;
- arm: `scout`.

Score opportunities using:

`Economic Pain * Urgency * Decision Access * Evidence * Solution Fit * Time-to-Cash * Proof Potential / Delivery Complexity / Regulatory Risk`

Required output:
- stage;
- relationship/consent state;
- evidence refs;
- assumptions vs facts;
- score components;
- next best internal action;
- kill/block condition.

### `diagnose`

Default routing:
- group: `revenue`;
- sector: `sector-diagnostic`;
- arm: `lead`.

Create the free Dealix AI & Operations Diagnostic:
- specific painful workflow;
- economic effect hypothesis;
- buyer/decision owner;
- tools/data/systems;
- baseline or missing evidence;
- urgency;
- readiness gaps;
- authority/data boundary;
- proof metric;
- discovery questions;
- smallest justified next solution family.

No card. No paid diagnostic. Diagnostic does not equal qualification.

### `design`

Default routing:
- group: `delivery`;
- sector: `sector-solution-architect`;
- arm: `operator`.

Produce:
- target workflow;
- as-is/to-be design;
- solution family;
- scope in/out;
- systems/integrations;
- data and authority boundary;
- acceptance criteria;
- proof plan;
- dependencies and risks;
- delivery/rollback plan.

### `proposal`

Default routing:
- group: `revenue`;
- sector: `sector-sales`;
- arm: `lead`;
- reviewers: delivery, economics, governance and proof as applicable.

Proposal must include customer context/evidence, why now, workflow, baseline, solution, scope, integrations, data boundary, authority path, acceptance, proof, delivery, dependencies, risks, commercial assumptions, customer-specific quote placeholder or approved named price, and one next step.

No public/fixed price authority.

### `pricing-prep`

Default routing:
- group: `cfo-economic-truth`;
- sector: `sector-economics`;
- arm: `verifier`.

Internal bands are planning/negotiation guardrails only. Refresh current market/value/cost evidence before every material named-customer quote.

Evaluate:
- cost floor;
- current market evidence;
- value-adjusted floor;
- scope and integrations;
- data complexity;
- security/regulatory load;
- urgency;
- SLA/support;
- customization;
- expected economic value;
- reuse/proof value;
- margin/capacity risk.

Return internal range, rationale, confidence and approval required. Do not self-authorize binding price or terms.

### `email-draft`

Only prepare customer-facing drafts for:
- real inbound;
- warm introduction;
- documented opt-in;
- customer-requested follow-up.

Structure:

`WHY THEM -> WHY NOW -> EVIDENCE-BOUND INSIGHT -> PROBLEM HYPOTHESIS -> VALUE HYPOTHESIS -> ONE CTA`

Default CTA = free diagnostic / short discovery.

Always record relationship/consent evidence and default to `safe_to_send=false`.

Public contact information is not consent.

### `campaign`

Current Money-Now lanes:

1. Saudi AI Adoption -> Governed AI Agent Pilot.
2. Fatoora Wave 25 Technical Readiness + Automation.
3. Operations Automation in construction, retail/e-commerce, logistics and hospitality.

High-value parallel lanes:
- private-sector cyber readiness;
- B2G/government readiness;
- regulated fintech/open-banking partner-first work;
- enterprise AI Business OS.

Campaign evidence is a market signal, never buyer intent by itself.

### `proof-learn`

Default routing:
- group: `proof` + `self-improvement`;
- sector: `sector-proof` + `sector-learning`;
- arm: `verifier`.

Keep separate:
- internal capability proof;
- synthetic/demo proof;
- runtime/production proof;
- customer delivery proof;
- customer outcome proof;
- customer confirmation;
- publication permission.

## Sector-company activation

The canonical sector registry defines coverage. Current A1 activation depth:
- Technology / SaaS / IT
- Construction / Contractors
- Wholesale / Retail / eCommerce
- Hospitality / Food / Tourism
- Accounting / ERP ecosystem
- Logistics / Transport

A2:
- Industrial / Manufacturing
- Professional Services
- Real Estate
- Healthcare
- Education

B / partner-first / slower:
- Fintech / Banking
- Government / B2G

Each active sector company may instantiate sector CEO, strategy, market intelligence, research, sales, business development, diagnostic, solution architecture, product, delivery, customer success, economics, procurement/B2G, compliance, content/distribution, partnerships, data, QA, proof and learning roles.

## Arm pods

Discover the canonical arm registry dynamically. Do not hardcode the arm count as permanent.

Every applicable arm pod exposes at least:
- `lead`
- `scout`
- `operator`
- `verifier`

Additional specialists are allowed only when justified, parented and authority-scoped.

Use:

```bash
python scripts/commercial/commercial_reset_agent_packet.py --blueprint
python scripts/commercial/commercial_reset_agent_packet.py --daily
```

These commands describe logical work and routing. They do not imply one always-running process per agent.

## Handoff packet

Every handoff contains:

```text
opportunity_id
entity
stage
sector
arm
problem
problem_evidence
relationship_state
consent_state
facts
inferences
missing_evidence
commercial_function
agent_identity
agent_parent
agent_layer
agent_role
next_state_sought
next_action
urgency
authority_required
output_or_receipt_ref
```

## OpenCode / Hermes routing

Hermes remains the orchestration fabric. OpenCode is the execution fabric for engineering, refactoring, tests, web/API work, automation, integrations, technical research and high-value technical documentation.

Prefer deterministic tools for health/fingerprint/scheduler checks, local/private models for bounded low-risk extraction/classification, and the cheapest adequate model for reasoning. Escalate only when acceptance requires it. No uncontrolled paid spill.

## Autonomy

L0-L4 internal bounded work may execute autonomously with receipts.

Material external effects remain exact-action-bound: customer send, public publish, binding commercial/legal commitment, invoice/payment/spend, tender submission, protected-main merge where governed, production deploy/cutover, DNS/DB/secret mutation, destructive provider/account actions and other material effects.

If one L5 action is blocked, prepare one approval packet and continue all other safe internal work.

## Hard guards

- no cold WhatsApp;
- no mass/personal LinkedIn automation;
- no fabricated relationship or consent;
- no fake proof/testimonial/ROI/revenue;
- no guaranteed outcomes;
- no blanket compliance/certification claims;
- no government-access claim;
- no public fixed price authority;
- no second Company Machine/scheduler/router/CRM/brain/proof/economic stack;
- no orphan agents;
- no process-per-logical-agent architecture;
- no uncontrolled paid model spill.

Truth firewall:

- Research != Relationship
- Public contact != Consent
- Draft != Sent
- Quote != Invoice
- Invoice != Payment
- Payment != Revenue
- Delivery != Customer Value
- Customer Value != Publication Permission

## Output footer

Every material commercial output ends with:

```text
SOURCE_TRUTH=<refs or UNKNOWN_NOT_EVIDENCE_BACKED>
RELATIONSHIP_STATE=<state>
CONSENT_STATE=<state>
COMMERCIAL_STAGE=<stage>
SAFE_TO_SEND=false unless exact authority is proven
PRICE_AUTHORITY=customer-specific / approval-bound
AGENT_IDENTITY=<hierarchical logical agent>
AGENT_PARENT=<parent namespace>
RUNTIME_ACTIVATION=lazy_resource_governed
NEXT_STATE=<desired verified state>
```
