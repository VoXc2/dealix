# DEALIX Ω∞ — Agentic Holding + Sector Company Mesh

Status: **ADOPTED ARCHITECTURE CANDIDATE**  
Date: 2026-09-12  
Mode: continuation from live Dealix state; not a greenfield rebuild.

## 1. North Star

`CASH_READY_AUTONOMOUS_DEALIX_COMPANY`

Optimize for maximum verified business value per unit of time, capital, risk, compute, token cost, and founder attention.

## 2. New Company Model

Dealix evolves from a small fixed permanent-agent team into a governed **Agentic Holding / Group**.

```text
DEALIX GROUP / HOLDING
│
├── Group Executive Agent Council
├── Shared Agent Services
│   ├── Finance / Economic Truth
│   ├── Security / Risk / Governance
│   ├── AI / Model Routing
│   ├── Research / Intelligence
│   ├── Software Evolution
│   ├── Communications
│   ├── Procurement / B2G
│   ├── Proof / QA
│   └── Learning / Self-Improvement
│
└── Sector Companies [dynamic]
    │
    ├── Sector Executive Team
    ├── Sector Commercial Team
    ├── Sector Research Team
    ├── Sector Delivery Team
    ├── Sector Finance Team
    ├── Sector Compliance Team
    │
    └── Arm Pods [dynamic]
        ├── Lead Agent
        ├── Scout / Research Agent
        ├── Operator / Builder Agent
        ├── Verifier / Proof Agent
        └── Additional Specialists when justified
```

Every sector is treated as a **virtual specialist company under Dealix**. Every canonical arm becomes one or more **Agent Pods** within applicable sector companies.

No sector company owns a separate Company Brain, CRM, Economic Truth system, Approval Center, scheduler, model router, financial ledger, or infrastructure stack. Dealix Group remains the single authority and source of truth.

## 3. Hierarchy

### 3.1 Group Layer

Logical group-level specialist identities may include:

- Group President / CEO Agent
- Group Strategy & Capital Allocation Agent
- Group COO Agent
- Group CTO / Engineering Agent
- Group Chief AI & Automation Agent
- Group CFO / Economic Truth Agent
- Group CRO / Revenue Agent
- Group CMO / Growth Agent
- Group Chief Delivery Agent
- Group Customer Success Agent
- Group Research & Intelligence Agent
- Group Product Agent
- Group Data & Analytics Agent
- Group Security Agent
- Group Risk Agent
- Group Governance / Compliance Agent
- Group Procurement / B2G Agent
- Group Partnerships Agent
- Group Talent / Workforce Agent
- Group Brand / Content Agent
- Group QA / Verification Agent
- Group Proof Agent
- Group Self-Improvement Agent

These are **logical company roles**, not permanently-running LLM processes.

### 3.2 Sector Company Layer

For every sector discovered in the canonical sector registry, Dealix creates or reconciles a `dealix.<sector>` company namespace.

Each active sector company should be able to instantiate specialist roles such as:

- sector-ceo
- sector-strategy
- sector-market-intelligence
- sector-research
- sector-sales
- sector-business-development
- sector-diagnostic
- sector-solution-architect
- sector-product
- sector-delivery
- sector-customer-success
- sector-economics
- sector-procurement
- sector-b2g
- sector-compliance
- sector-content
- sector-distribution
- sector-partnerships
- sector-data
- sector-qa
- sector-proof
- sector-learning

The sector company owns a **scoped view** of its market, buyers, problems, triggers, competitors, regulations, procurement routes, opportunities, diagnostics, offers, delivery playbooks, proof, reusable IP and productization candidates.

### 3.3 Arm Pod Layer

Discover the canonical arm registry dynamically. Do not assume the current arm count is permanent.

For every relevant arm in every applicable sector company, create an Arm Pod with at least:

- `dealix.<sector>.<arm>.lead`
- `dealix.<sector>.<arm>.scout`
- `dealix.<sector>.<arm>.operator`
- `dealix.<sector>.<arm>.verifier`

Additional specialist identities may include analyst, architect, engineer, automation-builder, negotiator, procurement specialist, finance specialist, compliance specialist, content specialist, customer-success specialist, reviewer and red-team roles.

Every arm and agent must have an owner, parent, authority scope and evidence trail. No orphan sector, arm or agent is allowed.

## 4. Logical Agents vs Runtime Workers

The system may define hundreds or thousands of logical agent identities. This is intentional.

**Logical agent count is not runtime concurrency.**

Maintain separate concepts:

- `LOGICAL_AGENT_REGISTRY`
- `ACTIVE_RUNTIME_WORKERS`

Do not launch a process per logical agent. Instantiate workers lazily when work exists.

## 5. Migration of Legacy Invariants

The historical invariant `exactly five permanent agents` is deprecated by this architecture and must be migrated deliberately, not silently bypassed.

The historical global `DEEP_WIP_MAX=3` must also be migrated from a company-wide fixed worker count to a resource-aware concurrency policy.

### New invariant direction

1. All agents belong to one canonical hierarchical Agent Registry.
2. Every agent has one authority scope and one parent.
3. Every active sector has one Sector Company.
4. Every canonical arm has one or more owned Agent Pods.
5. No orphan agent / arm / sector company.
6. Runtime concurrency is resource-governed.
7. Parallel repository writers use isolated Git worktrees.
8. Economic Truth remains fail-closed.
9. Material external actions require the applicable authority.
10. Production Green requires exact release parity.
11. No cold WhatsApp mass automation.
12. Local/private model endpoints remain private.

Existing Economic Truth, external-authority, WhatsApp, local-LLM privacy and release-parity invariants remain valid and must be preserved.

## 6. Resource-Aware Concurrency Governor

Replace the old global WIP assumption with a `RESOURCE_AWARE_CONCURRENCY_GOVERNOR`.

Inputs should include:

- CPU load
- available RAM
- disk space / IO
- provider quota
- model quota
- token / API cost
- worktree availability
- task risk
- expected economic value
- duration
- contention domain
- incident state

Suggested budgets:

- `GROUP_RUNTIME_BUDGET`
- `SECTOR_RUNTIME_BUDGET`
- `ARM_RUNTIME_BUDGET`
- `MODEL_RUNTIME_BUDGET`
- `REPO_WRITER_BUDGET`

Read-only research and analysis can run more broadly than repository writers. Every parallel writer must use an isolated Git worktree.

## 7. Canonical Components

Prefer evolving existing components instead of creating parallel stacks.

Target capabilities:

- AgentRegistry
- AgentHierarchyGraph
- SectorCompanyRegistry
- SectorCompanyFactory
- ArmAgentRegistry
- ArmPodFactory
- AgentCapabilityGraph
- AgentAuthorityGraph
- AgentDispatcher
- ResourceGovernor
- AgentPerformanceLedger
- AgentLearningLedger
- AgentLifecycleManager
- AgentModelRouter
- AgentWorktreeManager
- AgentReceiptLedger

## 8. Hermes

Hermes remains the canonical orchestration fabric.

Use Hermes delegation, Skills, MCP, cron, deterministic scripts and background jobs. Do not create one cron job per logical agent. Use bounded dispatcher jobs that pull from canonical queues.

Suggested cadence:

- **Fast loop:** queue reconciliation, worker health, lease recovery, event dispatch.
- **Hourly:** sector radar, opportunity ranking, arm activation, relationship-state review.
- **Daily:** Group President economic ordering, sector economic review, delivery/proof review, model-cost review, content/distribution planning.
- **Nightly:** code quality, security, software evolution, learning consolidation, performance scoring.
- **Weekly:** sector portfolio review, agent promotion/demotion, capability gaps, productization, partnerships, keep/kill/scale decisions.

Use the existing Hermes scheduler. Do not create a second scheduler.

## 9. OpenCode

OpenCode is the engineering execution fabric for coding, refactoring, tests, web/API development, automation, integrations, data pipelines, security fixes, technical docs and infrastructure-as-code preparation.

When operationally useful, prefer a persistent headless OpenCode server and attach jobs to it rather than repeatedly cold-starting the entire tool stack.

All parallel code-writing lanes require isolated worktrees.

## 10. Model Portfolio

Do not permanently hardcode one model.

Route by class:

- Cheap/local: deterministic operations, extraction, classification, repetitive transforms.
- High-throughput: repo analysis, coding loops, broad research synthesis.
- Deep reasoning: architecture, difficult debugging, strategic/commercial analysis, security review.
- Reviewer: independent validation, adversarial review, proof checking.

Optimize verified value / cost / latency / reliability. No uncontrolled automatic paid spill.

## 11. Internet and Market Intelligence

Every Sector Company continuously learns from the internet with an official-source-first hierarchy:

1. Saudi government/regulator sources.
2. Official company/vendor sources.
3. Procurement/tender portals.
4. Official documentation.
5. Primary research.
6. Trusted news.
7. Supplementary community evidence.

Retain provenance: URL, retrieval date, source class, sector, buyer, signal, confidence, evidence scope and next action.

Research is not relationship, consent, pipeline, customer proof, payment or revenue.

## 12. Commercial Closed Loop

Every Sector Company should be able to operate:

`Signal -> Account Intelligence -> Relationship State -> Problem Hypothesis -> Free Diagnostic -> Discovery -> Solution Design -> Customer-Specific Proposal -> Negotiation Preparation -> Pilot -> Payment Verification -> Delivery -> Acceptance -> Proof -> Expansion -> Referral -> Productization`

Agents may autonomously research, score, enrich, prepare diagnostics/proposals/negotiation options, draft communications, prepare meetings/deliverables, analyze conversations and update internal state.

Material external actions remain authority-gated.

## 13. Communications

Specialists may support Gmail, WhatsApp, Telegram, Slack, website inbound, forms, meetings, support, partnerships and procurement.

Internal agent-to-agent communication is autonomous. External communications must obey relationship state, consent, channel policy, sender identity, opt-out and authority rules.

No cold WhatsApp mass automation.

## 14. Website

`dealix.me` is the digital front door for the entire holding structure.

The site should eventually represent Dealix Group, sectors, sector companies, capabilities, arms, diagnostics, solutions, proof, resources and inbound journeys without generating thin SEO spam.

Every public page requires real usefulness, truthful claims, a clear buyer/problem/CTA, evidence where required, Arabic/English quality, SEO, accessibility, performance and mobile acceptance.

Diagnostics remain free/card-free unless a newer explicit commercial policy supersedes that rule.

## 15. Delivery Mesh

Each qualified opportunity may instantiate:

- Delivery Lead Agent
- Solution Agent
- Implementation Agent
- QA Agent
- Customer Success Agent
- Proof Agent

Delivery completion is not automatically customer value. Customer value requires evidence-backed acceptance.

## 16. Economic Truth

Preserve and strengthen the existing Economic Truth system.

Never allow:

- research -> revenue
- proposal -> revenue
- invoice -> revenue
- payment request -> verified payment
- synthetic test -> customer proof

Track real evidence such as verified payment, recognized revenue, gross margin, collection probability, delivery effort, founder minutes, automation leverage, reuse value, retention, expansion and risk.

## 17. Agent Performance and Lifecycle

Every agent template and active instance should produce receipts.

Track task success, verifier acceptance, economic value, time, token/API cost, failures, retries, evidence violations, human intervention and reusable assets.

Use evidence to:

- PROMOTE
- KEEP
- SPECIALIZE
- IMPROVE
- DEMOTE
- SUSPEND
- KILL

Agents may improve prompts, skills, tests, routing, context, memory structure, retrieval, playbooks, heuristics, model selection and tool selection when changes are versioned, tested, reviewable and rollback-capable.

No agent may grant itself additional external authority.

## 18. Software Acquisition

Reuse the existing Software Acquisition & Evolution Factory. Internet-discovered tools must pass provenance, license, CVE/KEV, capability, sandbox, rollback, duplication and economic-benefit gates.

No blind host installation.

## 19. Authority

Autonomous internal authority:

- L0 Observe
- L1 Analyze
- L2 Draft
- L3 Internal Execute
- L4 Repository Execute

Material external effects remain exact-action gated, including protected-main merge, production cutover/deploy, DNS, production DB/schema mutation, secrets/keys, firewall/root infrastructure mutation, payment/spend, contract acceptance, tender submission, live customer send and public publishing.

If one material action is blocked, prepare one bounded approval packet and continue all other safe work.

## 20. Migration Strategy

Do not perform a destructive big-bang rewrite.

1. Audit current architecture.
2. Introduce hierarchical registries and compatibility adapters.
3. Migrate agents, sectors and arms.
4. Migrate scheduler/resource model.
5. Migrate legacy invariants/tests.
6. Activate sector-company dispatch.
7. Run acceptance and independent review.

Legacy interfaces may temporarily remain as compatibility facades, but there must be one canonical new truth underneath.

## 21. Required Acceptance

Acceptance should prove:

- old exactly-five constraint is removed safely;
- arbitrary specialist-agent count works;
- every sector generates a Sector Company;
- every canonical arm gets owned Agent Pods;
- every agent has a parent and authority scope;
- no orphan agent exists;
- resource budgets work;
- sector/arm isolation works;
- worktree isolation works;
- Economic Truth remains intact;
- payment != revenue;
- material external authority remains gated;
- production parity remains fail-closed;
- no cold WhatsApp mass automation;
- no duplicate Company Brain/scheduler/Economic Truth store;
- no uncontrolled paid model spill.

## 22. Execution Receipt

Future implementation runs should emit at least:

```text
DEALIX_AGENTIC_HOLDING_RECEIPT
BASE_SHA=
HEAD_SHA=
BRANCH=
SECTORS_DISCOVERED=
SECTOR_COMPANIES_CREATED=
ARMS_DISCOVERED=
ARM_PODS_CREATED=
GROUP_AGENT_TEMPLATES=
SECTOR_AGENT_TEMPLATES=
ARM_AGENT_TEMPLATES=
TOTAL_LOGICAL_AGENTS=
MAX_SIMULTANEOUS_RUNTIME_AGENTS=
RESOURCE_GOVERNOR_STATUS=
LEGACY_FIVE_AGENT_INVARIANT=
LEGACY_DEEP_WIP_3_INVARIANT=
AGENT_HIERARCHY_TESTS=
ECONOMIC_TRUTH_TESTS=
AUTHORITY_TESTS=
WORKTREE_TESTS=
FULL_RELEVANT_ACCEPTANCE=
HERMES_STATUS=
OPENCODE_STATUS=
MODEL_ROUTER_STATUS=
DRAFT_PR=
L5_EXECUTED=NONE
TOP_10_NEXT_ECONOMIC_ACTIONS=
BLOCKERS=
APPROVAL_QUEUE=
```

## 23. Non-negotiable Truth Firewall

Research != relationship.  
Public contact != consent.  
Signal != qualified problem.  
Engagement != buyer intent.  
Draft != sent.  
Quote != invoice.  
Invoice != payment.  
Payment request != verified cash.  
Synthetic/demo != customer proof.  
HTTP 200 != release identity.  
Merged PR != deployed release.  
Historical PASS != current exact-head PASS.  
Model output != authority.
