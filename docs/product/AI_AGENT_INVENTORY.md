# AI Agent Inventory

> The canonical registry of every named AI agent in Dealix. Gartner's
> "agent sprawl" warning is real — Dealix avoids it by registering, scoping,
> auto-leveling, and monitoring every agent. No unregistered agent ships.

## Agent table (Phase-1 catalog)

| Agent | Capability served | Allowed tools | Data access | Autonomy level | Risk | Status |
|-------|-------------------|---------------|-------------|---------------:|------|--------|
| DataQualityAgent | Data | `data_os` modules | customer datasets | 1 | Medium | MVP |
| RevenueAgent | Revenue | `revenue_os/lead_scoring`, `icp_builder` | accounts | 2 | Medium | MVP |
| OutreachAgent | Revenue / Marketing | drafts only (no send) | accounts + offer | 2 | High | MVP |
| SupportAgent | Customer | `customer_os` (Phase 2) | support corpus | 2 | High | Designed |
| KnowledgeAgent | Knowledge | `knowledge_os/retrieval` | approved docs only | 2 | High | Beta |
| WorkflowAgent | Operations | `orchestrator/runtime` | workflow state | 2 | Medium | MVP |
| ReportingAgent | Reporting | `reporting/executive_report`, `proof_pack` | project outputs | 2 | Medium | MVP |
| ComplianceGuardAgent | Governance (mandatory gate) | `dealix/trust/*` policy + PII + claims | action metadata | 3 | High | MVP |
| DeliveryManagerAgent | All (stage machine) | `delivery_factory/stage_machine` | project state | 3 | Medium | MVP |
| StrategyAgent | Strategy (Phase 3) | `strategy_os` (planned) | customer profile | 1 | Low | Not Ready |

## Autonomy levels (per `docs/governance/RUNTIME_GOVERNANCE.md`)

```
0 = passive helper            (read-only)
1 = analyze                   (classify, score, summarize)
2 = draft / recommend         (no side-effect, human reviews)
3 = queue action for approval (action prepared; awaits approver)
4 = execute internal action   (after approval)
5 = execute external          (enterprise-only; per-action approval)
6 = autonomous external       (FORBIDDEN, no exceptions)
```

## Dealix MVP rule

```
Allowed in MVP:  Levels 0–3
Restricted:      Level 4 (requires explicit approval per action)
Enterprise-only: Level 5 (with full audit + procurement-grade contract)
Forbidden:       Level 6
```

## Agent Card requirement

Every entry above has a corresponding Agent Card in
`docs/product/agent_cards/<agent>.md` per
`docs/product/AI_WORKFORCE_OPERATING_MODEL.md`. **No agent ships in
production without a card.**

## Promotion gate (Designed → Beta → MVP → Production)

| Stage | Requirements |
|-------|--------------|
| Designed | Agent Card written + scope reviewed |
| Beta | Eval test in `EVALUATION_REGISTRY.md` passes; one supervised customer use |
| MVP | 3 successful supervised runs; no Hard Fail |
| Production | 30 days stable in MVP; CTO + HoLegal co-sign; promotion logged in Decision Ledger |

## Agent Lifecycle (sourced from Gartner agent-sprawl guidance)

```
Proposed → Designed → Simulated → Evaluated → Approved
        → Monitored → Improved → (Retired)
```

Retire an agent when:
- It is no longer used in any active workflow.
- Its error rate exceeds the agent's eval threshold.
- A better-scoring replacement exists.
- Its risk rises above its delivered value.

## Information-access principle (Permission Mirroring)

Per `docs/governance/RUNTIME_GOVERNANCE.md`:

> An agent may only access data and perform actions that the requesting
> user is authorized to access or perform.

No "super-user agent". No bypass. Every access logged with `actor` = the agent id linked to the requesting user's session.

## Monitoring (Phase 2 telemetry)

- Run count per agent per week.
- Eval pass rate.
- Cost per agent run (LLM Gateway).
- Hard Fail count.
- Approval-required-but-not-received count.
- Average latency.

## Cross-links
- `docs/product/AI_WORKFORCE_OPERATING_MODEL.md`
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `docs/governance/RUNTIME_GOVERNANCE.md`
- `docs/product/agent_cards/` — per-agent specs
- `docs/product/EVALUATION_REGISTRY.md` — eval tests per agent
