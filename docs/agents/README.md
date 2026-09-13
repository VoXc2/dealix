# Dealix Agent Governance — حوكمة منظومة الوكلاء

This directory documents the **current Omega V3 Agentic Holding authority**. It is
not a fixed roster and it must not create a second scheduler, queue, model router,
Company Brain, Opportunity Graph, Approval Center, Proof Ledger, or execution
fabric.

## Canonical architecture

`Dealix Holding -> Company Control Plane -> Sector Companies -> Arm Pods -> Specialist Logical Agents -> ResourceGovernor-bounded runtime workers`

The current logical roster is derived from
`dealix.agentic_holding.runtime.build_current_registry()` and the canonical sector
and arm registries. Counts are runtime/source observations, not permanent product
architecture targets.

The historical names `dealix-pm`, `dealix-sales`, `dealix-delivery`,
`dealix-engineer`, and `dealix-content` remain **legacy executor aliases / compatibility
entrypoints only**. They do not define fleet size, sector coverage, WIP, model
routing, or the company architecture.

## Execution fabric

`Hermes / Founder / governed ingress -> canonical Session Factory -> isolated exact-head worktree/session -> OpenCode -> independent verifier -> receipt`

- ResourceGovernor is runtime-capacity authority.
- Builder != Verifier.
- Safe internal/source work L0-L4 may execute autonomously in bounded exact-head
  worktrees with acceptance evidence.
- Material external effects remain exact action-bound L5: merge, production
  deploy/cutover, external send/publication, payment/spend, binding quote/contract,
  tender submission, DNS/DB/secrets/provider/billing mutation, and destructive
  operations.
- Automatic model execution follows the canonical Dealix model/cost/data broker.
  Founder unattended law is **NO_DEEPSEEK** and no silent paid spill.

## Commercial truth loaded into agents

`Free Execution Diagnostic -> Qualified Discovery -> Customer-Specific Quote -> Outcome Sprint/Pilot -> Proof Review -> Dealix Runtime | Stop | Expand | Redesign`

All diagnostics are free by current default authority. No active agent may mint a
public fixed price, fixed duration, guaranteed outcome, unsupported compliance or
residency claim, or treat historical compatibility IDs as current commercial
terms.

Truth firewall: Research != Relationship; Public Contact != Consent; Signal !=
Qualified Problem; Draft != Sent; Quote != Invoice; Invoice != Payment; Payment !=
Revenue; Delivery != Customer Value; Customer Value != Public Proof; Merged !=
Deployed; HTTP 200 != release identity.

## Read in this order

1. [`AGENT_TEAM_REGISTRY.md`](AGENT_TEAM_REGISTRY.md) — registry-derived authority,
   surfaces, compatibility aliases, non-negotiables, and extension rules.
2. [`AGENT_PERMISSION_MATRIX.md`](AGENT_PERMISSION_MATRIX.md) — permission levels
   and hard effect boundaries; Omega V3 L0-L4/L5 precedence wins over historical
   wording if a legacy level label conflicts.
3. [`AGENT_OUTPUT_CONTRACT.md`](AGENT_OUTPUT_CONTRACT.md) — evidence/output contract.
4. [`AGENT_DAILY_RUNBOOK.md`](AGENT_DAILY_RUNBOOK.md) — daily internal execution.
5. [`AGENT_SECURITY_POLICY.md`](AGENT_SECURITY_POLICY.md) — hard security boundaries.
6. [`TOKEN_BUDGET_POLICY.md`](TOKEN_BUDGET_POLICY.md) — resource discipline.
7. [`PR_TRIAGE_POLICY.md`](PR_TRIAGE_POLICY.md) — PR prioritization and evidence.

Scoped `AGENTS.md` files closest to authority-sensitive source paths refine root
repo guidance and must preserve this Omega V3 law.

## Verify the governed company mesh

```bash
make agents-audit
# equivalent:
python scripts/audit_agent_team.py --strict
```

The audit must prove current registry construction succeeds, `orphan_failures=[]`,
required governance surfaces exist, historical fixed-five aliases are not promoted
to architecture authority, and the doctrine guards remain present. Claude/Codex
file parity is compatibility hygiene only; it is not a count of the logical fleet.

## Related

- [`../../AGENTS.md`](../../AGENTS.md) — root repository guidance; current Omega V3
  governance and scoped `AGENTS.md` precedence override historical fleet wording.
- [`../../dealix/agentic_holding/runtime.py`](../../dealix/agentic_holding/runtime.py)
  — registry/runtime authority.
- [`../company/DEALIX_OPENCODE_AUTONOMY_POLICY_V3.md`](../company/DEALIX_OPENCODE_AUTONOMY_POLICY_V3.md)
  when present on the accepted OpenCode lane.
- [`../ops/FOUNDER_AGENT_PLAYBOOK_AR.md`](../ops/FOUNDER_AGENT_PLAYBOOK_AR.md) —
  founder-facing provenance/runbook; current authority still comes from the
  registry and machine-readable control plane.
