# Dealix Full Company Team + Communication Plane

## Objective
Run Dealix as an AI-native operating company with a complete internal agent team, a founder command channel, customer-facing communication channels, governed negotiation, proof, and learning.

## Non-negotiable architecture
- Dealix Company Brain / Company Intelligence = canonical context.
- Opportunity Graph = canonical commercial opportunity state.
- Strategy Execution / Action Queue = canonical action state.
- Approval Center = canonical gate for external/sensitive actions.
- Proof Ledger / Proof Packs = canonical evidence.
- Learning / Self-Improvement = canonical learning state.
- Company Autopilot = deterministic scheduler and safe internal executor.
- Hermes = internal specialist agent runtime.
- OpenClaw = founder-facing conversational gateway.
- n8n = deterministic connector/workflow runtime, not a second business database.
- Railway = Production Core.
- Hostinger VPS = Command & AI Node.
- GitHub = code/source-of-truth history.

## Channel ownership
### Telegram — Founder Command Center
Owner: OpenClaw.
Purpose:
- Daily Command.
- urgent production/security incidents.
- approval cards.
- money-now opportunity alerts.
- executive summaries.
- founder deep-work requests.

Telegram must not be a customer-facing sales bot by default.

### WhatsApp — Customer Business Operations
Preferred production design:
Dedicated WhatsApp Business number -> Meta WhatsApp Business Cloud -> n8n -> Dealix.

Uses:
- inbound lead qualification.
- customer support.
- approved sales replies.
- approved negotiation responses.
- booking links and scheduling handoff.
- proposal/document handoff.
- delivery/status updates.
- customer success/value follow-ups.

Personal WhatsApp should not be the primary autonomous commercial sender. OpenClaw WhatsApp Web may be used only as a controlled internal/test lane if explicitly enabled.

### Email — Formal Commercial Lane
Uses:
- proposals.
- formal follow-ups.
- attachments.
- contracts and commercial documents.
- meeting recaps.
- customer onboarding packs.

Email remains draft/approval-first unless a specific send is approved.

## Full agent team
### 1. CEO Chair / Chief Operating Conductor
Runtime: SprintOrchestratorAgent + Agent Council CEO synthesis.
Responsibilities:
- prioritize whole-company work.
- resolve cross-functional conflicts.
- choose highest-value next action.
- escalate only decisions requiring founder authority.

### 2. Chief Context Officer
Runtime: CompanyBrainAgent.
Responsibilities:
- maintain evidence-backed company context.
- offers, constraints, personas, proof and client history.
- block stale/invented assumptions.

### 3. Revenue Intelligence Lead
Runtime: RevenueIntelligenceAgent.
Responsibilities:
- money-now opportunities.
- pipeline risk.
- stale deals.
- closeability.
- revenue proof gaps.

### 4. Sales Strategy Lead
Runtime: SalesIntelligenceAgent.
Responsibilities:
- discovery briefs.
- negotiation options.
- objection handling.
- follow-up drafts.
- proposal strategy.

### 5. Customer Acquisition Lead
Runtime: CustomerAcquisitionAgent.
Responsibilities:
- acquisition experiments.
- channel plans.
- lead-to-opportunity transitions.
- approval-ready outbound plans.

### 6. Market Intelligence Lead
Runtime: MarketIntelAgent.
Responsibilities:
- Saudi/GCC signals.
- sectors, accounts, tenders, partners and competitors.
- source-backed opportunities.

### 7. Account Qualification Lead
Runtime: LeadIntelligenceAgent.
Responsibilities:
- ICP fit.
- evidence quality.
- buying trigger.
- decision-maker hypotheses.
- next best action.

### 8. Diagnostic & Value Discovery Lead
Runtime: DiagnosticAgent.
Responsibilities:
- diagnose operational/commercial problems.
- quantify value hypotheses.
- build pilot hypotheses and diagnostic packs.

### 9. Operations & Delivery Lead
Runtime: ManagedOpsAgent.
Responsibilities:
- delivery readiness.
- customer onboarding.
- blockers/deadlines/capacity.
- support/customer-success escalation.

### 10. Data & Intelligence Architect
Runtime: DataArchitectAgent.
Responsibilities:
- entity resolution.
- source lineage.
- data quality.
- normalization and evidence packs.

### 11. Chief Risk & Governance Officer
Runtime: GovernanceAgent.
Responsibilities:
- approval rules.
- privacy/compliance.
- commercial claim safety.
- proof requirements.
- external-action blocking.

## Operating loop
Inbound signal/message/form/email
-> identify person/company
-> load Company Brain context
-> update/create Opportunity Graph state
-> route to specialist agent
-> research/analyze/score
-> prepare response/negotiation/delivery action
-> risk/claim check
-> Approval Center when external/sensitive
-> approved execution through n8n/connector
-> delivery/read/reply capture
-> Proof Ledger
-> Learning / Self-Improvement
-> next action

## Negotiation system
Agents may autonomously:
- research counterparty.
- classify negotiation stage.
- calculate options.
- build BATNA/walk-away recommendations.
- draft counteroffers.
- compare price/scope/timeline tradeoffs.
- identify objections and concessions.
- prepare an exact recommended response.

Agents must not autonomously:
- send a price/discount/counteroffer.
- commit scope/timeline/SLA.
- accept terms.
- sign contracts.
- charge/refund/pay.
- make legal commitments.

Every negotiation approval card must contain:
- counterparty.
- opportunity id.
- current stage.
- requested terms.
- proposed response.
- price/discount/scope/timeline delta.
- floor/walk-away guard.
- evidence/rationale.
- risk.
- expiry.
- decision: APPROVE / EDIT / REJECT.

## WhatsApp workflow set
1. WA_01_Inbound_Triage
2. WA_02_Identity_Entity_Resolution
3. WA_03_Lead_Qualification
4. WA_04_Sales_Reply_Draft
5. WA_05_Negotiation_Analysis
6. WA_06_Approval_Card
7. WA_07_Approved_Send
8. WA_08_Delivery_Read_Reply_Proof
9. WA_09_Customer_Support
10. WA_10_Booking_Handoff
11. WA_11_Proposal_Handoff
12. WA_12_Suppression_Consent
13. WA_13_Customer_Success
14. WA_14_Expansion_Signals

Every n8n workflow must define:
- trigger.
- owner.
- canonical entity ids.
- inputs/outputs.
- idempotency key.
- retry and timeout.
- approval requirement.
- evidence/proof path.
- failure/dead-letter path.
- suppression/consent behavior when applicable.

## Founder interaction model
Founder should normally receive only:
1. Morning Daily Command.
2. Critical Production/Security incident.
3. Money-now opportunity.
4. Exact Approval Cards.
5. Major customer/churn/delivery risk.
6. Weekly Proof/Revenue report.

Everything else should be handled internally by agents, workflows, and existing Dealix operating systems.

## Autonomy policy
- L0 Observe: automatic.
- L1 Analyze: automatic.
- L2 Draft: automatic.
- L3 Internal Execute: automatic.
- L4 Repo Execute: isolated branch/worktree, tests, Draft PR only.
- L5 External/Sensitive: exact founder approval immediately before execution.

## Preferred implementation order
1. Prove first Agent Council Daily Command + PROOF.json.
2. Make Telegram founder route healthy and paired.
3. Build Engineering L4 worktree -> tests -> Draft PR.
4. Provision dedicated WhatsApp Business number / Meta app credentials.
5. Implement WhatsApp inbound -> Dealix entity/opportunity update.
6. Implement sales/negotiation draft -> Approval Center.
7. Implement approved send -> delivery/reply Proof Ledger.
8. Implement support/booking/proposal/customer-success workflows.
9. Add Gmail formal-commercial lane.
10. Add weekly executive proof/revenue/customer-value review.

## Success state
Dealix is operational when the founder can mostly manage the company through Telegram approval/command cards while the internal agents continuously research, prioritize, prepare, execute safe internal work, update canonical Dealix state, and prove results; customer-facing WhatsApp/email actions are executed only after exact approval unless policy is explicitly changed for a narrowly scoped, low-risk use case.