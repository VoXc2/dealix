# AI Control Tower

> A single operator pane for the running AI surface of Dealix. Phase-1 is a
> Notion-style snapshot; Phase-2 is a live dashboard under `frontend/` backed
> by the event store. The Control Tower exists so that AI sprawl never
> becomes an unmonitored line of business.

## Why a Control Tower

Dealix runs many AI workflows across many customers. Without one operator
view, "is AI behaving today" becomes guesswork. Gartner's agent-sprawl
warning applies directly: agents that aren't watched drift, leak cost, and
ship low-quality outputs to paying customers.

## What it monitors

| Monitor | Purpose | Source of truth |
|---------|---------|----------------|
| AI runs (volume, p95 latency) | Are agents actually doing work? | `AI_RUN_LEDGER.md` + event store |
| Cost (SAR per day / per customer / per agent) | Margin protection | LLM gateway + `MODEL_PORTFOLIO.md` budgets |
| Prompt versions in use | Detect drift, unauthorized prompts | `PROMPT_REGISTRY.md` + run logs |
| Eval scores (rolling) | Quality assurance | `EVALUATION_REGISTRY.md` + nightly runs |
| Governance flags | Block / redact / escalate counts | `dealix/trust/policy.py` outputs |
| Approval status | Approvals overdue per customer | `dealix/trust/approval_matrix.py` |
| Error rates | Provider, schema, validator failures | gateway + Pydantic round-trip log |
| Customer-facing outputs | What actually shipped today | `dealix/reporting/proof_pack.py` + `executive_report.py` |

## Alerts (Phase 2 wiring)

| Alert | Trigger | Routing | Severity |
|-------|---------|---------|---------:|
| Cost over budget | daily SAR cost > soft budget per `MODEL_PORTFOLIO.md` | HoP + CRO | High |
| QA below threshold | rolling eval score < pass threshold | Eval owner + HoP | High |
| Governance block | `ComplianceGuardAgent` returned `BLOCK` | HoLegal + delivery owner | High |
| PII detected | `pii_detector.py` flag on outbound output | HoLegal + HoData | Critical |
| Source missing | retrieval returned zero / source check failed | HoData + agent owner | Medium |
| Hallucination risk | low faithfulness from Ragas on Company Brain run | KnowledgeAgent owner | High |
| Approval overdue | queued action older than per-stage SLA | Approver + HoP | Medium |
| Schema violation | output failed Pydantic round-trip | agent owner | Medium |

## Phase-1 deliverable

Phase-1 surfaces the same data as a weekly snapshot tab in
`docs/ledgers/AI_RUN_LEDGER.md` plus a Friday review note in
`SALES_OPS_SOP.md` §10. No live UI; humans run the queries.

## Phase-2 deliverable

A dashboard surface under `frontend/` consuming:

- `auto_client_acquisition/agent_observability/*` for run metadata
- `auto_client_acquisition/revenue_memory/event_store.py` for proof events
- LiteLLM + Langfuse for prompt version and cost telemetry
- `dealix/trust/audit.py` for governance decisions

Every tile clicks through to the underlying run, prompt, eval, or
governance decision so an operator can act in one click (pause agent,
rerun with stronger model, escalate).

## Hard rules

- Every customer-facing output is reachable from the Control Tower with
  three clicks: customer → workflow → AI run → prompt + eval + governance
  decision.
- An alert without a named owner is not an alert; it's noise.
- Phase-2 ships behind feature flag; access is RBAC-scoped to operator role.

## Cross-links

- `/home/user/dealix/docs/product/AI_AGENT_INVENTORY.md`
- `/home/user/dealix/docs/product/PROMPT_REGISTRY.md`
- `/home/user/dealix/docs/product/EVALUATION_REGISTRY.md`
- `/home/user/dealix/docs/product/MODEL_PORTFOLIO.md`
- `/home/user/dealix/docs/product/AGENT_LIFECYCLE_MANAGEMENT.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/docs/governance/AI_MONITORING_REMEDIATION.md`
- `/home/user/dealix/docs/ledgers/AI_RUN_LEDGER.md`
- `/home/user/dealix/dealix/trust/policy.py`
- `/home/user/dealix/dealix/trust/audit.py`
- `/home/user/dealix/auto_client_acquisition/agent_observability/`
