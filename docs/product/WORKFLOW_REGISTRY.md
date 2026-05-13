# Workflow Registry

> The canonical list of every Dealix workflow — what it delivers, which
> service it serves, the risk class, the human-in-loop posture, and the
> ship status. Referenced by `WORKFLOW_RUNTIME_DESIGN.md` and
> `SERVICE_RUNTIME_TABLE.md`. Adding a row here is the entry ticket for any
> new automation.

## Status legend

| Status | Meaning |
|--------|---------|
| Designed | 8-step contract written; no code yet |
| Manual | Delivered today by a human following the contract |
| MVP | Automated, behind a human reviewer for every customer-facing output |
| Production | Automated, eval at threshold, monitored in Control Tower |
| Deprecated | Replaced or retired; do not invoke |
| Blocked | Cannot ship — open governance / eval / data gap |

## Registry (Phase-1)

| Workflow | Capability | Service | Risk | Human review | Owner | Status |
|----------|-----------|---------|------|--------------|-------|--------|
| Lead Import Preview | Data / Revenue | Lead Intel | Medium | Yes (per batch) | HoData | MVP |
| Account Scoring | Revenue | Lead Intel | Medium | Yes (top-50 sample) | CRO | MVP |
| Outreach Drafting | Revenue | Lead Intel | High | Yes (per draft) | HoCS | MVP |
| Outreach Send (customer-side) | Revenue | Lead Intel | High | Customer-side; Dealix delivers approved drafts only | HoCS | Manual |
| Knowledge Answering | Knowledge | Company Brain | High | Yes (sources verified for first 30 days) | HoP | Beta |
| Source Onboarding | Knowledge / Governance | Company Brain | Medium | Yes (owner + sensitivity) | HoData | Designed |
| Freshness Sweep | Knowledge / Governance | Company Brain | Low | No (read-only flag) | HoData | Designed |
| Quick Win Diagnostic | Strategy | AI Quick Win | Medium | Yes (final report) | CRO | Beta |
| Quick Win Pilot Selection | Strategy | AI Quick Win | Medium | Yes | CRO | Beta |
| Support Triage | Customer | Support Desk | Medium | No (classification only) | HoCS | Designed |
| Support Reply Draft | Customer | Support Desk | High | Yes (per reply) | HoCS | Designed |
| Support Escalation Decision | Customer | Support Desk | High | Yes | HoCS | Designed |
| Executive Report | Reporting | All services | Medium | Yes (final QA) | HoP | MVP |
| Proof Pack | Reporting | All services | Medium | Yes (inputs + outputs sample) | HoP | MVP |
| Weekly Customer Summary | Reporting | All services | Low | Yes | HoP | MVP |
| Governance Check (runtime) | Governance | All services | Required | Automated; Hard Fail escalates | HoLegal | MVP |
| Approval Routing | Governance | All services | Required | n/a (humans approve) | HoLegal | MVP |
| Source Registration | Governance | Governance Program | Medium | Yes | HoLegal | MVP |
| Agent Promotion Gate | Governance | Governance Program | High | Yes (CTO + HoLegal) | HoLegal | MVP |
| Monthly Audit | Governance | Governance Program | Medium | Yes | HoLegal | MVP |
| Incident Response | Governance | Governance Program | Critical | Yes (per `INCIDENT_RESPONSE.md`) | HoLegal | MVP |

## Hard rules

- Every row has a named owner. "Team" is not an owner.
- A row in **Status = MVP** must have:
  - An entry in `PROMPT_REGISTRY.md` per AI step.
  - An eval in `EVALUATION_REGISTRY.md` at or above threshold.
  - A clean runtime governance pass (no open Hard Fail in
    `dealix/trust/policy.py`).
- A row in **Status = Blocked** must reference the open issue in
  `docs/governance/RISK_REGISTER.md` or a CTO-signed decision.
- Workflows with `Risk = High` cannot be promoted past MVP without a Friday
  review noted in `SALES_OPS_SOP.md` §10.

## Lifecycle

```
Designed  →  Manual  →  MVP  →  Production  →  Deprecated
                                 ↑                ↑
                                 │                │
                          (eval+monitor)    (replaced)
```

A workflow may skip `Manual` only if the capability is brand new with no
human predecessor — rare. Most workflows graduate from `Manual` so the
8-step contract is proven by humans before code.

## Cross-links

- `/home/user/dealix/docs/product/WORKFLOW_RUNTIME_DESIGN.md`
- `/home/user/dealix/docs/product/SERVICE_RUNTIME_TABLE.md`
- `/home/user/dealix/docs/product/AI_AGENT_INVENTORY.md`
- `/home/user/dealix/docs/product/AGENT_LIFECYCLE_MANAGEMENT.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `/home/user/dealix/auto_client_acquisition/orchestrator/runtime.py`
- `/home/user/dealix/auto_client_acquisition/delivery_factory/stage_machine.py`
