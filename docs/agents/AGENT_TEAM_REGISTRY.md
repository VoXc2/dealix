# Dealix Agent Governance Registry — سجل حوكمة الوكلاء

This document is the human-readable mirror of the **Omega V3 registry-derived
Agentic Holding**. It is not a manually fixed roster and it must never become a
second source of runtime identity.

Canonical source:

```python
from dealix.agentic_holding.runtime import build_current_registry
registry = build_current_registry()
receipt = registry.receipt()
```

The source/runtime registry decides which logical identities exist. This document
explains the governance contract around them.

## Canonical company architecture

`Dealix Holding -> Company Control Plane -> Sector Companies -> Arm Pods -> Specialist Logical Agents -> ResourceGovernor-bounded runtime workers`

Important consequences:

- fleet size is registry-derived, not fixed at five;
- sector, arm, pod and logical-agent counts are observations, not architecture
  ceilings;
- business Top-3 prioritization is economic focus, not a global worker limit;
- modifying execution is admitted by the canonical Session Factory and
  ResourceGovernor;
- OpenCode is an execution surface, not a second model router or scheduler;
- Builder != Verifier;
- orphan logical agents or namespaces fail closed;
- no agent can mint model/cost/data/privacy authority;
- founder unattended model law is **provider-neutral free/local-first**; DeepSeek is eligible only through the canonical broker when explicit-free or trusted included capacity is proven; no silent paid spill;
- safe internal/source work may execute autonomously at L0-L4 in bounded
  exact-head isolated worktrees; material external effects are L5 and require
  exact action-bound authority.

## Current commercial authority

`Free Execution Diagnostic -> Qualified Discovery -> Customer-Specific Quote -> Outcome Sprint/Pilot -> Proof Review -> Dealix Runtime | Stop | Expand | Redesign`

- all diagnostics are free by current default authority;
- no public/automatic fixed price or fixed sprint/pilot duration;
- price, duration, terms, scope, acceptance and remedies are customer-specific
  after qualified discovery and require evidence-linked authority;
- research/public signals may create internal research and reusable diagnostics,
  never relationship, buyer intent, pipeline, quote, revenue or public proof;
- no cold WhatsApp, no automated personal LinkedIn, no scraping, no fabricated
  proof, no guaranteed revenue/ROI, no unsupported certification/compliance/data
  residency or government-access claims.

Truth firewall:
`Research != Relationship`; `Public Contact != Consent`; `Signal != Qualified Problem`;
`Draft != Sent`; `Quote != Invoice`; `Invoice != Payment`; `Payment != Revenue`;
`Delivery != Customer Value`; `Customer Value != Public Proof`; `Merged != Deployed`;
`HTTP 200 != release identity`.

---

## Registry layers

### Group / Holding roles

`dealix.agentic_holding.runtime.GROUP_ROLES` defines logical holding/control-plane
roles such as president, strategy/capital, operations, technology, AI automation,
economic truth, revenue, growth, delivery, customer success, research,
engineering, security, risk, governance/compliance, procurement/B2G,
partnerships, brand/content, QA/verification, proof and self-improvement.

These are logical responsibilities. They do not imply one process per role.
Runtime workers are bounded, temporary executors admitted by ResourceGovernor.

### Sector Companies

The canonical `SectorCompanyFactory` supplies current sectors. Each sector receives
registry-derived sector roles such as strategy, intelligence, research, sales,
business development, diagnostic, solution architecture, product, delivery,
customer success, economics, procurement/B2G, compliance, content, distribution,
partnerships, data, QA, proof and learning.

All sectors may maintain intelligence coverage. Deep execution is dynamically
allocated to the highest evidence/economic opportunities.

### Arm Pods

Active arms come from `dealix.commercial.arm_registry.get_active_arms()`. Each
applicable sector/arm namespace gets bounded pod roles (`lead`, `scout`,
`operator`, `verifier`) from the canonical registry. Unsupported/unmapped arms
are visible in the registry receipt and must fail governance acceptance rather
than being silently ignored.

### Specialist logical agents

Additional specialist identities must be children of a valid canonical namespace,
carry bounded authority, and remain subject to Session Factory, ResourceGovernor,
model/data policy, effect classification and independent verification.

---

## Legacy executor aliases — compatibility only

The following historical names remain useful entrypoints/surfaces but are **not the
canonical fleet architecture**:

| Alias | Compatibility responsibility | Current law |
|---|---|---|
| `dealix-pm` | founder/operator orchestration facade | delegates into Agentic Holding; does not define fleet size |
| `dealix-sales` | revenue/commercial facade | free diagnostic -> qualified discovery -> customer-specific quote; drafts only unless exact L5 authority |
| `dealix-delivery` | delivery/proof facade | customer-specific Outcome Sprint/Pilot; no fixed 7-day/30-day authority |
| `dealix-engineer` | engineering facade | exact-head isolated L0-L4 source execution; no direct-main or production authority |
| `dealix-content` | content/distribution facade | evidence-backed bilingual drafts; no unapproved publication |

Claude/Codex files for these aliases may stay mirrored for compatibility. Adding a
new sector/arm/specialist logical agent **does not require adding a sixth fixed
alias** or editing a fixed roster table.

---

## Agent surfaces

These are execution/instruction surfaces, not separate fleets:

| Surface | Path | Role |
|---|---|---|
| Root/scoped coding guidance | `AGENTS.md`, `**/AGENTS.md` | repository and authority precedence |
| Claude compatibility agents | `.claude/agents/` | developer-facing executor aliases/specialists |
| Codex compatibility agents | `.codex/agents/` | mirrored developer-facing aliases/specialists |
| Cursor rules | `.cursor/rules/` | editor execution guidance |
| Agentic Holding registry | `dealix/agentic_holding/` | canonical logical hierarchy/runtime authority |
| Session Factory | `scripts/ops/session_factory.py` | one bounded execution/session fabric |
| ResourceGovernor | canonical runtime resource policy | capacity/admission authority |
| OpenCode | project/runtime config + CLI | bounded code/research execution after admission |
| Autonomous growth/research | `autonomous_growth/agents/` | internal research/evolution workers under canonical authority |
| Company Brain/acquisition | `auto_client_acquisition/` | evidence, opportunity and commercial workflows |
| MCP tools | `mcp_server/` | governed tool surface; cannot mint commercial/model authority |

No surface may create a parallel scheduler, work queue, Company Brain, Opportunity
Graph, model router, approval center, Proof Ledger or company database.

---

## The non-negotiables

These remain hard constraints regardless of logical agent count:

1. No scraping systems.
2. No cold WhatsApp automation.
3. No automated personal LinkedIn activity.
4. No fake or unsourced claims.
5. No guaranteed sales/revenue/ROI claims.
6. No PII/secrets in logs or proof artifacts.
7. No source-less knowledge answer where provenance is required.
8. No material external action without exact action-bound authority.
9. No orphan/unidentified logical agent or namespace.
10. No customer-value/public-proof claim without evidence and permission.
11. No execution success claim from process exit/HTTP 200 alone; acceptance receipt
    and release identity are separate evidence.

Current doctrine tests plus registry/audit acceptance enforce these rules. If a
request conflicts, the agent must fail closed and continue any independent safe
work that remains possible.

---

## Permission / effect model

Current precedence is:

- **L0 Observe** — read/inspect.
- **L1 Analyze** — classify/prioritize.
- **L2 Draft** — create reviewable artifacts.
- **L3 Internal Execute** — update internal queues/files/receipts.
- **L4 Repo Execute** — isolated source change, tests, branch/draft PR, safe patch.
- **L5 External/Material Execute** — merge, production deploy/cutover, send/publish,
  spend/payment/refund, binding quote/contract, tender submission, DNS/DB/secrets/
  provider/billing mutation, destructive operation. Requires exact action-bound
  authority.

Historical permission labels in older docs are compatibility/provenance only when
they conflict with this current effect model.

---

## OpenCode / model boundary

Canonical path:

`governed ingress -> Session Factory -> exact-head isolated worktree -> canonical model/cost/data broker -> OpenCode Builder -> independent Verifier -> receipt`

Workers request task/model class and trusted data sensitivity; they do not select
provider entitlement. Project config, worker env, provider defaults, last-used
model, or self-authored receipts cannot mint model/cost/data/privacy authority or
downgrade sensitivity.

Automatic routing target:
`deterministic/no-model -> adequate local/private -> suitable data-eligible VERIFIED-FREE -> trusted included capacity with cost/privacy/data authority -> HOLD`. Provider family alone never grants authority; arbitrary paid capacity remains approval-gated.

---

## How to add or change a logical agent

1. Change the canonical sector/arm/registry source, not this document first.
2. Build `build_current_registry()` and require `orphan_failures=[]`.
3. Confirm the new identity has a valid parent namespace, bounded authority and
   capabilities.
4. If an editor-specific definition is useful, add it as a surface/compatibility
   projection; never turn that file count into fleet architecture authority.
5. Add/update focused regressions and run `python scripts/audit_agent_team.py --strict`.
6. For modifying work, use Session Factory exact-head isolation and independent
   verification.
7. Material effects remain separate L5 actions.

No new framework or permanent process is required merely to represent a new
logical specialist.

---

## Verification

```bash
python scripts/audit_agent_team.py --strict
```

A governance PASS requires at minimum:

- canonical current registry builds;
- `orphan_failures=[]` and `unmapped_arms=[]`;
- required governance/source surfaces exist;
- legacy alias files may be present without becoming fleet-size authority;
- scoped/root guidance does not re-promote fixed-five, retired commercial terms,
  provider/model bypasses or a second execution fabric;
- doctrine guard tests remain present;
- current registry receipt is recorded in the audit report.

## Auditor prompt

```text
You are a Dealix Omega V3 governance verifier.
Inspect the current Agentic Holding registry, scoped/root AGENTS guidance, Session
Factory/ResourceGovernor boundaries, OpenCode/model authority, commercial truth
and doctrine tests. Do not infer fleet size from editor-agent files. Require zero
orphans/unmapped arms. Preserve legacy aliases only as compatibility surfaces.
Safe L0-L4 verification may run in exact-head isolated worktrees. Do not merge,
deploy, send, publish, spend, mutate production/DNS/DB/secrets/providers, or
perform any other L5 effect without exact action-bound authority.
```
