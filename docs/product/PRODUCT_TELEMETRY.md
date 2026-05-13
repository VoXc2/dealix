# Product Telemetry

> What Dealix measures to know whether the product is working — for the
> customer, for governance, and for the business. Phase-1 captures these as
> spreadsheet rows; Phase-2 surfaces them in the AI Control Tower
> (`AI_CONTROL_TOWER.md`) and the business KPI dashboard
> (`docs/BUSINESS_KPI_DASHBOARD_SPEC.md`).

## Five families of telemetry

Every metric belongs to one of: **Usage**, **Quality**, **Governance**,
**Value**, **Economics**. If a metric doesn't fit, it's noise.

## Usage

| Metric | Source |
|--------|--------|
| Active clients (30-day) | Billing + project state |
| Active workflows / week | Event store |
| Reports generated | `dealix/reporting/executive_report.py` |
| Proof packs published | `dealix/reporting/proof_pack.py` |
| Approvals issued | `dealix/trust/approval.py` |
| Active agents | `agent_observability` |

## Quality

| Metric | Source |
|--------|--------|
| QA score per service (1–5) | Reviewer rubric |
| Eval pass rate | `EVALUATION_REGISTRY.md` runners |
| Rework rate (% reopened) | Project state machine |
| Citation present rate (Brain) | Ragas |
| Arabic-tone score | Human rubric / DeepEval |

## Governance

| Metric | Source |
|--------|--------|
| Blocked actions | `dealix/trust/policy.py` |
| PII flags | `dealix/trust/pii_detector.py` |
| Forbidden-claim blocks | `dealix/trust/forbidden_claims.py` |
| Approvals overdue | Approval matrix |
| Source-missing incidents | Runtime governance check |

## Value (customer-side)

| Metric | Source |
|--------|--------|
| Proof events written | Event store |
| Hours saved (est.) | Customer-confirmed |
| Opportunities surfaced | RevenueAgent + customer confirmation |
| NPS / CSAT | Post-delivery survey |

## Economics

| Metric | Source |
|--------|--------|
| Cost per run (SAR) | LLM gateway + `MODEL_PORTFOLIO.md` |
| Cost per project (SAR) | Aggregated runs + delivery time |
| Margin per service (%) | Pricing − delivered cost |
| Cost over budget incidents | Gateway alerts |

## Phase-2 wiring

All five families flow into the AI Control Tower under `frontend/`. The
event store is the source of truth for Usage, Value, and Governance.
LiteLLM + Langfuse provide Economics and Quality telemetry. The Business
KPI dashboard consumes the same feed for revenue-side metrics.

## Hard rules

- No new service ships without its rows in this telemetry doc.
- A metric without a source path and a named owner is dropped.
- Customer-facing value metrics are always corroborated by a Proof event,
  never by an AI estimate alone.

## Cross-links

- `/home/user/dealix/docs/product/AI_CONTROL_TOWER.md`
- `/home/user/dealix/docs/product/SERVICE_RUNTIME_TABLE.md`
- `/home/user/dealix/docs/BUSINESS_KPI_DASHBOARD_SPEC.md`
- `/home/user/dealix/dealix/reporting/executive_report.py`
- `/home/user/dealix/dealix/reporting/proof_pack.py`
- `/home/user/dealix/auto_client_acquisition/revenue_memory/event_store.py`
- `/home/user/dealix/auto_client_acquisition/agent_observability/`
