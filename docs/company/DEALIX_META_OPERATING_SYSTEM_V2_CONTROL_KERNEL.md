# DEALIX Ω∞ — META-OPERATING SYSTEM V2 — CONTROL KERNEL

Effective: 2026-09-11

Status: **Canonical constitutional superlayer.**

Machine-readable authority: `config/company/dealix_control_kernel_v2.json`.

Fail-closed verifier: `scripts/commercial/verify_dealix_control_kernel_v2.py`.

Runtime primitives: `scripts/commercial/dealix_control_kernel_v2.py`.

This section **overrides conflicting lower-level operating logic**. It does **not** replace the existing Dealix Constitution. It strengthens decision quality, economic allocation, agent identity, execution safety, learning, scalability, and enterprise readiness.

## LXXI. Decision Quality Kernel

Dealix must distinguish `DATA / EVIDENCE / BELIEF / PREDICTION / DECISION / ACTION / RESULT`.

A prediction is never stored as fact. An inference is never stored as customer evidence. Material decisions should carry `decision_id`, `decision`, `decision_owner`, `evidence`, `assumptions`, `confidence`, `expected_result`, `expected_value`, `downside`, `reversibility`, `decision_deadline`, `prediction`, `actual_result`, and `calibration_error`.

Goal: **MAKE BETTER DECISIONS FASTER.**

## LXXII. Confidence-Aware Economic Dispatcher

Normalize inputs to `0.00 → 1.00`.

`VALUE_VECTOR = 0.30*CASH_IMPACT + 0.20*CUSTOMER_VALUE + 0.15*PROOF_VALUE + 0.15*CONSTRAINT_RELIEF + 0.10*FOUNDER_TIME_SAVED + 0.10*STRATEGIC_REUSE`.

`EXECUTION_DRAG = 0.25*TIME_COST + 0.20*CASH_COST + 0.20*FAILURE_RISK + 0.15*IRREVERSIBILITY + 0.10*COMPLEXITY_COST + 0.10*MAINTENANCE_COST`.

`CONFIDENCE_FACTOR = EVIDENCE_CONFIDENCE * DATA_FRESHNESS`.

`FINAL_PRIORITY = VALUE_VECTOR * CONFIDENCE_FACTOR * CONSTRAINT_FIT * URGENCY_FACTOR / MAX(0.20, EXECUTION_DRAG)`.

The score is a decision aid, not objective truth. If two candidates are within 10%, prefer higher reversibility, faster feedback, higher customer learning, lower founder attention, and stronger proof potential.

## LXXIII. Value of Information

Before expensive, risky, or irreversible actions, calculate `VOI = EXPECTED_DECISION_LOSS_AVOIDED / INFORMATION_COST`. If VOI exceeds immediate execution advantage, research/test first. Research must not become procrastination.

## LXXIV. Reversibility Classification

- `R0` — READ ONLY
- `R1` — INSTANTLY REVERSIBLE
- `R2` — REVERSIBLE WITH SMALL COST
- `R3` — REVERSIBLE WITH MATERIAL COST
- `R4` — DIFFICULT TO REVERSE
- `R5` — EFFECTIVELY IRREVERSIBLE

Autonomy increases with reversibility. Evidence requirements increase with irreversibility. High uncertainty + R4/R5 defaults HOLD. High confidence + R0/R1 defaults EXECUTE.

## LXXV. Business State Machines

Opportunity state:

`RESEARCH_ONLY → KNOWN → INTERACTION → QUALIFIED_PROBLEM → DIAGNOSTIC → DISCOVERY → QUOTE_READY → QUOTED → PAYMENT_PENDING → PAID → DELIVERY → PROOF → EXPANSION`.

Every transition requires `from_state`, `to_state`, `required_evidence`, `authority`, `side_effect`, and `receipt`. Illegal transitions return `INVALID_STATE_TRANSITION`.

## LXXVI. Production State Machine

`SOURCE_ACCEPTED → BUILD_ACCEPTED → RELEASE_CANDIDATE → DEPLOYED → HEALTHY → RELEASE_PARITY_PROVEN → BUSINESS_FLOW_PROVEN → PRODUCTION_GREEN`.

Rollback may move production to `DEGRADED` or `ROLLBACK_ACTIVE`. A previous green release never makes a new release green.

## LXXVII. Financial State Machine

`OPPORTUNITY_VALUE → QUOTE → ACCEPTED_COMMERCIAL_TERMS → INVOICE → PAYMENT_REQUESTED → PAYMENT_PENDING → PAYMENT_VERIFIED → CASH_AVAILABLE → REVENUE_RECOGNITION_STATE`.

No automatic promotion. Every promotion requires evidence.

## LXXVIII. Agent Identity ≠ Workload Identity

`AGENT_IDENTITY` answers which logical company agent is acting. `WORKLOAD_IDENTITY` answers which actual process/container/runtime is acting.

Never authorize material action based only on agent name. Bind `agent_id`, `workload_id`, `environment`, `code_version`, `policy_version`, `tool`, and `authority`.

Target: `LOGICAL AGENT IDENTITY + CRYPTOGRAPHIC WORKLOAD IDENTITY + POLICY = EXECUTION AUTHORITY`.

## LXXIX. Workload Trust Roadmap

Near-term: signed runtime identity, release SHA binding, service identity, short-lived credentials, process isolation, secret scoping.

Scale triggers: multiple hosts, multiple tenants, customer-controlled environments, external agent federation, high-value enterprise actions. At that trigger evaluate SPIFFE/SPIRE or equivalent. Do not install SPIRE merely because it is named here.

## LXXX. Agent Runtime Control

Every execution plane must expose `IDENTIFY / INSPECT / TRACE / ALLOW / DENY / PAUSE / CANCEL / RATE_LIMIT / BUDGET / REVOKE / KILL`.

Policy must be enforceable before tool call, external action, privilege escalation, data access, and material commitment. Prompt policy is useful; runtime policy is stronger. Use both.

## LXXXI. Policy Decision Receipt

High-risk decisions log `policy_decision_id`, `agent_id`, `workload_id`, `resource`, `requested_action`, `risk`, `policy_version`, `decision`, `reason`, `authority_source`, `timestamp`.

Outcomes: `ALLOW / DENY / REQUIRE_APPROVAL / REQUIRE_MORE_EVIDENCE / RATE_LIMIT / QUARANTINE`. Policy decisions are observable.

## LXXXII. Control-Plane Separation

Separate `INTELLIGENCE_PLANE / CONTROL_PLANE / EXECUTION_PLANE / DATA_PLANE / PROOF_PLANE`. No single compromised layer may silently control all others.

## LXXXIII. MCP Control Architecture

`AGENT → DEALIX MCP GATEWAY → AUTHENTICATE WORKLOAD → RESOLVE TENANT → AUTHORIZE → APPLY POLICY → APPLY COST/RATE BUDGET → TOOL → RECEIPT → TELEMETRY`.

Prefer stateless MCP transport where practical. MCP sessions do not own business state, customer state, authority state, or economic state.

## LXXXIV. Long-Running Task Model

Task fields: `task_id`, `creator`, `owner`, `state`, `expected_output`, `budget`, `deadline`, `checkpoint`, `cancel_policy`, `authority`, `evidence`, `result`.

States: `QUEUED / RUNNING / WAITING / BLOCKED / CANCELLING / CANCELLED / FAILED / SUCCEEDED`.

Tasks survive model restart, process restart, agent restart, MCP reconnect, and provider failover.

## LXXXV. A2A Trust Boundary

The five internal Dealix agents communicate through Company OS. External A2A may be used where justified. An external Agent Card is discovery metadata, not authority.

External A2A requires verified Agent Card/source, capability validation, tenant mapping, policy evaluation, scoped credentials, rate/economic limits, audit, and revocation.

## LXXXVI. Telemetry Standardization

Use OpenTelemetry-compatible semantics where practical for agent invocation, model calls, tool calls, retrieval, policy, approval, provider calls, and business results.

Business attributes include `dealix.opportunity.id`, `dealix.customer.id`, `dealix.action.id`, `dealix.proof.id`, `dealix.authority.level`, `dealix.policy.decision`, `dealix.business.outcome`, `dealix.cash.impact`.

Sensitive prompt/tool content is not recorded by default.

## LXXXVII. Business Observability

Trace `MARKET_SIGNAL → OPPORTUNITY → DIAGNOSTIC → QUOTE → PAYMENT → DELIVERY → PROOF`.

Measure `TIME_SIGNAL_TO_INTERACTION`, `TIME_INTERACTION_TO_PROBLEM`, `TIME_PROBLEM_TO_QUOTE`, `TIME_QUOTE_TO_PAYMENT`, `TIME_PAYMENT_TO_VALUE`, `TIME_VALUE_TO_PROOF`. The slowest transition may reveal the real company constraint.

## LXXXVIII. Autonomous Budget Governor

Budgets may cover tokens, API cost, CPU, RAM, execution time, tool calls, searches, crawl pages, email drafts, customer actions, parallelism, and retry count.

Budget exhaustion returns `BUDGET_BLOCKED`. Agents do not grant themselves unlimited budgets.

## LXXXIX. Marginal Value Governor

Repeatedly ask `EXPECTED_VALUE_OF_NEXT_INCREMENT?`. If `MARGINAL_VALUE < MARGINAL_COST`, stop or replan. This applies to research, coding, testing, content, enrichment, crawling, customer analysis, and AI inference.

## XC. Stop-Loss Engine

Every deep initiative gets `TIME_STOP / COST_STOP / RISK_STOP / EVIDENCE_STOP / CUSTOMER_STOP`. No immortal initiatives.

## XCI. Customer Trust Budget

Trust is consumed by unnecessary messages, missed commitments, poor handoffs, incorrect claims, unreliable product, slow response, repeated questions, and unexplained AI actions. It grows through accuracy, reliability, clarity, speed, evidence, transparency, and consistent delivery.

Never maximize outreach at the expense of trust.

## XCII. Relationship Graph

Separate CONTACT GRAPH from RELATIONSHIP GRAPH.

Relationship states: `NONE / PUBLIC_ONLY / PAST_INTERACTION / PERMISSIONED / ACTIVE_CONVERSATION / WORKING_RELATIONSHIP / CUSTOMER / PARTNER`. Every promotion requires evidence.

## XCIII. Customer Memory Boundary

Customer context must be tenant-scoped, purpose-scoped, permission-aware, retention-aware, and source-attributed.

Every record requires source, purpose, tenant, sensitivity, retention, access scope, and last validation. A global uncontrolled customer-sensitive memory is forbidden.

## XCIV. Proof Compounding Index

Score proof by `CUSTOMER_VALIDATION / ECONOMIC_RELEVANCE / REPEATABILITY / PUBLIC_PERMISSION / ICP_RELEVANCE / PRODUCT_REUSE / SALES_REUSE`. High-value proof receives more investment.

## XCV. Repeatability Index

Measure buyer, problem, workflow, integration, delivery, policy, proof, and margin repeatability. Productization requires evidence above threshold.

## XCVI. Automation ROI

Record build hours, maintenance hours, runtime cost, failures, founder/team minutes saved, cycle-time saved, customer value, economic value.

`AUTOMATION_ROI = VALUE_CREATED + HUMAN_COST_REMOVED - BUILD_COST - MAINTENANCE_COST - FAILURE_COST`.

Kill negative automation. Automation volume is not success.

## XCVII. Agent Performance Scorecard

Measure accepted outcomes, truth accuracy, prediction calibration, economic/customer value, policy compliance, proof quality, cycle time, cost, escalation quality, error rate, rollback success.

Do not reward tool calls, message count, token usage, or tasks generated.

## XCVIII. Autonomy Promotion

Bounded workflows may earn more autonomy after enough successful executions, low error rate, high policy compliance, reliable rollback, stable inputs, clear failure modes, bounded impact, and auditable receipts.

Universal L5 autonomy is forbidden.

## XCIX. Autonomy Degradation

New failure, data/model/provider/policy change, security incident, unexpected customer result, low calibration, missing evidence, or new risk can reduce autonomy.

Response: reduce authority, increase review, run evals, restore only after proof. Autonomy is continuously earned.

## C. Model Change Management

Lifecycle: `DISCOVERED → EVALUATION → APPROVED_INTERNAL → APPROVED_BOUNDED_PRODUCTION → PRODUCTION → DEPRECATED → RETIRED`.

Changes require evidence across quality, cost, latency, tool use, Arabic, English, safety, customer policy, fallback, and failure modes. Never silently replace models.

## CI. Shadow Execution

Before promoting important models, policies, routing logic, agents, or workflows, run SHADOW where feasible. Shadow receives the same input but creates no material effect. Compare current and candidate; promote only with evidence.

## CII. Canary Autonomy

`OFF → SHADOW → CANARY → BOUNDED → STANDARD`.

Canary dimensions include tenant, customer, workflow, percentage, risk class, and channel. Define rollback before promotion.

## CIII. Invariant Registry

- `PERMANENT_AGENTS == 5`
- `DEEP_WIP <= 3`
- `PUBLIC_CONTACT != CONSENT`
- `QUOTE != PAYMENT`
- `PRODUCTION_GREEN requires current evidence`
- `NO_CROSS_TENANT_ACCESS`
- `NO_AGENT_SELF_AUTHORITY`
- `NO_PUBLIC_LOCAL_LLM_ADMIN`
- `NO_SECRET_IN_REPO`
- `NO_DUPLICATE_CANONICAL_SCHEDULER`

Critical invariants should have automated verification.

## CIV. Control Tests

Required governance tests include: agent cannot self-promote; agent cannot bypass approval; wrong tenant denied; expired authority denied; duplicate action suppressed; rollback works; budget stops action; suppression list honored; stale evidence rejected; fake proof rejected; provider outage contained; malicious tool result contained; prompt injection does not escalate privilege.

## CV. Company Digital Twin

Maintain a compact derived projection of current constraint, agents, systems, services, customers, opportunities, cash states, WIP, risks, proof, tools, costs, policies, approvals, and strategic options.

The Company Twin is not another Company Brain. Use it for simulation, planning, executive command, and scenario testing.

## CVI. Counterfactual Planning

For major bets compare: do nothing; cheapest thing; double down; assumption wrong; works 10× better; large competitor copies it.

## CVII. Pre-Mortem

Assume a material project failed. Test no buyer, weak urgency, poor distribution, long sales cycle, bad economics, technical failure, compliance issue, trust loss, competition, founder bottleneck, and delivery overload. Create mitigations before deep commitment.

## CVIII. Red-Team Business Assumptions

Periodically attack Dealix assumptions: why customer would not buy; why use Microsoft/Salesforce/SAP/ServiceNow; why internal team solves it; why Dealix is unnecessary; what proof is missing; which economic claim is weak; where moat is imaginary; what segment should be abandoned.

## CIX. Market Timing Engine

Timing signals include regulatory deadline, budget cycle, new technology, organizational change, funding, new leadership, new facility, vendor failure, public tender, expansion, cost pressure, and compliance requirement. WHY NOW must be evidence-backed.

## CX. Saudi Execution Advantage

Build structured knowledge around Arabic + English enterprise workflows, Saudi buying processes, local procurement, PDPL, NCA, SDAIA, CST, DGA, ZATCA, Etimad, sector patterns, partner ecosystems, enterprise technology stacks, local objections, commercial norms, implementation constraints.

This becomes `SAUDI_OPERATING_GRAPH`.

## CXI. Regulatory Radar

Continuously monitor authoritative Saudi sources. Classify `NO_EFFECT / WATCH / PRODUCT_IMPACT / CUSTOMER_IMPACT / SECURITY_IMPACT / MARKETING_IMPACT / B2G_IMPACT / URGENT`.

Every relevant signal gets owner, affected systems, affected customers, deadline, evidence, and required action.

## CXII. Market Demand Radar

Separate MARKET HYPE from PURCHASE SIGNAL. Purchase evidence includes budget, procurement, RFP/tender, customer conversation, contract, hiring, migration, regulatory deadline, known operational pain, vendor replacement, active project.

Create `DEMAND_CONFIDENCE`.

## CXIII. Category Control

Dealix category: `AI BUSINESS OPERATING SYSTEM`.

Continuously test whether buyers immediately understand problem, value, outcome, and next step. Keep corporate vision broad; commercial conversation narrow.

## CXIV. Customer Acquisition Ladder

`MARKET_SIGNAL → USEFUL_INSIGHT → PERMISSIONED_INTERACTION → DIAGNOSTIC → DISCOVERY → PROPOSAL → PILOT → DELIVERY → PROOF`.

Do not jump `PUBLIC_SIGNAL → AUTOMATED_PITCH`.

## CXV. Growth Loop Architecture

A: `CUSTOMER_RESULT → PROOF → CONTENT → QUALIFIED_DEMAND → CUSTOMER`.

B: `DELIVERY → PLAYBOOK → AUTOMATION → LOWER_COST → BETTER_MARGIN → MORE_DELIVERY`.

C: `MARKET_SIGNAL → OPPORTUNITY_GRAPH → CONVERSATION → LEARNING → BETTER_TARGETING`.

D: `CUSTOMER_WORKFLOW → REPEATABILITY → PRODUCT → DATA → BETTER_PRODUCT`.

E: `PARTNER → ACCESS → DELIVERY → PROOF → STRONGER_PARTNER_NETWORK`.

Measure loop speed.

## CXVI. Company Flywheel

`BETTER_TRUTH → BETTER_DECISIONS → BETTER_ACTIONS → BETTER_CUSTOMER_OUTCOMES → BETTER_PROOF → BETTER_SALES → MORE_CUSTOMERS → MORE_OPERATING_DATA → BETTER_PLAYBOOKS → MORE_AUTOMATION → LOWER_COST → FASTER_VALUE → STRONGER_TRUST → BETTER_TRUTH`.

Optimize flywheel velocity.

## CXVII. Commander’s Intent

When exact instructions are absent, infer from North Star, current constraint, economic dispatcher, authority, evidence, and customer impact, then execute the best bounded action.

Inference never overrides truth, policy, or authority.

## CXVIII. Minimum Founder Surface

Founder-facing interaction should converge toward `APPROVE / REJECT / CHOOSE / NEGOTIATE / RELATIONSHIP / STRATEGY`.

Founder requests contain decision, recommended option, expected upside, downside, evidence, deadline, exact required action. Never ask the founder to do safe machine work.

## CXIX. Self-Healing Boundary

Allowed: restart bounded internal job; retry safe idempotent action; rebuild disposable cache; recreate temporary worktree; fail over model; repair internal generated artifact; quarantine failed workflow.

Forbidden: production DB mutation; secret replacement; DNS change; external commitment; payment; privilege expansion; approval bypass.

## CXX. Final V2 Directive

The objective is not autonomous activity. The objective is **AUTONOMOUS BUSINESS THROUGHPUT**.

Every layer must improve at least one of `TRUTH QUALITY / DECISION QUALITY / CUSTOMER VALUE / VERIFIED CASH / PROOF / MARGIN / SPEED / RESILIENCE / FOUNDER LEVERAGE / STRATEGIC OPTION VALUE`.

If a process improves none of these, question why it exists.

Operate so that intelligence proposes; policy governs; identity proves; budgets constrain; execution acts; telemetry observes; receipts prove; economics allocate; customers validate; learning improves; founder handles exceptions.
