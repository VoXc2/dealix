# DEALIX Ω∞ — Canonical Agentic Holding Constitution

**Status:** CANONICAL  
**Effective date:** 2026-09-12  
**North Star:** `CASH_READY_AUTONOMOUS_DEALIX_COMPANY`  
**Design basis:** `docs/architecture/DEALIX_AGENTIC_HOLDING_SECTOR_MESH.md`  
**Machine-readable contract:** `config/company/agentic_holding_canonical_contract.json`

This document is the authority for the Dealix company-agent architecture from the effective date above. The earlier Sector Mesh document remains design history and rationale; where wording conflicts, this constitution plus the machine-readable contract wins unless superseded by newer verified authority.

## 1. Company shape

Dealix is one governed Agentic Holding, not a collection of disconnected AI businesses.

```text
DEALIX HOLDING
├── Group Council + Shared Services
├── Sector Companies [dynamic from canonical sector registry]
│   └── Arm Pods [dynamic from canonical arm registry]
│       └── Bounded Specialists [created only when work justifies them]
└── One Company Machine / Brain / Economic Truth / Approval / Proof / Scheduler / Model Policy
```

Logical agent count is independent from runtime worker count. Hundreds or thousands of logical identities may exist while only a resource-governed subset runs.

## 2. Agent identity and hierarchy

Every logical agent must have:

- `agent_id`
- `parent_id`
- layer: holding / group / sector_company / arm_pod / bounded_specialist
- authority scope
- capability scope
- sector scope where applicable
- arm scope where applicable
- lifecycle state
- evidence/receipt lineage

No orphan agent, arm, sector company, queue, truth store, scheduler, model router, approval path or proof store is allowed.

The historical fixed-five agent model is compatibility metadata only. It is not the canonical organization model.

## 3. Coordination law: manager vs handoff

Use a **manager pattern** when one owner must retain control, synthesize multiple specialists, preserve shared commercial truth, or produce the final customer/company output.

Use a **handoff** when a specialist should take ownership of a scoped workflow state and its instructions materially differ from the current agent.

Every handoff must include a structured packet with at least:

`trace_id, source_agent, target_agent, reason, scope, facts, inferences, evidence_refs, authority_scope, relationship_state, consent_state, context_filter, expected_output, acceptance_criteria, next_state_sought`

A handoff never transfers authority, relationship, consent, customer proof or publication permission implicitly.

## 4. Context isolation

Pass the minimum useful context, not the entire company history by default.

- filter handoff history;
- separate facts, inferences and unknowns;
- keep provenance with market/customer claims;
- do not propagate secrets through prompts;
- do not leak customer-specific data across sector/company scopes;
- retrieve deeper context only when the receiving specialist actually needs it.

## 5. Tool and side-effect guardrails

Every tool/action is classified as:

- `read_only`
- `reversible_internal`
- `material_external`
- `destructive`

Material/destructive actions must pass blocking pre-execution guardrails. Relevant output must also pass post-execution validation before it can become proof, a commitment or a public/customer artifact.

Exact-action authority remains required for live send, publish, payment/spend, contract/tender commitment, protected merge where governed, production mutation, DNS/DB/secret mutation and destructive provider/account operations.

No agent may self-approve or infer authority from model output.

## 6. Tracing and receipts

Every material workflow must have an end-to-end `trace_id` and record:

- agent start/end;
- model calls and route class;
- tool calls;
- handoffs;
- guardrail results;
- approval checks;
- acceptance checks;
- retries/failures;
- rollback;
- final receipt and evidence references.

Minimum correlation fields are `trace_id`, `work_id`, `agent_id`, `parent_agent_id`, opportunity/project id, authority level, model route, cost class and evidence refs.

Historical PASS is never current exact-head PASS.

## 7. MCP and connector security

Protected remote tools require a real authorization boundary at the server/tool layer.

Required posture:

- validate authorization issuer where the protocol supports it;
- bind credentials to the issuer that created them;
- use resource-bound access tokens;
- forbid token passthrough;
- use explicit agent identity and delegated scope;
- support scope step-up rather than issuing broad standing authority;
- prefer current client-identity metadata / managed-enterprise authorization mechanisms when supported;
- keep credentials out of model prompt context;
- protect metadata/discovery fetches from SSRF with HTTPS-only policy, internal-network blocking, timeout, size limits and strict schema validation.

## 8. Resource and model economics

Execution law:

`deterministic first -> local/free/included cheapest adequate -> acceptance-gated escalation -> paid only with explicit authority`

Resource Governor decides runtime concurrency from CPU, RAM, swap, disk/IO, provider/model quota, worktree capacity, cost, risk, expected economic value, duration, contention and incident state.

Parallel repository writers require isolated worktrees.

No uncontrolled paid spill.

## 9. Evaluation and verification

Material outputs require verifier evidence. The verifier must not self-approve the work it originated.

Independent review is preferred for:

- architecture;
- security;
- Economic Truth / financial state;
- customer proof;
- production release identity.

Acceptance criteria should exist before execution for material work.

Synthetic/demo proof is not customer proof. Delivery is not customer value. Merge is not deployment.

## 10. Commercial company loop

Every Sector Company can operate the same governed path:

`Signal -> Evidence -> Relationship State -> Qualified Problem -> FREE Diagnostic -> Discovery -> Solution Design -> Customer-Specific Proposal -> Negotiation Preparation -> Pilot Decision -> Invoice -> Verified Payment -> Delivery -> Acceptance -> Customer-Validated Proof -> Expansion / Referral / Productization`

Sector companies specialize the context; they do not create parallel commercial truth.

## 11. Learning and lifecycle

Track per logical agent/template:

- accepted task success;
- economic value;
- latency;
- token/API cost;
- failures/retries;
- authority or evidence violations;
- founder/human intervention;
- reusable assets and proof value.

Lifecycle decisions are `PROMOTE / KEEP / SPECIALIZE / IMPROVE / DEMOTE / SUSPEND / KILL`.

Self-improvement may change prompts, skills, retrieval, context, routing, heuristics, tests and tool selection only through versioned, tested, reviewable, rollback-capable changes with receipts. No agent can grant itself external authority.

## 12. Truth firewall

- Research != Relationship
- Public contact != Consent
- Signal != Qualified Problem
- Engagement != Buyer Intent
- Draft != Sent
- Quote != Invoice
- Invoice != Payment
- Payment Request != Verified Cash
- Payment != Revenue without reconciliation
- Synthetic/Demo != Customer Proof
- Delivery != Customer Value
- Customer Value != Publication Permission
- HTTP 200 != Release Identity
- Merged PR != Deployed Release
- Historical PASS != Current Exact-Head PASS
- Model Output != Authority

## 13. Research-informed hardening

The coordination/security additions above are informed by current primary documentation, not copied as a framework dependency:

- OpenAI Agents SDK: agents, manager/agent-as-tool vs handoff orchestration, guardrails, tracing, human-in-the-loop.
- OpenAI handoff guidance: authorization must be checked before application side effects and handoff context can be filtered.
- OpenAI guardrail guidance: blocking guardrails are appropriate when token/tool side effects must not begin before validation; tool guardrails protect individual tool invocations.
- OpenAI tracing: model, tool, handoff and guardrail spans provide end-to-end observability.
- MCP 2026-07-28: authorization hardening includes issuer validation and issuer-bound credentials; newer protocol direction prioritizes enterprise security and agent identity/delegated authority.
- Anthropic production guidance reinforces simple composable workflows, orchestrator-workers, evaluator-optimizer, environment ground truth, stopping conditions, and adding complexity only when it measurably improves results.

Canonical URLs and applied principles are recorded in `config/company/agentic_holding_canonical_contract.json`.

## 14. Acceptance required for architecture changes

Any future architecture-changing PR must prove at minimum:

1. One-Company Law remains true.
2. No orphan hierarchy nodes.
3. Dynamic Group/Sector/Arm identities work.
4. Logical agents do not imply process-per-agent execution.
5. Runtime concurrency remains resource governed.
6. Handoffs preserve trace, scope, filtered context and explicit authority.
7. Material tools are fail-closed before side effects.
8. Connector/MCP credentials are identity/resource bound and not passed through prompts.
9. Economic Truth and Proof semantics remain intact.
10. Paid spill remains disabled by default.
11. External/material authority remains exact-action-bound.
12. Exact-current-main focused acceptance and diff-check pass before merge readiness.

## 15. Current implementation path

- Commercial policy / work packets: merged Commercial Reset foundation (#1745).
- Model cost firewall: merged no-paid-spill hardening (#1750).
- Runtime hierarchy / Resource Governor / Session Factory adapter: continue through the active Agentic Holding runtime lane and migration spine.
- Existing compatibility aliases are removed only after their dependent executors/verifiers migrate.

This architecture is intentionally evolutionary: extend the canonical Company Machine; never create a second one.
