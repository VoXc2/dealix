# Workflow Registry

> The canonical list of every Dealix workflow — service, risk, human-in-loop
> posture, status. Referenced by `WORKFLOW_RUNTIME_DESIGN.md` and
> `SERVICE_RUNTIME_TABLE.md`. Adding a row here is the entry ticket for any
> new automation.

## Status legend

| Status | Meaning |
|--------|---------|
| Designed | 8-step contract written; no code yet |
| Manual | Delivered today by a human |
| MVP | Automated; human reviews every customer-facing output |
| Production | Automated; eval at threshold; Control Tower monitored |
| Deprecated | Replaced or retired |
| Blocked | Open governance / eval / data gap |

## Registry (Phase-1)

| Workflow | Service | Risk | Human review | Owner | Status |
|----------|---------|------|--------------|-------|--------|
| Lead Import Preview | Lead Intel | Medium | Per batch | HoData | MVP |
| Account Scoring | Lead Intel | Medium | Top-50 sample | CRO | MVP |
| Outreach Drafting | Lead Intel | High | Per draft | HoCS | MVP |
| Outreach Send (customer-side) | Lead Intel | High | Customer-side | HoCS | Manual |
| Knowledge Answering | Company Brain | High | First-30-day source check | HoP | Beta |
| Source Onboarding | Company Brain | Medium | Owner + sensitivity | HoData | Designed |
| Freshness Sweep | Company Brain | Low | Read-only flag | HoData | Designed |
| Quick Win Diagnostic | AI Quick Win | Medium | Final report | CRO | Beta |
| Quick Win Pilot Selection | AI Quick Win | Medium | Yes | CRO | Beta |
| Support Triage | Support Desk | Medium | No (classify only) | HoCS | Designed |
| Support Reply Draft | Support Desk | High | Per reply | HoCS | Designed |
| Support Escalation | Support Desk | High | Yes | HoCS | Designed |
| Executive Report | All | Medium | Final QA | HoP | MVP |
| Proof Pack | All | Medium | Inputs+outputs sample | HoP | MVP |
| Weekly Customer Summary | All | Low | Yes | HoP | MVP |
| Governance Check (runtime) | All | Required | Automated | HoLegal | MVP |
| Approval Routing | All | Required | n/a | HoLegal | MVP |
| Source Registration | Governance Program | Medium | Yes | HoLegal | MVP |
| Agent Promotion Gate | Governance Program | High | CTO + HoLegal | HoLegal | MVP |
| Monthly Audit | Governance Program | Medium | Yes | HoLegal | MVP |
| Incident Response | Governance Program | Critical | Per SOP | HoLegal | MVP |

## Hard rules

- Every row has a named owner. "Team" is not an owner.
- A row in **Status = MVP** must have a prompt in `PROMPT_REGISTRY.md`, an
  eval in `EVALUATION_REGISTRY.md` at or above threshold, and a clean
  runtime governance pass (no open Hard Fail in `dealix/trust/policy.py`).
- A row in **Status = Blocked** must reference an open issue in
  `RISK_REGISTER.md` or a CTO-signed decision.
- `Risk = High` rows cannot promote past MVP without a Friday review in
  `SALES_OPS_SOP.md` §10.

## Lifecycle

```
Designed → Manual → MVP → Production → Deprecated
```

Most workflows graduate from `Manual` so the 8-step contract is proven by
humans before code.

## Cross-links

- `/home/user/dealix/docs/product/WORKFLOW_RUNTIME_DESIGN.md`
- `/home/user/dealix/docs/product/SERVICE_RUNTIME_TABLE.md`
- `/home/user/dealix/docs/product/AI_AGENT_INVENTORY.md`
- `/home/user/dealix/docs/product/AGENT_LIFECYCLE_MANAGEMENT.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `/home/user/dealix/auto_client_acquisition/orchestrator/runtime.py`
- `/home/user/dealix/auto_client_acquisition/delivery_factory/stage_machine.py`
