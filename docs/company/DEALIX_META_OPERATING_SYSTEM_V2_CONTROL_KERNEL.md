# DEALIX Ω∞ — META-OPERATING SYSTEM V2 — CONTROL KERNEL

Effective: 2026-09-11

Status: **Canonical constitutional superlayer candidate.**

Machine-readable authority: `config/company/dealix_control_kernel_v2.json`  
Fail-closed verifier: `scripts/commercial/verify_dealix_control_kernel_v2.py`  
Runtime primitives: `scripts/commercial/dealix_control_kernel_v2.py`

This layer **overrides conflicting lower-level operating logic** but **does not replace the existing Dealix Constitution**. It strengthens decision quality, economic allocation, agent identity, execution safety, learning, scalability, and enterprise readiness.

## LXXI — Decision Quality Kernel

Distinguish `DATA / EVIDENCE / BELIEF / PREDICTION / DECISION / ACTION / RESULT`. Never store prediction as fact or inference as customer evidence. Material decisions may record `decision_id`, `decision`, `decision_owner`, `evidence`, `assumptions`, `confidence`, `expected_result`, `expected_value`, `downside`, `reversibility`, `decision_deadline`, `prediction`, `actual_result`, `calibration_error`. Goal: **MAKE BETTER DECISIONS FASTER**.

## LXXII — Confidence-Aware Economic Dispatcher

Normalize inputs to `0.00 → 1.00`.

`VALUE_VECTOR = 0.30*CASH_IMPACT + 0.20*CUSTOMER_VALUE + 0.15*PROOF_VALUE + 0.15*CONSTRAINT_RELIEF + 0.10*FOUNDER_TIME_SAVED + 0.10*STRATEGIC_REUSE`

`EXECUTION_DRAG = 0.25*TIME_COST + 0.20*CASH_COST + 0.20*FAILURE_RISK + 0.15*IRREVERSIBILITY + 0.10*COMPLEXITY_COST + 0.10*MAINTENANCE_COST`

`CONFIDENCE_FACTOR = EVIDENCE_CONFIDENCE * DATA_FRESHNESS`

`FINAL_PRIORITY = VALUE_VECTOR * CONFIDENCE_FACTOR * CONSTRAINT_FIT * URGENCY_FACTOR / MAX(0.20, EXECUTION_DRAG)`

The score is a decision aid, not objective truth. If candidates are within 10%, prefer higher reversibility, faster feedback, higher customer learning, lower founder attention, then stronger proof potential.

## LXXIII — Value of Information

Before expensive, risky, or irreversible action ask what uncertainty blocks the decision, what evidence could reduce it, what economic loss better information could avoid, its cost, and speed.

`VOI = EXPECTED_DECISION_LOSS_AVOIDED / INFORMATION_COST`

If VOI exceeds immediate execution advantage, research/test first. Research must not become procrastination.

## LXXIV — Reversibility Classification

`R0 READ_ONLY / R1 INSTANTLY_REVERSIBLE / R2 REVERSIBLE_SMALL_COST / R3 REVERSIBLE_MATERIAL_COST / R4 DIFFICULT_TO_REVERSE / R5 EFFECTIVELY_IRREVERSIBLE`.

Autonomy rises with reversibility; evidence requirements rise with irreversibility. High-uncertainty R4/R5 defaults HOLD. High-confidence R0/R1 defaults EXECUTE. The founder text defines no numeric threshold, so runtime must not invent one.

## LXXV — Business State Machines

Opportunity:
`RESEARCH_ONLY → KNOWN → INTERACTION → QUALIFIED_PROBLEM → DIAGNOSTIC → DISCOVERY → QUOTE_READY → QUOTED → PAYMENT_PENDING → PAID → DELIVERY → PROOF → EXPANSION`.

Every transition requires `from_state`, `to_state`, `required_evidence`, `authority`, `side_effect`, `receipt`. Illegal transition: `INVALID_STATE_TRANSITION`.

## LXXVI — Production State Machine

`SOURCE_ACCEPTED → BUILD_ACCEPTED → RELEASE_CANDIDATE → DEPLOYED → HEALTHY → RELEASE_PARITY_PROVEN → BUSINESS_FLOW_PROVEN → PRODUCTION_GREEN`.

Rollback changes green to `DEGRADED` or `ROLLBACK_ACTIVE`. Previous green never makes a new release green.

## LXXVII — Financial State Machine

`OPPORTUNITY_VALUE → QUOTE → ACCEPTED_COMMERCIAL_TERMS → INVOICE → PAYMENT_REQUESTED → PAYMENT_PENDING → PAYMENT_VERIFIED → CASH_AVAILABLE → REVENUE_RECOGNITION_STATE`.

Never auto-promote; every promotion requires evidence.

## LXXVIII — Agent Identity ≠ Workload Identity

Agent identity names the logical company agent. Workload identity identifies the actual process/container/runtime. Never authorize material action by agent name alone. Bind `agent_id`, `workload_id`, `environment`, `code_version`, `policy_version`, `tool`, `authority`.

Target: `LOGICAL_AGENT_IDENTITY + CRYPTOGRAPHIC_WORKLOAD_IDENTITY + POLICY = EXECUTION_AUTHORITY`.

## LXXIX — Workload Trust Roadmap

Near-term: signed runtime identity, release-SHA binding, service identity, short-lived credentials, process isolation, secret scoping. Evaluate SPIFFE/SPIRE or equivalent only when scale triggers appear: multiple hosts/tenants, customer-controlled environments, external federation, or high-value enterprise actions. Do not install SPIRE merely because it is mentioned here.

## LXXX — Agent Runtime Control

Execution planes expose `IDENTIFY / INSPECT / TRACE / ALLOW / DENY / PAUSE / CANCEL / RATE_LIMIT / BUDGET / REVOKE / KILL`. Runtime policy must apply before tool calls, external actions, privilege escalation, data access, and material commitment. Prompt policy is useful; runtime policy is stronger. Use both.

## LXXXI — Policy Decision Receipt

High-risk decisions log `policy_decision_id`, `agent_id`, `workload_id`, `resource`, `requested_action`, `risk`, `policy_version`, `decision`, `reason`, `authority_source`, `timestamp`.

Outcomes: `ALLOW / DENY / REQUIRE_APPROVAL / REQUIRE_MORE_EVIDENCE / RATE_LIMIT / QUARANTINE`. Policy decisions are observable.

## LXXXII — Control-Plane Separation

Separate `INTELLIGENCE / CONTROL / EXECUTION / DATA / PROOF` planes. No compromised layer may silently control all others.

## LXXXIII — MCP Control Architecture

Preferred flow: `AGENT → DEALIX_MCP_GATEWAY → AUTHENTICATE_WORKLOAD → RESOLVE_TENANT → AUTHORIZE → APPLY_POLICY → APPLY_COST_RATE_BUDGET → TOOL → RECEIPT → TELEMETRY`.

Prefer stateless MCP transport where practical. MCP session state must not own business, customer, authority, or economic state.

## LXXXIV — Long-Running Task Model

Durable task fields: `task_id`, `creator`, `owner`, `state`, `expected_output`, `budget`, `deadline`, `checkpoint`, `cancel_policy`, `authority`, `evidence`, `result`.

States: `QUEUED / RUNNING / WAITING / BLOCKED / CANCELLING / CANCELLED / FAILED / SUCCEEDED`. Tasks survive model/process/agent restart, MCP reconnect, and provider failover.

## LXXXV — A2A Trust Boundary

The five internal Dealix agents use Company OS. External A2A may be used when justified. External Agent Card is discovery metadata, not authority. Require verified card/source, capability validation, tenant mapping, policy evaluation, scoped credentials, rate/economic limits, audit, revocation.

## LXXXVI — Telemetry Standardization

Use OpenTelemetry-compatible semantics where practical for agent invocation, model/tool calls, retrieval, policy, approval, provider calls, and business results. Standard business attributes include `dealix.opportunity.id`, `dealix.customer.id`, `dealix.action.id`, `dealix.proof.id`, `dealix.authority.level`, `dealix.policy.decision`, `dealix.business.outcome`, `dealix.cash.impact`. Do not record sensitive prompt/tool content by default.

## LXXXVII — Business Observability

Trace `MARKET_SIGNAL → OPPORTUNITY → DIAGNOSTIC → QUOTE → PAYMENT → DELIVERY → PROOF`. Measure `TIME_SIGNAL_TO_INTERACTION`, `TIME_INTERACTION_TO_PROBLEM`, `TIME_PROBLEM_TO_QUOTE`, `TIME_QUOTE_TO_PAYMENT`, `TIME_PAYMENT_TO_VALUE`, `TIME_VALUE_TO_PROOF`. The slowest transition may reveal the actual company constraint.

## LXXXVIII — Autonomous Budget Governor

Budgets may cover tokens, API cost, CPU, RAM, execution time, tool calls, searches, crawl pages, email drafts, customer actions, parallelism, retries. Exhaustion returns `BUDGET_BLOCKED`. Agents cannot self-grant unlimited budgets.

## LXXXIX — Marginal Value Governor

During long work ask `EXPECTED_VALUE_OF_NEXT_INCREMENT?`. If `MARGINAL_VALUE < MARGINAL_COST`, stop or replan. Applies to research, coding, testing, content, enrichment, crawling, customer analysis, inference.

## XC — Stop-Loss Engine

Every deep initiative gets `TIME_STOP / COST_STOP / RISK_STOP / EVIDENCE_STOP / CUSTOMER_STOP`. No immortal initiatives.

## XCI — Customer Trust Budget

Trust is consumed by unnecessary messages, missed commitments, poor handoffs, incorrect claims, unreliable product, slow response, repeated questions, unexplained AI actions; increased by accuracy, reliability, clarity, speed, evidence, transparency, consistent delivery. Never maximize outreach at the expense of trust.

## XCII — Relationship Graph

Keep CONTACT GRAPH separate from RELATIONSHIP GRAPH. States: `NONE / PUBLIC_ONLY / PAST_INTERACTION / PERMISSIONED / ACTIVE_CONVERSATION / WORKING_RELATIONSHIP / CUSTOMER / PARTNER`. Every promotion requires evidence.

## XCIII — Customer Memory Boundary

Customer context must be tenant-scoped, purpose-scoped, permission-aware, retention-aware, source-attributed. Every record requires source, purpose, tenant, sensitivity, retention, access scope, last validation. Global uncontrolled customer-sensitive memory is forbidden.

## XCIV — Proof Compounding Index

Score proof by `CUSTOMER_VALIDATION / ECONOMIC_RELEVANCE / REPEATABILITY / PUBLIC_PERMISSION / ICP_RELEVANCE / PRODUCT_REUSE / SALES_REUSE`. High-value proof receives more investment.

## XCV — Repeatability Index

Measure `buyer / problem / workflow / integration / delivery / policy / proof / margin` repeatability. Productization becomes eligible only after the required threshold is met with evidence.

## XCVI — Automation ROI

Every automation records `build_hours`, `maintenance_hours`, `runtime_cost`, `failures`, `founder_minutes_saved`, `team_minutes_saved`, `cycle_time_saved`, `customer_value`, `economic_value`.

The constitutional components are `VALUE_CREATED`, `HUMAN_COST_REMOVED`, `BUILD_COST`, `MAINTENANCE_COST`, `FAILURE_COST`. **The founder text does not define operators or weights between these components; no arithmetic formula may be invented silently.** An explicit policy must define aggregation before a scalar ROI is treated as authoritative. Kill negative automation. Automation volume is not success.

## XCVII — Agent Performance Scorecard

Measure `accepted_outcomes`, truth accuracy, prediction calibration, economic/customer value, policy compliance, proof quality, cycle time, cost, escalation quality, error rate, rollback success. Do not reward tool calls, message count, token usage, tasks generated.

## XCVIII — Autonomy Promotion

Bounded workflows may earn more autonomy after enough successful executions, low error rate, high policy compliance, reliable rollback, stable inputs, clear failure modes, bounded impact, auditable receipts. Universal L5 autonomy is forbidden.

## XCIX — Autonomy Degradation

Triggers include new failure, data/model/provider/policy change, security incident, unexpected customer result, low calibration, missing evidence, new risk. Respond by reducing authority, increasing review, running evals, and restoring only after proof. Autonomy is earned continuously.

## C — Model Change Management

Lifecycle: `DISCOVERED → EVALUATION → APPROVED_INTERNAL → APPROVED_BOUNDED_PRODUCTION → PRODUCTION → DEPRECATED → RETIRED`. Require evidence across quality, cost, latency, tool use, Arabic, English, safety, customer policy, fallback, failure modes. Never silently replace models.

## CI — Shadow Execution

Before important model/policy/routing/agent/workflow promotion, use SHADOW where feasible: same input, no material effect. Compare incumbent and candidate; promote only with evidence.

## CII — Canary Autonomy

Progression: `OFF → SHADOW → CANARY → BOUNDED → STANDARD`. Canary dimensions: tenant, customer, workflow, percentage, risk class, channel. Define rollback before promotion.

## CIII — Invariant Registry

Machine-check critical invariants including `PERMANENT_AGENTS == 5`, `DEEP_WIP <= 3`, `PUBLIC_CONTACT != CONSENT`, `QUOTE != PAYMENT`, `PRODUCTION_GREEN requires current evidence`, `NO_CROSS_TENANT_ACCESS`, `NO_AGENT_SELF_AUTHORITY`, `NO_PUBLIC_LOCAL_LLM_ADMIN`, `NO_SECRET_IN_REPO`, `NO_DUPLICATE_CANONICAL_SCHEDULER`.

## CIV — Control Tests

Test that agents cannot self-promote or bypass approval; wrong tenant and expired authority are denied; duplicate actions are suppressed; rollback works; budgets stop actions; suppression lists are honored; stale evidence and fake proof are rejected; provider outage and malicious tool results are contained; prompt injection cannot escalate privilege.

## CV — Company Digital Twin

Maintain a compact machine-readable derived projection of current constraint, agents, systems, services, customers, opportunities, cash states, active WIP, risks, proof, tools, costs, policies, approvals, strategic options. The Twin is not another Company Brain. Use it for simulation, planning, executive command, scenario testing.

## CVI — Counterfactual Planning

Before major bets compare: do nothing; cheapest thing; double down; assumption wrong; 10× upside; large competitor copies it. Avoid single-path strategy.

## CVII — Pre-Mortem

Assume a material project failed. Ask why: no buyer, weak urgency, poor distribution, long sales cycle, bad economics, technical failure, compliance issue, trust loss, competition, founder bottleneck, delivery overload. Create mitigations before deep commitment.

## CVIII — Red-Team Business Assumptions

Periodically ask why a customer would not buy; why they would use Microsoft/Salesforce/SAP/ServiceNow; why an internal team solves it; why Dealix is unnecessary; what proof is missing; which economic claim is weak; where the moat is imaginary; what segment should be abandoned.

## CIX — Market Timing Engine

Timing signals: regulatory deadline, budget cycle, new technology, organizational change, funding, new leadership, new facility, vendor failure, public tender, expansion, cost pressure, compliance requirement. WHY NOW must be evidence-backed.

## CX — Saudi Execution Advantage

Build structured knowledge around Arabic/English enterprise workflows, Saudi buying processes, local procurement, PDPL, NCA, SDAIA, CST, DGA, ZATCA, Etimad, sector patterns, partner ecosystems, enterprise stacks, local objections, commercial norms, implementation constraints. This becomes `SAUDI_OPERATING_GRAPH`.

## CXI — Regulatory Radar

Continuously monitor authoritative Saudi sources. Classify `NO_EFFECT / WATCH / PRODUCT_IMPACT / CUSTOMER_IMPACT / SECURITY_IMPACT / MARKETING_IMPACT / B2G_IMPACT / URGENT`. Each relevant signal creates owner, affected systems/customers, deadline, evidence, required action.

## CXII — Market Demand Radar

Separate MARKET HYPE from PURCHASE SIGNAL. Purchase evidence includes budget, procurement, RFP/tender, customer conversation, contract, hiring, migration, regulatory deadline, known operational pain, vendor replacement, active project. Track `DEMAND_CONFIDENCE`.

## CXIII — Category Control

Category: `AI BUSINESS OPERATING SYSTEM`. Continuously test whether buyers immediately understand problem, value, outcome, next step. Keep corporate vision broad and commercial conversation narrow.

## CXIV — Customer Acquisition Ladder

`MARKET_SIGNAL → USEFUL_INSIGHT → PERMISSIONED_INTERACTION → DIAGNOSTIC → DISCOVERY → PROPOSAL → PILOT → DELIVERY → PROOF`. Do not jump `PUBLIC_SIGNAL → AUTOMATED_PITCH`.

## CXV — Growth Loop Architecture

A: `CUSTOMER_RESULT → PROOF → CONTENT → QUALIFIED_DEMAND → CUSTOMER`  
B: `DELIVERY → PLAYBOOK → AUTOMATION → LOWER_COST → BETTER_MARGIN → MORE_DELIVERY`  
C: `MARKET_SIGNAL → OPPORTUNITY_GRAPH → CONVERSATION → LEARNING → BETTER_TARGETING`  
D: `CUSTOMER_WORKFLOW → REPEATABILITY → PRODUCT → DATA → BETTER_PRODUCT`  
E: `PARTNER → ACCESS → DELIVERY → PROOF → STRONGER_PARTNER_NETWORK`

Measure loop speed.

## CXVI — Company Flywheel

`BETTER_TRUTH → BETTER_DECISIONS → BETTER_ACTIONS → BETTER_CUSTOMER_OUTCOMES → BETTER_PROOF → BETTER_SALES → MORE_CUSTOMERS → MORE_OPERATING_DATA → BETTER_PLAYBOOKS → MORE_AUTOMATION → LOWER_COST → FASTER_VALUE → STRONGER_TRUST → BETTER_TRUTH`.

Optimize flywheel velocity.

## CXVII — Commander’s Intent

When exact instructions are absent, infer from North Star, current constraint, economic dispatcher, authority, evidence, customer impact; execute the best bounded action. Inference never overrides truth, policy, authority.

## CXVIII — Minimum Founder Surface

Founder-facing interaction converges toward `APPROVE / REJECT / CHOOSE / NEGOTIATE / RELATIONSHIP / STRATEGY`. Requests contain decision, recommended option, expected upside, downside, evidence, deadline, exact required action. Never ask the founder to manually do safe machine work.

## CXIX — Self-Healing Boundary

Allowed: restart bounded internal job, retry safe idempotent action, rebuild disposable cache, recreate temporary worktree, fail over model, repair internal generated artifact, quarantine failed workflow.

Forbidden: production DB mutation, secret replacement, DNS change, external commitment, payment, privilege expansion, approval bypass.

## CXX — Final V2 Directive

The objective is not autonomous activity. It is **AUTONOMOUS BUSINESS THROUGHPUT**. Every layer must improve at least one of `TRUTH_QUALITY / DECISION_QUALITY / CUSTOMER_VALUE / VERIFIED_CASH / PROOF / MARGIN / SPEED / RESILIENCE / FOUNDER_LEVERAGE / STRATEGIC_OPTION_VALUE`.

If a process improves none of these, question why it exists.

Operate so that **intelligence proposes; policy governs; identity proves; budgets constrain; execution acts; telemetry observes; receipts prove; economics allocate; customers validate; learning improves; founder handles exceptions.**
